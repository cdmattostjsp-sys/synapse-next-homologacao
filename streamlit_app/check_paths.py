# check_paths.py
from pathlib import Path

root = Path(__file__).resolve().parent
exports = root / "exports"

paths = {
    "analises": exports / "analises",
    "auditoria": exports / "auditoria",
    "relatorios": exports / "relatorios"
}

print("\n📁 Verificação de estrutura SynapseNext\n" + "-"*50)
for nome, caminho in paths.items():
    existe = "✅" if caminho.exists() else "❌"
    print(f"{existe} {nome:<12} → {caminho}")
print("-"*50)
