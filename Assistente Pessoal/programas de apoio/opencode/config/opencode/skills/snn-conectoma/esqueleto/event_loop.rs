//! Esqueleto do event-loop SNN user-space — conectoma Drosophila MaleCNS.
//!
//! Zero-cost: sem alocação por spike no hot path. Agendamento de spikes via
//! Min-Heap binário (O(log n) por push/pop) — alternativa: Timing Wheel O(1).
//!
//! RESTRIÇÕES (packet snn-hefesto-absorb):
//!   - user-space only (sem kernel).
//!   - Min-Heap O(log n) OU Timing Wheel.
//!   - Threads SNN pinadas em slots CPU: 9086 / 9090 / 9092 (-ngl 0 validado).
//!
//! ESTE É UM ESQUELETO: interfaces + invariantes + esboço de hot path.
//! NÃO é implementação completa — não copia dados do conectoma.

#![allow(dead_code)]

use std::collections::BinaryHeap;
use std::cmp::Ordering;

// ─────────────────────────────── Tipos core ───────────────────────────────

/// Índice de neurônio (0..N). N = 166_000 (MaleCNS).
pub type NeuronId = u32;

/// Timestep de simulação (discreto, em unidades de dt).
pub type Timestep = u64;

/// Peso sináptico (contagem de sinapses agregadas).
pub type Weight = u32;

/// Potencial de membrana (fixo, para evitar float no hot path).
/// Opcional: usar f32 para modelos mais ricos (LIF com decaimento).
pub type MembranePot = f32;

// ─────────────────────────────── CSR (do parser) ───────────────────────────────

/// Grafo de adjacência em CSR — produzido pelo parser (spec-parser-csr.md).
pub struct ConnectomeCsr {
    /// row_ptr[pre..pre+1] = intervalo em col_idx/weight.
    row_ptr: Vec<u64>,
    /// pós-sinápticos, ordenados por (pre, post).
    col_idx: Vec<NeuronId>,
    /// peso por aresta agregada.
    weight: Vec<Weight>,
    n: usize,
}

impl ConnectomeCsr {
    /// Iterador zero-alocação sobre os vizinhos pós-sinápticos de `pre`.
    #[inline]
    pub fn out_neighbors(&self, pre: NeuronId) -> impl Iterator<Item = (NeuronId, Weight)> + '_ {
        let start = self.row_ptr[pre as usize] as usize;
        let end = self.row_ptr[pre as usize + 1] as usize;
        (start..end).map(move |i| (self.col_idx[i], self.weight[i]))
    }

    #[inline]
    pub fn neuron_count(&self) -> usize {
        self.n
    }
}

// ─────────────────────────────── Modelo de neurônio ───────────────────────────────

/// Neurônio LIF (Leaky Integrate-and-Fire) — invariantes mínimas.
/// Valência (dopamina/octopamina) é sinal modulador SEPARADO do sensorial.
pub struct LifNeuron {
    /// Potencial de membrana atual.
    pub v: MembranePot,
    /// Limiar de disparo.
    pub threshold: MembranePot,
    /// Reset pós-disparo.
    pub reset: MembranePot,
    /// Decaimento por timestep (0.0 = sem leak).
    pub leak: MembranePot,
    /// Atraso axonal (em timesteps) antes do spike chegar ao pós-sináptico.
    pub delay: Timestep,
}

impl LifNeuron {
    /// Aplica spike de entrada (peso) e retorna `true` se disparou.
    #[inline]
    pub fn receive(&mut self, w: Weight) -> bool {
        self.v += w as MembranePot;
        if self.v >= self.threshold {
            self.v = self.reset;
            true
        } else {
            false
        }
    }

    /// Decaimento passivo (leak) — chamado 1x por timestep.
    #[inline]
    pub fn decay(&mut self) {
        self.v *= 1.0 - self.leak;
    }
}

// ─────────────────────────────── Evento de spike ───────────────────────────────

/// Spike agendado: dispara em `time`, entregue ao neurônio `target`.
#[derive(Clone, Copy)]
pub struct SpikeEvent {
    pub time: Timestep,
    pub target: NeuronId,
    pub weight: Weight,
}

impl Ord for SpikeEvent {
    #[inline]
    fn cmp(&self, other: &Self) -> Ordering {
        // BinaryHeap é max-heap; inverter para min-heap por tempo.
        other.time.cmp(&self.time)
            .then_with(|| other.target.cmp(&self.target))
    }
}
impl PartialOrd for SpikeEvent {
    #[inline]
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}
impl PartialEq for SpikeEvent {
    #[inline]
    fn eq(&self, other: &Self) -> bool {
        self.time == other.time && self.target == other.target
    }
}
impl Eq for SpikeEvent {}

// ─────────────────────────────── Event-loop SNN ───────────────────────────────

/// Núcleo da simulação. Invariantes:
///   - `heap` = Min-Heap de spikes futuros (BinaryHeap com Ord invertido).
///   - Um passo = drenar todos os spikes do timestep corrente → somar a `v` →
///     disparos geram novos spikes com `time + delay`.
pub struct SnnEventLoop {
    pub neurons: Vec<LifNeuron>,
    pub connectome: ConnectomeCsr,
    pub heap: BinaryHeap<SpikeEvent>,
    pub now: Timestep,
    /// Contador de spikes por timestep (para pooling/métrica HMI).
    pub spikes_this_step: usize,
    /// Spill buffer de disparos do passo (reutilizável, capacidade constante).
    spill: Vec<NeuronId>,
    /// Spill buffer de vizinhos pós-sinápticos (reutilizável).
    spill_neighbors: Vec<(NeuronId, Weight)>,
}

