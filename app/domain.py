from dataclasses import dataclass



@dataclass
class Issue:
    path: str
    message: str
    severity: str = "error"

@dataclass
class Report:
    ok: bool
    issues: list[Issue]  