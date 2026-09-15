# Autofagia: Browser-Use

**Data:** 2024-07-24
**Fonte:** https://github.com/browser-use/browser-use (106k+ stars)
**Objetivo:** Absorver padrões arquiteturais de automação de browser com IA

---

## 1. Visão Geral do Projeto

Browser-Use é uma biblioteca Python >=3.11 que permite agentes de IA controlarem navegadores web autonomamente via CDP (Chrome DevTools Protocol). O agente navega páginas, interage com elementos e completa tarefas complexas processando HTML e tomando decisões via LLM.

**Stack Principal:**
- Python 3.11+ (async)
- Pydantic v2 para validação
- CDP (Chrome DevTools Protocol) via `cdp-use`
- EventBus (`bubus`) para arquitetura orientada a eventos
- uv para gerenciamento de dependências

---

## 2. Arquitetura Orientada a Eventos

### Padrão EventBus com Watchdogs

```python
class BrowserSession(BaseModel):
    # EventBus coordena múltiplos watchdogs
    _event_bus: EventBus = PrivateAttr()
    
    # Watchdogs especializados:
    # - DownloadsWatchdog: gerencia downloads de PDF
    # - PopupsWatchdog: gerencia dialogs JavaScript
    # - SecurityWatchdog: restringe domínios
    # - DOMWatchdog: processa snapshots DOM
    # - AboutBlankWatchdog: redireciona páginas vazias
```

**Aprendizado:** O EventBus permite desacoplamento entre componentes. Cada watchdog é independente e reage a eventos específicos. Padrão excelente para sistemas complexos.

### Eventos Tipados

```python
# Eventos são classes Pydantic
class BrowserStartEvent(BaseEvent):
    browser_profile: BrowserProfile

class NavigateToUrlEvent(BaseEvent):
    url: str
    target_id: TargetID

class ClickElementEvent(BaseEvent):
    node: EnhancedDOMTreeNode
    target_id: TargetID
```

**Aprendizado:** Eventos como modelos Pydantic garantem type safety e validação automática.

---

## 3. Padrão Service/Views

### Organização de Código

```
browser_use/
├── agent/
│   ├── service.py      # Lógica principal do Agent
│   ├── views.py        # Modelos Pydantic (AgentHistory, ActionResult)
│   └── prompts.py      # System prompts
├── browser/
│   ├── session.py      # BrowserSession (service)
│   ├── views.py        # BrowserStateSummary, TabInfo
│   └── profile.py      # BrowserProfile (config)
├── tools/
│   ├── service.py      # Tools (registry de ações)
│   └── views.py        # Action models
└── dom/
    ├── service.py      # DomService
    └── views.py        # DOMNode models
```

**Aprendizado:** Separar lógica (service.py) de modelos (views.py) mantém código organizado e testável.

---

## 4. Sistema de Tools/Actions

### Decorator Pattern para Ações

```python
tools = Tools()

@tools.action('Ask human for help with a question')
async def ask_human(question: str) -> ActionResult:
    answer = input(f'{question} > ')
    return ActionResult(extracted_content=f'Human responded: {answer}')

# Uso no Agent
agent = Agent(task='...', llm=llm, tools=tools)
```

### ActionResult Estruturado

```python
class ActionResult(BaseModel):
    extracted_content: str | None = None
    long_term_memory: str | None = None
    error: str | None = None
    is_done: bool = False
    success: bool | None = None
    attachments: list[str] | None = None
```

**Aprendizado:** Actions retornam ActionResult estruturado para ajudar o agente a raciocinar melhor. `long_term_memory` é especialmente útil para persistir contexto.

---

## 5. Integração com LLM

### Abstração de Múltiplos Providers

```python
from browser_use.llm.base import BaseChatModel

# Suporta: OpenAI, Anthropic, Google, Groq, etc.
llm = ChatBrowserUse(model='openai/gpt-5.5')
# ou
llm = ChatAnthropic(model='claude-opus-4-8')
# ou
llm = ChatGoogle(model='gemini-3-flash-preview')
```

### Message Manager

```python
class MessageManager:
    """Gerencia histórico de conversas com compactação"""
    def __init__(self, ...):
        self.messages: list[BaseMessage] = []
        self.max_history_items = max_history_items
```

**Aprendizado:** Abstrair LLMs permite trocar providers sem mudar código do agente. Message Manager com compactação evita estourar contexto.

---

## 6. CDP (Chrome DevTools Protocol)

### Tipagem Forte com cdp-use

```python
from cdp_use import CDPClient
from cdp_use.cdp.target import ActivateTargetParameters

# Comandos tipados
await cdp_client.send.DOMSnapshot.enable(session_id=session_id)
await cdp_client.send.Target.attachToTarget(
    params=ActivateTargetParameters(targetId=target_id, flatten=True)
)

# Eventos registrados via callback
cdp_client.register.Browser.downloadWillBegin(callback_func)
```

**Aprendizado:** Wrapper tipado sobre CDP previne erros de API. `cdp-use` é a camada de abstração recomendada.

---

## 7. Padrões de Código

### 7.1. Type Hints Modernas

```python
# Python 3.12+ style
def process(data: str | None) -> dict[str, Any]:
    ...

# Não usar Optional[str] ou Dict[str, Any]
```

### 7.2. Pydantic v2 com ConfigDict

```python
class MyModel(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        validate_by_name=True,
        validate_by_alias=True,
    )
    
    id: str = Field(default_factory=uuid7str)
```

