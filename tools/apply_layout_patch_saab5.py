# ============================================================
# tools/apply_layout_patch_saab5.py
# ------------------------------------------------------------
# Patch institucional SAAB 5.0 – Padronização de layout e gráficos
# ------------------------------------------------------------
# Função: Inserir imports e ajustes visuais (layout_manager)
# nas páginas com gráficos do SynapseNext, sem alterar a lógica.
#
# Autor: Synapse.Engineer
# Data: 2025-10-30
# ============================================================

import os
import re

# ------------------------------------------------------------
# CONFIGURAÇÃO: Páginas que possuem gráficos
# ------------------------------------------------------------
TARGET_PAGES = [
    "10_💡 Análise de Desempenho.py",
    "11_📊 Painel de Governança.py",
    "12_📈 Painel Executivo.py",
    "09_⚠️ Alertas.py",
]

# ------------------------------------------------------------
# Padrões de inserção
# ------------------------------------------------------------
IMPORT_LINE = "from utils.layout_manager import ajustar_grafico, iniciar_secao\n"
AJUSTE_GRAFICO_SNIPPET = (
    "\n    # Aplicação de layout padrão SAAB 5.0\n"
    "    fig = ajustar_grafico(fig, titulo='Visualização Institucional')\n"
    "    st.plotly_chart(fig, use_container_width=True)\n"
)
SECAO_SNIPPET = "\n\niniciar_secao('Indicadores Institucionais', '📊')\n"


def patch_file(file_path):
    """Aplica o patch em um arquivo específico."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # 1️⃣ Inserir o import se ainda não existir
    if "layout_manager" not in content:
        match = re.search(r"import streamlit as st\s*\n", content)
        if match:
            pos = match.end()
            content = content[:pos] + IMPORT_LINE + content[pos:]
            modified = True

    # 2️⃣ Inserir seção padrão antes do primeiro gráfico
    if "iniciar_secao(" not in content and "st.plotly_chart" in content:
        first_plot = content.find("st.plotly_chart")
        if first_plot != -1:
            content = content[:first_plot] + SECAO_SNIPPET + content[first_plot:]
            modified = True

    # 3️⃣ Substituir exibição direta de gráfico por versão padronizada
    if "ajustar_grafico" not in content:
        content = re.sub(
            r"st\.plotly_chart\s*\(\s*fig\s*\)",
            AJUSTE_GRAFICO_SNIPPET.strip(),
            content,
        )
        modified = True

    # 4️⃣ Salvar backup e novo arquivo, se houve alterações
    if modified:
        backup_path = file_path + ".bak"
        os.rename(file_path, backup_path)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Patch aplicado em: {file_path}")
        print(f"💾 Backup criado em: {backup_path}")
    else:
        print(f"⚪ Nenhuma alteração necessária em: {file_path}")


def main():
    base_path = os.path.join("streamlit_app", "pages")
    print("🚀 Aplicando patch de layout SAAB 5.0...")
    print("-" * 70)

    for filename in TARGET_PAGES:
        path = os.path.join(base_path, filename)
        if os.path.exists(path):
            patch_file(path)
        else:
            print(f"⚠️ Página não encontrada: {path}")

    print("-" * 70)
    print("✅ Processo concluído. Execute o Streamlit para validar o novo layout.")


if __name__ == "__main__":
    main()
