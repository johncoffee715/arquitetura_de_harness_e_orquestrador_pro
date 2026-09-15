#!/usr/bin/env python3
# agents/gran-mestre-monitor.py — Monitor de infraestrutura do Gran-Mestre
# Autofagia de: /mnt/dados/Assistente Pessoal/agents/cairo_agent.py
# Adaptado para: Gran-Mestre Pipeline (observabilidade + auto-healing)

import os
import sys
import json
import time
import subprocess
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# =============================================================================
# CONFIGURAÇÃO (adaptável)
# =============================================================================

class Config:
    """Configuração centralizada — substitui hardcoded paths do Cairo original."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.base_dir = Path(os.environ.get("GRAN_MESTRE_BASE", "~/.opencode")).expanduser()
        self.log_dir = self.base_dir / "logs"
        self.state_dir = self.base_dir / "state"
        self.state_file = self.state_dir / "monitor_state.json"
        self.report_file = self.state_dir / "monitor_report.json"
        
        # Configurações de GPU (detectadas automaticamente)
        self.vram_total = self._detect_vram_total()
        self.gpu_device = os.environ.get("GPU_DEVICE", "/sys/class/drm/card1/device")
        self.rocm_smi = os.environ.get("ROCM_SMI", "/opt/rocm/bin/rocm-smi")
        
        # Configurações de serviços
        self.services = {
            "ollama": {"port": 11434, "critical": True},
            "qdrant": {"port": 6333, "critical": True},
            "opencode": {"port": 3000, "critical": False},
        }
        
        # Configurações de thresholds
        self.temp_critical = 80.0
        self.vram_critical_gb = 2.0
        self.gpu_usage_low_pct = 5
        self.vram_high_gb = 14.0
        
        # Carregar configuração externa se fornecida
        if config_path and Path(config_path).exists():
            self._load_config(config_path)
    
    def _detect_vram_total(self) -> int:
        """Detecta VRAM total automaticamente."""
        try:
            vram_path = Path(self.gpu_device) / "mem_info_vram_total"
            if vram_path.exists():
                return int(vram_path.read_text())
        except:
            pass
        return 16 * 1073741824  # Default: 16GB
    
    def _load_config(self, path: str):
        """Carrega configuração de arquivo JSON."""
        try:
            with open(path) as f:
                cfg = json.load(f)
                for key, value in cfg.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
        except Exception as e:
            print(f"[WARN] Erro ao carregar config: {e}")


# =============================================================================
# LOGGING
# =============================================================================

class Logger:
    """Sistema de logging estruturado."""
    
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def log(self, msg: str, level: str = "INFO", component: str = "Monitor"):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}][{component}][{level}] {msg}"
        print(line)
        
        log_file = self.log_dir / f"gran-mestre_{datetime.now().strftime('%Y%m%d')}.log"
        try:
            with open(log_file, "a") as f:
                f.write(line + "\n")
        except:
            pass


# =============================================================================
# GPU MONITORING (do Cairo original)
# =============================================================================

class GPUMonitor:
    """Monitoramento de GPU — herdado do Cairo com melhorias."""
    
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
    
    def vram_free_gb(self) -> float:
        """Retorna VRAM livre em GB."""
        try:
            vram_path = Path(self.config.gpu_device)
            total = int((vram_path / "mem_info_vram_total").read_text())
            used = int((vram_path / "mem_info_vram_used").read_text())
            return (total - used) / 1073741824
        except:
            return 16.0  # Default seguro
    
    def gpu_temp(self) -> float:
        """Retorna temperatura da GPU em Celsius."""
        try:
            r = subprocess.run(
                [self.config.rocm_smi, "--showtemp"],
                capture_output=True, text=True, timeout=5
            )
            for line in r.stdout.splitlines():
                if "edge" in line.lower():
                    return float(line.split()[-1].replace("C", ""))
        except:
            pass
        return 0.0
    
    def gpu_usage(self) -> int:
        """Retorna uso da GPU em percentual."""
        try:
            r = subprocess.run(
                [self.config.rocm_smi, "--showuse"],
                capture_output=True, text=True, timeout=5
            )
            for line in r.stdout.splitlines():
                if "GPU use" in line:
                    return int(line.split()[-1].replace("%", ""))
        except:
            pass
        return 0
    
    def collect(self) -> Dict:
        """Coleta todas as métricas da GPU."""
        return {
            "vram_free_gb": round(self.vram_free_gb(), 2),
            "gpu_temp_c": round(self.gpu_temp(), 1),
            "gpu_use_pct": self.gpu_usage(),
        }


# =============================================================================
# SERVICE MONITORING (do Cairo original)
# =============================================================================

class ServiceMonitor:
    """Monitoramento de serviços — herdado do Cairo com melhorias."""
    
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
    
    def is_alive(self, port: int) -> bool:
        """Verifica se um serviço está rodando na porta."""
        try:
            result = subprocess.run(
                ["ss", "-tlnp"],
                capture_output=True, text=True, timeout=5
            )
            return f":{port} " in result.stdout
        except:
            return False
    
    def check_all(self) -> Dict[str, bool]:
        """Verifica todos os serviços configurados."""
        status = {}
        for name, cfg in self.config.services.items():
            status[name] = self.is_alive(cfg["port"])
        return status


# =============================================================================
# AUTO-HEALER (do Cairo original, adaptado)
# =============================================================================

class AutoHealer:
    """Sistema de auto-healing — herdado do Cairo com melhorias."""
    
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
    
    def heal(self, issue: str, fix: str) -> bool:
        """Executa uma correção automática."""
        self.logger.log(f"Executando fix: {fix}", "FIX", "Healer")
        
        try:
            if fix == "restart_ollama":
                subprocess.run(["sudo", "systemctl", "restart", "ollama"], timeout=30)
                return True
            
            elif fix == "heal_gpu":
                env = os.environ.copy()
                env["HSA_OVERRIDE_GFX_VERSION"] = "9.0.6"
                subprocess.run(
                    ["bash", "-c", "pkill -f 'ollama serve'; sleep 3; ollama serve &"],
                    env=env, timeout=20
                )
                return True
            
            elif fix == "gpu_reset":
                subprocess.run(
                    ["bash", "-c", "echo auto | sudo tee /sys/class/drm/card1/device/power_dpm_force_performance_level"],
                    timeout=10
                )
                return True
            
            elif fix == "clear_vram":
                # Tentar liberar VRAM reiniciando Ollama
                subprocess.run(["sudo", "systemctl", "restart", "ollama"], timeout=30)
                return True
            
            else:
                self.logger.log(f"Fix desconhecido: {fix}", "WARN", "Healer")
                return False
        
        except Exception as e:
            self.logger.log(f"Erro ao executar fix {fix}: {e}", "ERROR", "Healer")
            return False


# =============================================================================
# DREAM ENGINE (do Cairo original, adaptado)
# =============================================================================

class DreamEngine:
    """Motor de consolidação de memória — herdado do Cairo com melhorias."""
    
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
    
    def dream(self, history: List[Dict]) -> Dict:
        """Executa ciclo de consolidação de memória."""
        self.logger.log("DREAMING: consolidando memória", "DREAM", "Dream")
        
        summary = {
            "ts": datetime.now().isoformat(),
            "modified": [],
            "avg_vram": 0.0,
            "status": "clean"
        }
        
        # Calcular VRAM média
        if history:
            avg_vram = sum(m.get("vram_free_gb", 0) for m in history) / len(history)
            summary["avg_vram"] = round(avg_vram, 2)
        
        # Verificar arquivos modificados
        state_file = self.config.state_dir / "bootstrap_state.json"
        if state_file.exists():
            try:
                state = json.loads(state_file.read_text())
                for rel, sha in state.get("sha256", {}).items():
                    path = self.config.base_dir / rel
                    if path.exists():
                        current = hashlib.sha256(path.read_bytes()).hexdigest()
                        if current != sha:
                            summary["modified"].append(rel)
            except Exception as e:
                self.logger.log(f"Erro ao verificar estado: {e}", "WARN", "Dream")
        
        if summary["modified"]:
            summary["status"] = "modified"
        
        # Salvar relatório
        try:
            self.config.report_file.write_text(json.dumps(summary, indent=2))
        except Exception as e:
            self.logger.log(f"Erro ao salvar relatório: {e}", "WARN", "Dream")
        
        self.logger.log(f"Dream concluído: {summary['status']}", "DREAM", "Dream")
        return summary


# =============================================================================
# ANALYZER (do Cairo original)
# =============================================================================

class Analyzer:
    """Análise de métricas — herdado do Cairo."""
    
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
    
    def analyze(self, metrics: Dict) -> Tuple[List[str], List[str]]:
        """Analisa métricas e retorna issues + fixes."""
        issues = []
        fixes = []
        
        # GPU temperatura crítica
        if metrics.get("gpu_temp_c", 0) > self.config.temp_critical:
            issues.append(f"TEMP CRÍTICA {metrics['gpu_temp_c']}°C")
            fixes.append("gpu_reset")
        
        # VRAM crítica
        if metrics.get("vram_free_gb", 16) < self.config.vram_critical_gb:
            issues.append(f"VRAM CRÍTICA {metrics['vram_free_gb']}GB")
            fixes.append("clear_vram")
        
        # Serviços offline
        if not metrics.get("ollama", True):
            issues.append("Ollama offline")
            fixes.append("restart_ollama")
        
        if not metrics.get("qdrant", True):
            issues.append("Qdrant offline")
            fixes.append("restart_qdrant")
        
        # CPU fallback detectado
        if (metrics.get("ollama", False) and 
            metrics.get("gpu_use_pct", 100) < self.config.gpu_usage_low_pct and
            metrics.get("vram_free_gb", 0) > self.config.vram_high_gb):
            issues.append("CPU FALLBACK detectado")
            fixes.append("heal_gpu")
        
        return issues, fixes


# =============================================================================
# GRAN-MESTRE MONITOR (main orchestrator)
# =============================================================================

class GranMestreMonitor:
    """Monitor principal do Gran-Mestre — evolução do Cairo Agent."""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = Logger(config.log_dir)
        self.gpu = GPUMonitor(config, self.logger)
        self.services = ServiceMonitor(config, self.logger)
        self.healer = AutoHealer(config, self.logger)
        self.dreamer = DreamEngine(config, self.logger)
        self.analyzer = Analyzer(config, self.logger)
    
    def collect(self) -> Dict:
        """Coleta todas as métricas."""
        gpu_metrics = self.gpu.collect()
        service_status = self.services.check_all()
        
        return {
            "ts": datetime.now().isoformat(),
            **gpu_metrics,
            **service_status,
        }
    
    def run(self, interval: int = 300, dream_after: int = 1800, auto_heal: bool = True):
        """Loop principal do monitor."""
        self.logger.log(f"Gran-Mestre Monitor iniciado interval={interval}s dream_after={dream_after}s")
        
        history = []
        last_act = time.time()
        dreaming = False
        
        while True:
            # Coletar métricas
            metrics = self.collect()
            history.append(metrics)
            
            # Manter histórico limitado
            if len(history) > 120:
                history.pop(0)
            
            # Analisar
            issues, fixes = self.analyzer.analyze(metrics)
            
            for issue in issues:
                self.logger.log(issue, "WARN", "Monitor")
            
            # Auto-heal ou dream
            if issues and auto_heal:
                for fix in fixes:
                    self.healer.heal(issue, fix)
                dreaming = False
                last_act = time.time()
            else:
                idle = time.time() - last_act
                if idle > dream_after and not dreaming:
                    self.dreamer.dream(history[-20:])
                    dreaming = True
                elif idle < dream_after:
                    dreaming = False
            
            # Salvar estado
            state = {
                "ts": metrics["ts"],
                "metrics": metrics,
                "issues": issues,
                "idle_secs": round(time.time() - last_act),
                "dreaming": dreaming,
            }
            
            try:
                self.config.state_file.write_text(json.dumps(state, indent=2))
            except Exception as e:
                self.logger.log(f"Erro ao salvar estado: {e}", "WARN", "Monitor")
            
            time.sleep(interval)
    
    def status(self) -> Optional[Dict]:
        """Retorna status atual."""
        if self.config.state_file.exists():
            return json.loads(self.config.state_file.read_text())
        return None
    
    def dream_now(self):
        """Executa dream imediatamente."""
        return self.dreamer.dream([])


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Gran-Mestre Monitor — Monitor de infraestrutura"
    )
    parser.add_argument("--daemon", action="store_true", help="Executar como daemon")
    parser.add_argument("--interval", type=int, default=300, help="Intervalo em segundos")
    parser.add_argument("--dream-after", type=int, default=1800, help="Dream após N segundos idle")
    parser.add_argument("--no-heal", action="store_true", help="Desabilitar auto-healing")
    parser.add_argument("--status", action="store_true", help="Mostrar status atual")
    parser.add_argument("--dream-now", action="store_true", help="Executar dream agora")
    parser.add_argument("--config", type=str, help="Arquivo de configuração JSON")
    
    args = parser.parse_args()
    
    # Inicializar configuração
    config = Config(args.config)
    config.log_dir.mkdir(parents=True, exist_ok=True)
    config.state_dir.mkdir(parents=True, exist_ok=True)
    
    # Inicializar monitor
    monitor = GranMestreMonitor(config)
    
    # Comandos
    if args.status:
        status = monitor.status()
        print(json.dumps(status, indent=2) if status else "Monitor não iniciado")
        return
    
    if args.dream_now:
        monitor.dream_now()
        return
    
    if args.daemon:
        pid = os.fork()
        if pid > 0:
            print(f"Gran-Mestre Monitor PID: {pid}")
            (config.state_dir / "monitor.pid").write_text(str(pid))
            return
    
    monitor.run(args.interval, args.dream_after, not args.no_heal)


if __name__ == "__main__":
    main()