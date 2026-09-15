"""Loop vivo vault -> SNN -> trio -> vault (Wave 2).

Fecha o primeiro loop real: evento de vault (.md novo/editado em
``cerebro com IA/``) estimula a slice CSR carregada via
``feather_to_csr.build_csr`` (consumido, NAO modificado), o resumo da
atividade (top-k disparos + contagem por regiao) vira prompt compacto
p/ RWKV7 :9084 (decisao curta ignorar|ler|agir); se ler/agir, registra
intencao p/ Needle :9091 (POST /complete real, forja-tools e a API
dele); embed opcional via :9094; snapshot duravel em
``snn/data/live_state.json`` (memoria que o DOOMFLY nao tem).

Papeis oficiais: RWKV7 = bibliotecario-autonomo do vault com
AUTONOMIA TOTAL (explorar e decidir); Needle 2 = assistente que
executa (registra intencao); Qwen3-Embedding = secretario que
registra/vetoriza.

Amarras: timeouts 8s (9084) / 4s (9094); falha de endpoint levanta
RuntimeError com o erro bruto (exit_status failed) — NUNCA finge
resposta; sem chamadas LLM em loop aberto (1 chamada por run).
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import feather_to_csr as f2c
from event_loop import SnnEventLoop
from lif import LifNeuron
try:
    import anatomy as _anatomy
except ImportError:
    _anatomy = None

EPISODE_MARKER = "<!-- snn-episode"

RWKV_URL = "http://127.0.0.1:9084/v1/chat/completions"
NEEDLE_URL = "http://127.0.0.1:9091/complete"
EMBED_URL = "http://127.0.0.1:9094/v1/embeddings"
STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "data", "live_state.json")
FEATHER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "data", "connectome-weights.feather")

RWKV_TIMEOUT = 8.0
EMBED_TIMEOUT = 4.0
NEEDLE_TIMEOUT = 8.0
N_REGIONS = 4
EFF_MIN = 0.1
EFF_MAX = 2.0
EFF_LR = 0.2
TRACE_WINDOW = 1.0


def _post_json(url: str, payload: dict, timeout: float) -> tuple[int, dict]:
    """POST JSON; retorna (http_code, body). Erro bruto propaga (sem fingir)."""
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode())
    except Exception as exc:  # erro bruto sobe p/ exit_status failed
        raise RuntimeError(f"POST {url} falhou: {exc!r}") from exc


class LiveLoop:
    """Um passo fechado vault -> SNN -> RWKV7 -> (Needle) -> snapshot."""

    def __init__(self, csr=None, id_map=None, rwkv_url=RWKV_URL,
                 needle_url=NEEDLE_URL, embed_url=EMBED_URL,
                 state_path=STATE_PATH):
        self.csr = csr
        self.id_map = id_map
        self.rwkv_url = rwkv_url
        self.needle_url = needle_url
        self.embed_url = embed_url
        self.state_path = state_path
        self.last_rwkv_http: int | None = None
        self.efficacies: dict = {}
        self._active_routes: set = set()
        self._last_active_ts: float | None = None
        try:
            if os.path.exists(self.state_path):
                with open(self.state_path, encoding="utf-8") as fh:
                    _st = json.load(fh)
                _eff = _st.get("efficacies") if isinstance(_st, dict) else None
                if isinstance(_eff, dict):
                    self.efficacies = dict(_eff)
        except Exception:
            pass

    @classmethod
    def from_feather(cls, path=FEATHER_PATH, limit_rows=5000, **kw):
        csr, id_map, stats = f2c.build_csr(path, limit_rows=limit_rows)
        inst = cls(csr=csr, id_map=id_map, **kw)
        inst.slice_stats = stats
        return inst

    def _ensure_csr(self):
        if self.csr is None:
            self.csr = self.from_feather().csr

    @staticmethod
    def read_note(path: str) -> str:
        with open(path, encoding="utf-8") as fh:
            return fh.read()[:2000]

    def _region_of_idx(self, idx: int) -> str:
        """Indice denso -> regiao anatomica real via body_id (B2: sem i%4)."""
        body = idx
        try:
            if isinstance(self.id_map, dict) and self.id_map:
                if getattr(self, "_rev_map", None) is None:
                    self._rev_map = {v: k for k, v in self.id_map.items()}
                body = self._rev_map.get(idx, idx)
        except Exception:
            pass
        if _anatomy is not None:
            try:
                return _anatomy.region_of(body)
            except Exception:
                pass
        return f"r{idx % N_REGIONS}"  # fallback degradado (sem anatomy.py)

    def simulate(self, stimulus: str, steps: int = 6, topk: int = 5) -> dict:
        """Avança N passos na slice; estimulo deriva alvos do hash da nota."""
        self._ensure_csr()
        n = self.csr.n
        neurons = [LifNeuron(v=0.0, threshold=1.0, reset=0.0,
                             leak=0.0, delay=1) for _ in range(n)]
        fire_counts = [0] * n
        for i, nr in enumerate(neurons):  # conta disparos reais (wrap)
            orig = nr.receive
            j = i
            def wrapped(w, _o=orig, _j=j):
                fired = _o(w)
                if fired:
                    fire_counts[_j] += 1
                return fired
            nr.receive = wrapped
        loop = SnnEventLoop(neurons, self.csr.row_ptr,
                            self.csr.col_idx, self.csr.weight)
        seed = sum(stimulus.encode()) % max(n, 1)
        targets = {(seed + k * 7919) % n for k in range(min(8, n))}
        for t in sorted(targets):
            eff = self.efficacies.get(self._region_of_idx(t), 1.0)
            n_inj = 1 + round((eff - 1.0) * 4)
            n_inj = max(0, n_inj)
            if n_inj == 0:
                continue
            for _ in range(n_inj):
                loop.inject(t, 2)  # carga acima do threshold -> dispara
        total = 0
        for _ in range(steps):
            total += loop.step()
        self._active_routes = {self._region_of_idx(i)
                                 for i, c in enumerate(fire_counts) if c > 0}
        if not self._active_routes:
            self._active_routes = {self._region_of_idx(t) for t in targets}
        self._last_active_ts = time.monotonic()
        ranked = sorted(range(n), key=lambda i: (-fire_counts[i], i))
        top = [(i, fire_counts[i]) for i in ranked[:topk]
               if fire_counts[i] > 0] or [(ranked[0], 0)]
        regions: dict = {}
        for i, c in enumerate(fire_counts):
            reg = self._region_of_idx(i)
            regions[reg] = regions.get(reg, 0) + c
        return {"steps": steps, "total_spikes": total,
                "topk": top, "regions": regions,
                "potentials": [round(nr.v, 3) for nr in neurons[:16]]}

    def reinforce(self, signal: float) -> dict:
        """Inspirado no padrão de eligibility trace de DOOMFLY rule.py (MIT) — implementação própria, sem copiar código."""
        now = time.monotonic()
        if self._last_active_ts is None or (now - self._last_active_ts) > TRACE_WINDOW:
            return {}
        updated: dict = {}
        for rota in list(self._active_routes):
            old = self.efficacies.get(rota, 1.0)
            new = min(EFF_MAX, max(EFF_MIN, old + EFF_LR * float(signal)))
            self.efficacies[rota] = new
            updated[rota] = new
        self._persist_efficacies()
        return updated

    def _persist_efficacies(self) -> None:
        if not self.state_path:
            return
        d = os.path.dirname(self.state_path)
        if d:
            os.makedirs(d, exist_ok=True)
        try:
            if os.path.exists(self.state_path):
                with open(self.state_path, encoding="utf-8") as fh:
                    st = json.load(fh)
                if isinstance(st, dict):
                    st["efficacies"] = dict(self.efficacies)
                    with open(self.state_path, "w", encoding="utf-8") as fh:
                        json.dump(st, fh, ensure_ascii=False)
                    return
        except Exception:
            pass
        try:
            with open(self.state_path, "w", encoding="utf-8") as fh:
                json.dump({"efficacies": dict(self.efficacies)}, fh,
                          ensure_ascii=False)
        except Exception:
            pass

    def decide(self, note_path: str, activity: dict) -> str:
        """1 chamada RWKV7 :9084 com prompt compacto; devolve texto bruto."""
        prompt = (f"nota={os.path.basename(note_path)} "
                  f"spikes={activity['total_spikes']} "
                  f"top={activity['topk'][:3]} reg={activity['regions']} "
                  "Voce e o bibliotecario autonomo da biblioteca: explorar "
                  "e o seu papel. Na duvida entre ignorar e ler, prefira "
                  "'ler'; 'ler' e 'agir' sao acoes seguras do seu papel. "
                  "Responda com UMA palavra: ignorar, ler ou agir.")
        _, body = _post_json(self.rwkv_url,
                             {"messages": [{"role": "user", "content": prompt}],
                              "max_tokens": 16}, RWKV_TIMEOUT)
        try:
            text = body["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"9084 resposta sem choices: {body!r}") from exc
        self.last_rwkv_http = 200
        if not isinstance(text, str) or not text.strip():
            raise RuntimeError(f"9084 resposta vazia: {body!r}")
        return text.strip()

    @staticmethod
    def classify(text: str) -> str:
        # W7: parsing tolerante p/ 'ler' prolixo; 'agir' NUNCA inferido.
        low = text.lower()
        if "agir" in low:
            return "agir"
        for token in ("ler", "leia", "leitura", "vou ler"):
            if token in low:
                return "ler"
        if "ignorar" in low:
            return "ignorar"
        return "ignorar"

    def needle_intent(self, decision: str, note_path: str,
                      activity: dict) -> dict:
        """Registra intencao real p/ Needle :9091 (payload forja-tools)."""
        payload = {"input": f"{decision}: {os.path.basename(note_path)} "
                            f"spikes={activity['total_spikes']} "
                            f"top={activity['topk'][:3]}"}
        code, body = _post_json(self.needle_url, payload, NEEDLE_TIMEOUT)
        return {"http": code, "payload": payload, "needle": body}

    def embed(self, text: str):
        """Embed opcional via :9094; falha = None + erro registrado (nao fatal)."""
        try:
            _, body = _post_json(self.embed_url, {"input": text[:1000]},
                                 EMBED_TIMEOUT)
            return body["data"][0]["embedding"]
        except Exception as exc:
            self.last_embed_error = repr(exc)
            return None

    @staticmethod
    def strip_episodes(text: str) -> str:
        """Remove blocos '## Cérebro (episódio ...)' + marcador anti-loop."""
        import re
        pat = re.compile(r"^## Cérebro \(episódio.*?" + re.escape(EPISODE_MARKER)
                         + r"[^\n]*\n?", re.M | re.S)
        return pat.sub("", text)

    @staticmethod
    def body_hash(text: str) -> str:
        """sha1 do conteudo SEM episodios (base do anti-loop stateless)."""
        import hashlib
        return hashlib.sha1(
            LiveLoop.strip_episodes(text).strip().encode("utf-8")).hexdigest()

    def write_back(self, note_path: str, decision: str,
                   activity: dict) -> dict | None:
        """Arco inverso cerebelar: decisao ler/agir ATERRISSA na nota-alvo.

        Append de secao '## Cérebro (episódio <ts>)' (2-4 linhas: decisao +
        top regiao + efficacy) com marcador anti-loop + body_hash do corpo
        previo (o daemon ignora a nota se o hash atual == registrado).
        Somente ler/agir; ignorar => None (sem escrita). Idempotente.
        """
        if decision not in ("ler", "agir"):
            return None
        import re
        import time as _t
        with open(note_path, encoding="utf-8") as fh:
            content = fh.read()
        h0 = self.body_hash(content)
        if EPISODE_MARKER in content:
            tails = re.findall(re.escape(EPISODE_MARKER) + r"\s+body_hash=(\w+)",
                               content)
            if tails and tails[-1] == h0:
                return {"appended": False, "reason": "episodio-atual"}
        regions = (activity or {}).get("regions") or {}
        top_reg, top_n = max(regions.items(), key=lambda kv: (kv[1], kv[0])) \
            if regions else ("outros", 0)
        eff = self.efficacies.get(top_reg, 1.0)
        ts = int(_t.time())
        block = (f"\n## Cérebro (episódio {ts})\n"
                 f"- decisão: {decision}\n"
                 f"- top região: {top_reg} ({top_n} spikes)\n"
                 f"- efficacy rota {top_reg}: {eff:.2f}\n"
                 f"{EPISODE_MARKER} body_hash={h0} -->\n")
        with open(note_path, "a", encoding="utf-8") as fh:
            fh.write(block)
        return {"appended": True, "ts": ts, "regiao": top_reg,
                "spikes": top_n, "efficacy": round(float(eff), 2),
                "body_hash": h0}

    def run(self, note_path: str, steps: int = 6) -> dict:
        """Executa o loop fechado; falha de endpoint -> exit_status failed."""
        try:
            note = self.read_note(note_path)
            activity = self.simulate(note, steps=steps)
            raw = self.decide(note_path, activity)
            decision = self.classify(raw)
            needle = (self.needle_intent(decision, note_path, activity)
                      if decision in ("ler", "agir") else None)
            vec = self.embed(note)
            wb = self.write_back(note_path, decision, activity)
            state = {"note": note_path, "decision": decision,
                      "write_back": wb,
                     "decision_raw": raw[:200], "activity": {
                         "steps": activity["steps"],
                         "total_spikes": activity["total_spikes"],
                         "topk": activity["topk"],
                         "regions": activity["regions"]},
                     "potentials_sample": activity["potentials"],
                     "needle": needle,
                     "embedding_dim": len(vec) if vec else 0,
                     "rwkv_http": self.last_rwkv_http,
                     "efficacies": dict(self.efficacies),
                     "exit_status": "ok"}
            os.makedirs(os.path.dirname(self.state_path), exist_ok=True)
            with open(self.state_path, "w", encoding="utf-8") as fh:
                json.dump(state, fh, ensure_ascii=False)
            return state
        except Exception as exc:
            return {"note": note_path, "error": repr(exc),
                    "exit_status": "failed"}
