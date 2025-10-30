# -*- coding: utf-8 -*-
"""
apply_path_patch.py – Atualizador institucional
Adiciona o bloco sys.path.append() no topo das páginas Streamlit.
Compatível com arquitetura SynapseNext vNext (TJSP/SAAB).
"""

import os

PAGES_DIR = "streamlit_app/pages"
PATCH_BLOCK = (
    "import sys, os\n"
    "sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))\n\n"
)

def aplicar_patch_em_pagina(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Verifica se já tem o bloco
    if "sys.path.append" in content:
        print(f"🟡 Já compatível: {os.path.basename(path)}")
        return

    # Insere o bloco logo após o cabeçalho de codificação
    linhas = content.splitlines()
    if linhas and linhas[0].startswith("# -*- coding:"):
        linhas.insert(2, PATCH_BLOCK.strip())
    else:
        linhas.insert(0, PATCH_BLOCK.strip())

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

    print(f"✅ Corrigido: {os.path.basename(path)}")


if __name__ == "__main__":
    for nome_arquivo in os.listdir(PAGES_DIR):
        if nome_arquivo.endswith(".py"):
            aplicar_patch_em_pagina(os.path.join(PAGES_DIR, nome_arquivo))
    print("\n🏁 Patch de compatibilidade aplicado com sucesso.")
