import os
import re
import shutil
from datetime import datetime
from pathlib import Path

# === SynapseNext v3 – Stabilization Pipeline (TJSP / SAAB) ===
# Autor: Synapse.Engineer (GPT-5)
# Propósito:
# 1️⃣ Corrigir imports antigos (from utils. → from streamlit_app.utils.)
# 2️⃣ Criar backup antes de qualquer modificação
# 3️⃣ Verificar estrutura e presença de arquivos essenciais
# 4️⃣ Exibir relatório técnico completo sem apagar nada

BASE_DIR = Path("/workspaces/synapse-next")
PAGES_DIR = BASE_DIR / "streamlit_app" / "pages"
UTILS_DIR = BASE_DIR / "streamlit_app" / "utils"
BACKUP_DIR = BASE_DIR / "backups" / datetime.now().strftime("%Y%m%d_%H%M%S")

os.makedirs(BACKUP_DIR, exist_ok=True)

print("\n🧠 === SYNAPSENEXT v3 – STABILIZATION PIPELINE ===\n")
print(f"📂 Diretório base: {BASE_DIR}")
print(f"📁 Páginas: {PAGES_DIR}")
print(f"📁 Utils: {UTILS_DIR}")
print(f"💾 Backups: {BACKUP_DIR}\n")

def fix_imports_in_file(filepath: Path):
    """Corrige imports antigos e cria backup automático."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    original_content = content

    content = re.sub(r"from\s+utils\.", "from streamlit_app.utils.", content)
    content = re.sub(r"import\s+utils\.", "import streamlit_app.utils.", content)
    content = re.sub(r"from\s+integration_", "from streamlit_app.utils.integration_", content)

    if content != original_content:
        backup_path = BACKUP_DIR / filepath.name
        shutil.copy(filepath, backup_path)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Corrigido: {filepath.name} (backup em {backup_path})")
    else:
        print(f"⚙️ Sem alterações: {filepath.name}")

# 1️⃣ Corrige imports em streamlit_app/pages/
if PAGES_DIR.exists():
    print("🔍 Verificando imports em páginas...")
    for file in sorted(PAGES_DIR.glob("*.py")):
        fix_imports_in_file(file)
else:
    print("⚠️ Diretório de páginas não encontrado!")

# 2️⃣ Corrige imports em streamlit_app/utils/
if UTILS_DIR.exists():
    print("\n🔍 Verificando imports em utils...")
    for file in sorted(UTILS_DIR.glob("*.py")):
        fix_imports_in_file(file)
else:
    print("⚠️ Diretório de utils não encontrado!")

# 3️⃣ Verifica estrutura principal
print("\n📦 Estrutura principal:")
checks = {
    "streamlit_app/pages": PAGES_DIR.exists(),
    "streamlit_app/utils": UTILS_DIR.exists(),
    ".streamlit/secrets.toml": (BASE_DIR / ".streamlit" / "secrets.toml").exists(),
}
for name, ok in checks.items():
    print(f" {'✅' if ok else '❌'} {name}")

# 4️⃣ Lista módulos de integração
print("\n📦 Módulos de integração detectados em streamlit_app/utils:")
if UTILS_DIR.exists():
    for file in sorted(UTILS_DIR.glob("integration_*.py")):
        print(f"   • {file.name}")
else:
    print("⚠️ Nenhum módulo encontrado.")

print("\n🧩 Estabilização concluída com sucesso.")
print("   → Execute agora o Streamlit para validar a interface:")
print("     streamlit run streamlit_app/Home.py\n")
