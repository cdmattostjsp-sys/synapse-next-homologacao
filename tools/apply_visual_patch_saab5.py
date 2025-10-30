# -*- coding: utf-8 -*-
"""
apply_visual_patch_saab5.py
---------------------------------------------------------------
Patch de alinhamento visual SAAB 5.0 – SynapseNext
Autor: Synapse.Engineer
Instituição: Secretaria de Administração e Abastecimento – TJSP
Data: Novembro/2025
---------------------------------------------------------------
Função:
- Insere chamadas padronizadas de estilo institucional em todas
  as páginas do Streamlit.
- Garante consistência visual e rodapé unificado.
---------------------------------------------------------------
"""

import os
from pathlib import Path
from datetime import datetime

# Caminhos base
BASE_DIR = Path(__file__).resolve().parent
PAGES_DIR = BASE_DIR / "streamlit_app" / "pages"

# Trechos padrão a inserir
IMPORT_BLOCK = (
    "from utils.ui_style import aplicar_estilo_institucional, rodape_institucional\n"
    "aplicar_estilo_institucional()\n"
)

FOOTER_BLOCK = "rodape_institucional()\n"

def patch_page(file_path: Path):
    """Aplica o patch em uma única página Streamlit"""
    original = file_path.read_text(encoding="utf-8").splitlines()
    new_lines = []
    import_done = False
    footer_done = False

    for line in original:
        if "aplicar_estilo_institucional" in line:
            import_done = True
        if "rodape_institucional" in line:
            footer_done = True
        new_lines.append(line)

    # Inserir import block após blocos de import
    if not import_done:
        insert_at = 0
        for i, line in enumerate(new_lines):
            if line.startswith("st.set_page_config"):
                insert_at = i + 1
                break
        new_lines.insert(insert_at, IMPORT_BLOCK)

    # Inserir rodapé no final
    if not footer_done:
        new_lines.append("\n# ==========================================================")
        new_lines.append("# Rodapé institucional SAAB 5.0 (adicionado automaticamente)")
        new_lines.append("# ==========================================================")
        new_lines.append(FOOTER_BLOCK)

    # Backup
    backup_path = file_path.with_suffix(f".bak_{datetime.now():%Y%m%d_%H%M%S}")
    backup_path.write_text("\n".join(original), encoding="utf-8")

    # Sobrescrever o arquivo original
    file_path.write_text("\n".join(new_lines), encoding="utf-8")
    print(f"✅ Patch aplicado em: {file_path.name}")

def main():
    if not PAGES_DIR.exists():
        print("❌ Pasta 'streamlit_app/pages/' não encontrada.")
        return

    print(f"🔧 Iniciando alinhamento visual SAAB 5.0 em {PAGES_DIR}...")
    for py_file in sorted(PAGES_DIR.glob("*.py")):
        patch_page(py_file)

    print("\n🎯 Concluído com sucesso!")
    print("Todos os arquivos receberam o padrão de estilo institucional.")
    print("Backups criados automaticamente com extensão '.bak_YYYYMMDD_HHMMSS'.")

if __name__ == "__main__":
    main()