### 7.3. Logging Separado

```python
# Manter lógica de logging em métodos separados
def _log_pretty_path(path: Path) -> str:
    """Formata path para logging"""
    ...

# Usar no código principal
logger.info(_log_pretty_path(some_path))
```

### 7.4. Runtime Assertions

```python
async def process_page(page: Page) -> None:
    # Assertions no início para validar pré-condições
    assert page is not None, "Page cannot be None"
    assert page.url, "Page must have a URL"
    
    # ... lógica ...
    
    # Assertions no final para validar pós-condições
    assert result is not None, "Result cannot be None"
```

### 7.5. Async Consistente

```python
# Todo código é async
async def main():
    agent = Agent(task="...", llm=llm)
    history = await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 8. Configuração de Browser

### BrowserProfile

```python
class BrowserProfile(BaseModel):
    headless: bool = True
    window_size: dict = {'width': 1920, 'height': 1080}
    user_data_dir: Path | None = None
    proxy: ProxySettings | None = None
    allowed_domains: list[str] | None = None
    prohibited_domains: list[str] | None = None
    highlight_elements: bool = True
    enable_default_extensions: bool = True
```

### Detecção Automática de Display

```python
def detect_display_configuration() -> dict:
    """Detecta tamanho do display automaticamente"""
    # macOS: AppKit.NSScreen
    # Linux/Windows: screeninfo
    ...
```

**Aprendizado:** Configuração centralizada em Profile permite reuso e testabilidade.

---

## 9. Sistema de Watchdogs

### Padrão de Monitoramento

```python
class SecurityWatchdog:
    """Restringe navegação a domínios permitidos"""
    def __init__(self, browser_session: BrowserSession):
        self.session = browser_session
        self._register_events()
    
    def _register_events(self):
        self.session.event_bus.on('NavigationStarted', self._check_domain)
    
    async def _check_domain(self, event):
        if not self._is_allowed(event.url):
            raise SecurityError(f'Domain not allowed: {event.url}')
```

**Aprendizado:** Watchdogs são guardiões independentes que reagem a eventos. Padrão ideal para segurança, validação e monitoramento.

---

## 10. Lições de Design

### 10.1. APIs Ergonômicas

```python
# Bom: API intuitiva e difícil de usar errado
agent = Agent(task="Find stars", llm=llm)

# Ruim: API complexa e propensa a erros
agent = Agent(config=AgentConfig(task="Find stars", llm_config=LLMConfig(...)))
```

### 10.2. Estrutura de Pastas Clara

```
browser_use/
├── agent/          # Lógica do agente
├── browser/        # Controle do browser
├── dom/            # Processamento DOM
├── tools/          # Ações disponíveis
├── llm/            # Integração LLM
└── mcp/            # Protocolo MCP
```

### 10.3. Testes Sem Mocks

```python
# Regra: Nunca usar mocks em testes
# Exceção: Apenas para LLM (via fixtures)

@pytest.fixture
def mock_llm():
    # Mock apenas para LLM
    ...
```

### 10.4. URLs de Teste Locais

```python
# Nunca usar URLs reais em testes
# Usar pytest-httpserver para simular

@pytest.fixture
def test_server(httpserver):
    httpserver.expect_request('/').respond_with_data('<html>...</html>')
    return httpserver
```

---

## 11. Padrões Aplicáveis ao Nosso Sistema

### 11.1. EventBus para Orquestração

```python
# Aplicar ao Gran-Mestre para coordenar agentes
class GranMestreEventBus(EventBus):
    def __init__(self):
        super().__init__()
        self.on('TaskAssigned', self._delegate_to_agent)
        self.on('TaskCompleted', self._validate_result)
```

### 11.2. Sistema de Actions

```python
# Aplicar ao sistema de tools
registry = ToolRegistry()

@registry.action('Analyze code for security issues')
async def security_scan(code: str) -> ToolResult:
    ...
```

### 11.3. Watchdogs para Validação

```python
# Aplicar para gates de validação
class ValidationWatchdog:
    def __init__(self, event_bus):
        event_bus.on('PhaseCompleted', self._validate_phase)
```

### 11.4. Profile Pattern para Configuração

```python
# Aplicar para configuração de agentes
class AgentProfile(BaseModel):
    model: str = 'gpt-4'
    temperature: float = 0.0
    max_tokens: int = 4096
```

---

## 12. Comandos de Referência

```bash
# Setup
uv venv --python 3.11
source .venv/bin/activate
uv sync

# Testes
uv run pytest -vxs tests/ci

# Linting
uv run ruff check --fix
uv run ruff format

# Type checking
uv run pyright

# MCP Server
uvx browser-use[cli] --mcp
```

---

## 13. Conclusão

Browser-Use demonstra excelência em:

1. **Arquitetura orientada a eventos** com EventBus e Watchdogs
2. **Padrão Service/Views** para organização de código
3. **Sistema de Actions** com decorators para extensibilidade
4. **Abstração de LLM** para flexibilidade de providers
5. **Type safety** com Pydantic v2 e CDP tipado
6. **Testabilidade** sem mocks (exceção: LLM)

Estes padrões são diretamente aplicáveis ao nosso sistema de orquestração Gran-Mestre.

---

**Próximos Passos:**
- [ ] Implementar EventBus para Gran-Mestre
- [ ] Criar sistema de Actions com decorators
- [ ] Adotar padrão Service/Views
- [ ] Implementar Watchdogs para validação