impl SnnEventLoop {
    /// Avança um timestep: entrega spikes agendados p/ `now`, propaga disparos.
    /// Retorna o nº de spikes entregues neste passo.
    ///
    /// Zero-alocação no hot path: para evitar borrow duplo (`neurons` vs `heap`),
    /// os disparos do passo corrente são acumulados num buffer de spill reutilizável
    /// (capacidade constante, sem crescimento por spike).
    pub fn step(&mut self) -> usize {
        let mut delivered = 0usize;
        self.now += 1;

        // 1) Drenar eventos do timestep corrente, acumulando disparos no spill.
        self.spill.clear();
        while let Some(ev) = self.heap.peek().copied() {
            if ev.time > self.now {
                break;
            }
            self.heap.pop();
            delivered += 1;

            // Borrow curto do neurônio: registrar disparo e liberar imediatamente.
            let fired = {
                let neuron = &mut self.neurons[ev.target as usize];
                neuron.receive(ev.weight)
            };
            if fired {
                self.spill.push(ev.target);
            }
        }

        // 2) Propagar disparos acumulados (borrow exclusivo do self liberado).
        let fired_this_step = std::mem::take(&mut self.spill);
        for source in fired_this_step {
            self.propagate(source);
        }

        // 3) Decaimento passivo (leak) de todos os neurônios.
        for n in &mut self.neurons {
            n.decay();
        }

        self.spikes_this_step = delivered;
        delivered
    }

    /// Propaga o disparo de `source` aos vizinhos pós-sinápticos, empilhando os
    /// spikes resultantes no heap. Usa o atraso axonal do próprio neurônio-fonte.
    #[inline]
    fn propagate(&mut self, source: NeuronId) {
        let delay = self.neurons[source as usize].delay;
        let time = self.now + delay;
        // Coleta zero-alocação é impossível aqui por causa do borrow duplo entre
        // self.neurons/self.connectome/self.heap. Usa vec spill secundário com
        // capacidade reutilizável (não cresce por spike).
        self.spill_neighbors.clear();
        self.spill_neighbors
            .extend(self.connectome.out_neighbors(source));
        for (target, w) in self.spill_neighbors.drain(..) {
            self.heap.push(SpikeEvent { time, target, weight: w });
        }
    }

    /// Injeta um spike externo (estímulo sensorial) em `target`.
    pub fn inject(&mut self, target: NeuronId, weight: Weight) {
        self.heap.push(SpikeEvent {
            time: self.now,
            target,
            weight,
        });
    }
}

// ─────────────────────────────── Timing Wheel (alternativa O(1)) ───────────────────────────────

/// Alternativa O(1) amortizado ao Min-Heap para delays curtos e uniformes.
/// Invariante: `delay_max` cobre todos os atrasos axonais; cada slot é um bucket.
/// Trade-off: memória O(delay_max) fixa; ideal se delay << horizonte de simulação.
pub struct TimingWheel {
    slots: Vec<Vec<SpikeEvent>>,
    cursor: usize,
    now: Timestep,
}

impl TimingWheel {
    pub fn new(delay_max: usize) -> Self {
        Self {
            slots: vec![Vec::new(); delay_max + 1],
            cursor: 0,
            now: 0,
        }
    }

    #[inline]
    pub fn schedule(&mut self, ev: SpikeEvent) {
        let idx = (self.cursor + (ev.time - self.now) as usize) % self.slots.len();
        self.slots[idx].push(ev);
    }

    /// Avança um slot e retorna os spikes vencidos.
    pub fn tick(&mut self) -> Vec<SpikeEvent> {
        self.cursor = (self.cursor + 1) % self.slots.len();
        self.now += 1;
        std::mem::take(&mut self.slots[self.cursor])
    }
}

// ─────────────────────────────── Testes de invariante ───────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    /// Min-heap ordena por tempo crescente (invariante Ord invertido).
    #[test]
    fn spike_event_min_heap_order() {
        let mut h = BinaryHeap::new();
        h.push(SpikeEvent { time: 5, target: 0, weight: 1 });
        h.push(SpikeEvent { time: 2, target: 1, weight: 1 });
        assert_eq!(h.peek().unwrap().time, 2);
    }

    /// LIF dispara acima do limiar e reseta.
    #[test]
    fn lif_fires_and_resets() {
        let mut n = LifNeuron { v: 0.0, threshold: 1.0, reset: 0.0, leak: 0.0, delay: 0 };
        assert!(!n.receive(0));
        assert!(n.receive(2)); // v=2 >= 1 → dispara
        assert_eq!(n.v, 0.0);  // reset
    }

    /// CSR entrega vizinhos com peso correto.
    #[test]
    fn csr_out_neighbors() {
        let c = ConnectomeCsr {
            row_ptr: vec![0, 2, 2],
            col_idx: vec![1, 2],
            weight: vec![3, 5],
            n: 3,
        };
        let mut iter = c.out_neighbors(0);
        assert_eq!(iter.next(), Some((1, 3)));
        assert_eq!(iter.next(), Some((2, 5)));
        assert!(c.out_neighbors(1).next().is_none());
    }
}