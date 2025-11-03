import os
import sys
import json
import importlib.util
from pathlib import Path

print("\n🧠 === DIAGNÓSTICO TÉCNICO – SYNAPSENEXT ===\n")

# 🧩 Ajusta sys.path
base_dir = Path(__file__).resolve().parent
streamlit_dir = base_dir / "streamlit_app"
utils_dir = streamlit_dir / "utils"

for p in [str(streamlit_dir), str(utils_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)
        print(f"🛠️ Caminho adicionado ao sys.path: {p}")

print("\n�� sys.path atualizado:")
for p in sys.path:
    print(f"   • {p}")
print()

# 🔑 Checa chave OpenAI
secrets_file = base_dir / ".streamlit" / "secrets.toml"
if secrets_file.exists():
    with open(secrets_file, "r") as f:
        if "OPENAI_API_KEY" in f.read():
            print("🔑 OpenAI Key: ✅ Detectada em .streamlit/secrets.toml.\n")
        else:
            print("🔑 OpenAI Key: ⚠️ Arquivo encontrado, mas chave não detectada.\n")
else:
    print("🔑 OpenAI Key: ⚠️ NÃO detectada (adicione em .streamlit/secrets.toml)\n")

# 📂 Estrutura principal
dirs = {
    "pages": streamlit_dir / "pages",
    "utils": utils_dir,
    "exports": base_dir / "exports" / "insumos" / "json"
}

for name, path in dirs.items():
    if path.exists():
        print(f"📁 streamlit_app/{name} → ✅ OK")
    else:
        print(f"📁 streamlit_app/{name} → ⚠️ NÃO encontrado")
print()

# 📦 Lista JSONs
json_dir = dirs["exports"]
if json_dir.exists():
    files = sorted(json_dir.glob("*.json"))
    if files:
        print("📦 Arquivos JSON encontrados:")
        for f in files:
            print(f"   • {f.name}")
        print()

        # Mostra conteúdo resumido dos principais
        for artefato in ["DFD", "ETP", "TR"]:
            latest = [f for f in files if f.name.startswith(f"{artefato}_ultimo")]
            if latest:
                f = latest[0]
                try:
                    data = json.load(open(f))
                    print(f"✅ {f.name} encontrado.")
                    print(f"   → Chaves: {list(data.keys())}")
                    print(f"   → Data processamento: {data.get('data_processamento', 'N/D')}\n")
                except Exception:
                    print(f"⚠️ Erro ao ler {f.name}\n")
            else:
                print(f"⚠️ {artefato}_ultimo.json não encontrado.\n")
    else:
        print("⚠️ Nenhum JSON encontrado em exports/insumos/json.\n")

# 🧩 Testa importações
print("🧩 Testando importação dos módulos de integração:")
modules = [
    "streamlit_app.utils.integration_ai_engine",
    "streamlit_app.utils.integration_insumos",
    "streamlit_app.utils.integration_dfd",
    "streamlit_app.utils.integration_etp",
    "streamlit_app.utils.integration_tr",
]

ok_count = 0
for mod in modules:
    try:
        importlib.import_module(mod)
        print(f"   ✅ {mod} importável.")
        ok_count += 1
    except Exception as e:
        print(f"   ❌ Falha ao importar {mod}: {e}")

if ok_count >= 4:
    print(f"\n✅ Estrutura detectada: SynapseNext v3 ({ok_count} módulos importáveis).")
else:
    print(f"\n❌ Estrutura incompleta ({ok_count}/5 módulos disponíveis).")

print("\n🔍 Diagnóstico concluído.\n")
