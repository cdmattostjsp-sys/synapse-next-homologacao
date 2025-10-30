import os
from pathlib import Path

PAGES_DIR = Path("streamlit_app/pages")

EXPECTED_PAGES = [
    "01_🔧 Insumos.py",
    "02_📄 DFD – Formalização da Demanda.py",
    "03_📘 ETP – Estudo Técnico Preliminar.py",
    "04_🧮 Pesquisa de Preços.py (reservado)",
    "05_📑 TR – Termo de Referência.py",
    "06_📜 Edital – Minuta do Edital.py",
    "07_🧩 Validador de Editais.py",
    "08_📜 Contrato.py",
    "09_⚠️ Alertas.py",
    "10_💡 Análise de Desempenho.py",
    "11_📊 Painel de Governança.py",
    "12_📈 Painel Executivo.py",
    "13_🧾 Relatório Técnico.py",
    "14_🔍 Comparador.py",
    "15_🗂️ Exportar Snapshot.py",
    "16_🔗 Integração.py"
]

print("=" * 50)
print("🔍 Teste de Integridade das Páginas – SynapseNext vNext")
print("=" * 50, "\n")

found_files = sorted([f.name for f in PAGES_DIR.glob("*.py")])
missing = []
ok = []

for expected in EXPECTED_PAGES:
    base_name = expected.split(" (")[0]  # remove comentários como (reservado)
    if any(f.startswith(base_name.split()[0]) for f in found_files):
        print(f"✅ {expected}")
        ok.append(expected)
    else:
        print(f"⚠️  {expected} – não encontrado")
        missing.append(expected)

print("\n" + "=" * 50)
print(f"Total esperado: {len(EXPECTED_PAGES)}")
print(f"Encontrado: {len(ok)}")
print(f"Ausentes: {len(missing)}")
print("=" * 50)

if missing:
    print("\n⚠️  Páginas ausentes (esperado, se reserva ativa):")
    for m in missing:
        print(f"   - {m}")

print("\n🧾 Teste concluído.")
print("=" * 50)
