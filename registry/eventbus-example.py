#!/usr/bin/env python3
"""
Exemplo: EventBus para Gran-Mestre (inspirado em browser-use)

Este script demonstra como usar o padrão EventBus para coordenar agentes
de forma desaclopada, similar ao browser-use.

Uso:
    python3 eventbus-example.py
"""

import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Awaitable


# === EVENTOS ===

class EventType(Enum):
    """Tipos de eventos do sistema"""
    TASK_ASSIGNED = "task_assigned"
    TASK_COMPLETED = "task_completed"
    PHASE_STARTED = "phase_started"
    PHASE_COMPLETED = "phase_completed"
    VALIDATION_PASSED = "validation_passed"
    VALIDATION_FAILED = "validation_failed"
    ROLLBACK_REQUESTED = "rollback_requested"


@dataclass
class Event:
    """Evento base"""
    data: dict[str, Any]
    type: EventType = EventType.TASK_ASSIGNED
    source: str = ""
    timestamp: float = 0.0


@dataclass
class TaskAssignedEvent(Event):
    """Evento de task atribuída a agente"""
    task_id: str = ""
    agent_name: str = ""
    task_description: str = ""
    type: EventType = EventType.TASK_ASSIGNED


@dataclass
class TaskCompletedEvent(Event):
    """Evento de task completada"""
    task_id: str = ""
    agent_name: str = ""
    success: bool = False
    result: Any = None
    type: EventType = EventType.TASK_COMPLETED


@dataclass
class PhaseCompletedEvent(Event):
    """Evento de fase completada"""
    phase_name: str = ""
    artifacts: list[str] = None
    type: EventType = EventType.PHASE_COMPLETED


# === EVENT BUS ===

