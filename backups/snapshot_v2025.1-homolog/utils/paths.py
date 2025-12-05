# utils/paths.py
from pathlib import Path

def ensure_exports_structure(project_root: Path | None = None) -> dict:
    root = project_root or Path(__file__).resolve().parents[1]
    analises   = root / "exports" / "analises"
    auditoria  = root / "exports" / "auditoria"
    relatorios = root / "exports" / "relatorios"
    for p in (analises, auditoria, relatorios):
        p.mkdir(parents=True, exist_ok=True)
    return {"root": root, "analises": analises, "auditoria": auditoria, "relatorios": relatorios}
