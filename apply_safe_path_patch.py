# -*- coding: utf-8 -*-
"""
apply_safe_path_patch.py – Patch idempotente para compatibilidade de import.
- Substitui sys.path.append(...) “bruto” por versão segura (com if BASE_PATH not in sys.path).
- Faz backup dos arquivos alterados em exports/backups/pages/.
- Só altera arquivos que contenham um dos padrões-alvo.
"""

import os
import re
from datetime import datetime

PAGES_DIR = "streamlit_app/pages"
BACKUP_DIR = "exports/backups/pages"

SAFE_BLOCK = (
    "import sys, os\n"
    "BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), \"../../\"))\n"
    "if BASE_PATH not in sys.path:\n"
    "    sys.path.append(BASE_PATH)\n"
)

# Padrões antigos que queremos normalizar
PATTERNS = [
    r"sys\.path\.append\(.+?__file__.+?\)\)",   # genérico com __file__
    r"sys\.path\.append\(.+?../../.+?\)",       # genérico com ../../
]

def normalize(content: str) -> str:
    # Já está seguro?
    if "if BASE_PATH not in sys.path" in content:
        return content

    # Local para injetar: após comentários iniciais ou logo no topo
    lines = content.splitlines()
    insert_at = 0
    # se primeira linha é coding header, insere algumas linhas depois
    if lines and lines[0].startswith("# -*- coding:"):
        insert_at = 2

    # Remover blocos antigos que batam com os padrões
    new_lines = []
    skip_next = False
    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
        if any(re.search(p, line) for p in PATTERNS):
            # pula esta linha (e não tenta ser agressivo com múltiplas linhas)
            continue
        new_lines.append(line)

    # Injetar bloco seguro no topo calculado
    new_lines.insert(insert_at, SAFE_BLOCK.strip())
    return "\n".join(new_lines)

def patch_file(path: str) -> bool:
    with open(path, "r", encoding="utf-8") as f:
        original = f.read()
    patched = normalize(original)
    if patched == original:
        return False

    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_name = f"{os.path.basename(path)}.bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(original)

    with open(path, "w", encoding="utf-8") as f:
        f.write(patched)

    print(f"✅ Normalizado: {os.path.basename(path)}  (backup: {backup_name})")
    return True

if __name__ == "__main__":
    changed = 0
    for name in sorted(os.listdir(PAGES_DIR)):
        if not name.endswith(".py"):
            continue
        path = os.path.join(PAGES_DIR, name)
        if patch_file(path):
            changed += 1
    if changed == 0:
        print("🟢 Nenhuma alteração necessária – todas as páginas já estão seguras/idempotentes.")
    else:
        print(f"🏁 Patch aplicado com sucesso em {changed} arquivo(s).")