class EventBus:
    """Barramento de eventos desacoplado"""
    
    def __init__(self):
        self._handlers: dict[EventType, list[Callable]] = {}
        self._history: list[Event] = []
    
    def on(self, event_type: EventType, handler: Callable[[Event], Awaitable[None]]):
        """Registra handler para tipo de evento"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    async def emit(self, event: Event):
        """Emite evento para todos os handlers registrados"""
        self._history.append(event)
        
        if event.type in self._handlers:
            for handler in self._handlers[event.type]:
                try:
                    await handler(event)
                except Exception as e:
                    print(f"⚠️ Erro no handler {handler.__name__}: {e}")
    
    def get_history(self, event_type: EventType = None) -> list[Event]:
        """Retorna histórico de eventos"""
        if event_type:
            return [e for e in self._history if e.type == event_type]
        return self._history.copy()


# === WATCHDOGS ===

class ValidationWatchdog:
    """Watchdog que valida fases automaticamente"""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.on(EventType.PHASE_COMPLETED, self._validate_phase)
    
    async def _validate_phase(self, event: PhaseCompletedEvent):
        """Valida fase completada"""
        print(f"🔍 ValidationWatchdog: Validando fase '{event.phase_name}'...")
        
        # Simular validação
        await asyncio.sleep(0.1)
        
        # Critérios de validação
        if event.artifacts and len(event.artifacts) > 0:
            print(f"✅ Validação passou: {len(event.artifacts)} artefatos encontrados")
            await self.event_bus.emit(Event(
                type=EventType.VALIDATION_PASSED,
                data={"phase": event.phase_name},
                source="ValidationWatchdog"
            ))
        else:
            print(f"❌ Validação falhou: nenhum artefato")
            await self.event_bus.emit(Event(
                type=EventType.VALIDATION_FAILED,
                data={"phase": event.phase_name, "reason": "no_artifacts"},
                source="ValidationWatchdog"
            ))


class SecurityWatchdog:
    """Watchdog que verifica segurança"""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.on(EventType.TASK_ASSIGNED, self._check_task_security)
    
    async def _check_task_security(self, event: TaskAssignedEvent):
        """Verifica segurança da task"""
        print(f"🔒 SecurityWatchdog: Verificando task '{event.task_id}'...")
        
        # Verificar se a task é segura
        dangerous_patterns = ["rm -rf", "sudo", "chmod 777"]
        task_text = event.task_description.lower()
        
        for pattern in dangerous_patterns:
            if pattern in task_text:
                print(f"⚠️ Padrão perigoso detectado: {pattern}")
                await self.event_bus.emit(Event(
                    type=EventType.VALIDATION_FAILED,
                    data={"task": event.task_id, "reason": f"dangerous_pattern:{pattern}"},
                    source="SecurityWatchdog"
                ))
                return
        
        print(f"✅ Task segura")


# === AGENTES ===

class Agent:
    """Agente base"""
    
    def __init__(self, name: str, event_bus: EventBus):
        self.name = name
        self.event_bus = event_bus
    
    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """Executa task (implementar em subclasses)"""
        raise NotImplementedError


class PrometheusAgent(Agent):
    """Agente de planejamento"""
    
    def __init__(self, event_bus: EventBus):
        super().__init__("Prometheus", event_bus)
    
    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """Cria plano"""
        print(f"📋 Prometheus: Criando plano para '{task['description']}'...")
        
        # Simular criação de plano
        await asyncio.sleep(0.2)
        
        plan = {
            "id": "plan-001",
            "tasks": [
                {"id": "task-1", "description": "Implementar feature A"},
                {"id": "task-2", "description": "Implementar feature B"},
                {"id": "task-3", "description": "Testes"},
            ],
            "artifacts": ["PLAN.md", "CONTEXT.md"]
        }
        
        # Emitir evento de fase completada
        await self.event_bus.emit(PhaseCompletedEvent(
            data={"plan_id": plan["id"]},
            phase_name="PLANNING",
            artifacts=plan["artifacts"]
        ))
        
        return plan


class AtlasAgent(Agent):
    """Agente de execução"""
    
    def __init__(self, event_bus: EventBus):
        super().__init__("Atlas", event_bus)
    
    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """Executa task"""
        print(f"⚡ Atlas: Executando task '{task.get('id', 'unknown')}'...")
        
        # Emitir evento de task atribuída
        await self.event_bus.emit(TaskAssignedEvent(
            data={"task": task},
            task_id=task.get('id', 'unknown'),
            agent_name=self.name,
            task_description=task.get('description', '')
        ))
        
        # Simular execução
        await asyncio.sleep(0.3)
        
        result = {"output": "Feature implementada"}
        
        # Emitir evento de task completada
        await self.event_bus.emit(TaskCompletedEvent(
            data={"result": result},
            task_id=task.get('id', 'unknown'),
            agent_name=self.name,
            success=True,
            result=result
        ))
        
        return {"success": True, "output": "Feature implementada"}


class AthenaAgent(Agent):
    """Agente de revisão"""
    
    def __init__(self, event_bus: EventBus):
        super().__init__("Atena", event_bus)
    
    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """Revisa código"""
        print(f"🔍 Atena: Revisando código...")
        
        # Simular revisão
        await asyncio.sleep(0.2)
        
        return {
            "approved": True,
            "issues": [],
            "suggestions": ["Adicionar mais testes"]
        }


# === ORQUESTRADOR ===

class GranMestre:
    """Orquestrador central"""
    
    def __init__(self):
        self.event_bus = EventBus()
        self.agents: dict[str, Agent] = {}
        self.watchdogs: list[Any] = []
        
        # Registrar watchdogs
        self.watchdogs.append(ValidationWatchdog(self.event_bus))
        self.watchdogs.append(SecurityWatchdog(self.event_bus))
        
        # Registrar agentes
        self.agents["Prometheus"] = PrometheusAgent(self.event_bus)
        self.agents["Atlas"] = AtlasAgent(self.event_bus)
        self.agents["Atena"] = AthenaAgent(self.event_bus)
    
    async def process_request(self, request: str) -> dict[str, Any]:
        """Processa requisição do usuário"""
        print(f"\n🎯 Gran-Mestre: Processando '{request}'")
        print("=" * 50)
        
        # Fase 1: Planejamento
        print("\n📋 FASE 1: PLANEJAMENTO")
        plan = await self.agents["Prometheus"].execute({"description": request})
        
        # Fase 2: Execução
        print("\n⚡ FASE 2: EXECUÇÃO")
        results = []
        for task in plan["tasks"]:
            result = await self.agents["Atlas"].execute(task)
            results.append(result)
        
        # Fase 3: Revisão
        print("\n🔍 FASE 3: REVISÃO")
        review = await self.agents["Atena"].execute({"results": results})
        
        # Resumo
        print("\n" + "=" * 50)
        print("📊 RESUMO:")
        print(f"  Tasks executadas: {len(results)}")
        print(f"  Aprovação: {'✅' if review['approved'] else '❌'}")
        print(f"  Issues: {len(review['issues'])}")
        print(f"  Sugestões: {len(review['suggestions'])}")
        
        # Histórico de eventos
        print("\n📜 HISTÓRICO DE EVENTOS:")
        for event in self.event_bus.get_history():
            print(f"  - {event.type.value}: {event.data}")
        
        return {
            "plan": plan,
            "results": results,
            "review": review,
            "events": len(self.event_bus.get_history())
        }


# === MAIN ===

async def main():
    """Função principal"""
    print("🚀 Iniciando exemplo EventBus para Gran-Mestre")
    print("Inspiração: browser-use (https://github.com/browser-use/browser-use)")
    
    gran_mestre = GranMestre()
    
    # Processar requisição
    result = await gran_mestre.process_request(
        "Implementar sistema de login com OAuth2"
    )
    
    print("\n✅ Exemplo concluído!")
    print(f"Total de eventos: {result['events']}")


if __name__ == "__main__":
    asyncio.run(main())
