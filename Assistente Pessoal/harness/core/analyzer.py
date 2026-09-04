import re
import unicodedata
from dataclasses import dataclass, field
from typing import Dict, List


def _norm(text: str) -> str:
    """Strip accents and lowercase text for matching."""
    return "".join(
        c for c in unicodedata.normalize("NFD", text.lower())
        if unicodedata.category(c) != "Mn"
    )


@dataclass
class Demand:
    """Detected demand: tags, complexity and pipeline phases."""
    raw: str = ""
    tags: Dict[str, str] = field(default_factory=dict)
    complexity: str = "SIMPLE"
    phases: List[str] = field(default_factory=list)


class ContextAnalyzer:
    """Regex + light NLP classification of task demands (stdlib only)."""

    RULES = {
        "coding": [
            ("implement", "true"), ("criar", "true"), ("escrever", "true"),
            ("codigo", "true"), ("code", "true"), ("build", "true"),
            ("feature", "true"), ("funcao", "true"), ("api", "true"),
            ("endpoint", "true"), ("server", "true"), ("mcp", "true"),
        ],
        "mcp": [
            ("model context protocol", "true"), ("mcp", "true"),
        ],
        "auth": [
            ("jwt", "jwt"), ("oauth", "oauth"), ("token", "token"),
            ("login", "login"), ("authentication", "auth"),
            ("autenticacao", "auth"), ("auth", "auth"),
        ],
        "infra": [
            ("postgresql", "postgres"), ("postgres", "postgres"),
            ("database", "database"), ("banco", "database"),
            ("redis", "redis"), ("kafka", "kafka"), ("docker", "docker"),
            ("aws", "aws"), ("gcp", "gcp"), ("sql", "sql"),
            ("cloud", "cloud"), ("infra", "infra"),
        ],
        "policy": [
            (r"rate.?limit", "rate-limit"), ("throttl", "throttle"),
            ("quota", "quota"), ("limite", "limite"),
            ("politica", "policy"), ("policy", "policy"),
        ],
        "test": [
            ("tdd", "tdd"), ("coverage", "coverage"), ("cobertura", "coverage"),
            ("teste", "test"), ("test", "test"), ("verifica", "verify"),
            ("verify", "verify"),
        ],
        "docs": [
            ("readme", "readme"), ("documenta", "docs"), ("doc", "docs"),
        ],
    }

    SCORE_DOMAINS = ("coding", "auth", "infra", "policy", "test", "docs")

    def extract_demand(self, task: str) -> Demand:
        """Extract tags, complexity and pipeline phases from a task."""
        text = _norm(task)
        tags: Dict[str, str] = {}
        for domain, patterns in self.RULES.items():
            for pattern, value in patterns:
                if re.search(pattern, text):
                    tags[domain] = value
                    break
        score = sum(1 for d in self.SCORE_DOMAINS if d in tags)
        if len(task) > 200:
            score += 1
        complexity = self._level(score)
        return Demand(raw=task, tags=tags, complexity=complexity,
                      phases=self._phases(tags, complexity))

    def classify_complexity(self, task: str) -> str:
        """Classify task complexity only (TRIVIAL..CRITICAL)."""
        return self.extract_demand(task).complexity

    @staticmethod
    def _level(score: int) -> str:
        """Map a complexity score to a level bucket."""
        if score <= 1:
            return "TRIVIAL"
        if score <= 2:
            return "SIMPLE"
        if score <= 3:
            return "MEDIUM"
        if score <= 4:
            return "COMPLEX"
        return "CRITICAL"

    @staticmethod
    def _phases(tags: Dict[str, str], complexity: str) -> List[str]:
        """Derive the pipeline phases implied by tags and complexity."""
        phases = ["planning"]
        if "coding" in tags:
            phases.append("implementation")
        if "coding" in tags or "test" in tags:
            phases.append("testing")
        if "docs" in tags or complexity in ("COMPLEX", "CRITICAL"):
            phases.append("docs")
        return phases
