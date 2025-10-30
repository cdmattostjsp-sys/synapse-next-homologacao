# ==========================================================
# 🔗 SynapseNext – Integração Institucional
# Secretaria de Administração e Abastecimento – SAAB 5.0
# ==========================================================

import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# ==========================================================
# 🔧 Ajuste de caminhos e imports
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.integration_placeholders import upload_to_sharepoint, download_from_onedrive, save_integration_log
except Exception as e:
    st.error(f"❌ Erro ao importar módulos de integração: {e}")
    st.stop()

# ==========================================================
# ⚙️ Configuração da página
# ==========================================================
st.set_page_config(page_title="SynapseNext – Integração Institucional", layout="wide", page_icon="🔗")

# ==========================================================
# 🎨 Estilo institucional padronizado
# ==========================================================
try:
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except Exception:
    aplicar_estilo_global = lambda: None
    exibir_cabecalho_padrao = lambda *a, **kw: None

aplicar_estilo_global()

# ==========================================================
# 🏛️ Cabeçalho institucional padronizado
# ==========================================================
exibir_cabecalho_padrao(
    "Integração Institucional",
    "Simulação de conectividade com SharePoint e OneDrive – Fase Brasília (vNext)"
)
st.divider()

# ==========================================================
# 1️⃣ Enviar arquivo para SharePoint (simulado)
# ==========================================================
st.subheader("1️⃣ Enviar arquivo para SharePoint (simulado)")

base = Path(__file__).resolve().parents[2]
rascunhos_dir = base / "exports" / "rascunhos"
rascunhos_dir.mkdir(parents=True, exist_ok=True)

arquivos = sorted(rascunhos_dir.glob("*.docx"), reverse=True)

if not arquivos:
    st.info("📂 Nenhum arquivo encontrado em `exports/rascunhos`.")
else:
    arquivo_escolhido = st.selectbox(
        "Selecione o arquivo para envio:",
        [a.name for a in arquivos],
        index=0,
        help="Selecione um documento gerado (DFD, ETP, TR, Edital ou Contrato)."
    )
    destino = st.text_input(
        "Destino (SharePoint Site / Pasta):",
        placeholder="/sites/SynapseNext/DocumentosGerados"
    )

    if st.button("📤 Simular envio para SharePoint", use_container_width=True):
        response = upload_to_sharepoint(arquivo_escolhido, destino)
        save_integration_log("upload_sharepoint", response)
        st.success(f"✅ Simulação concluída: {response['mensagem']}")
        st.caption("O arquivo permanece localmente armazenado; esta função representa o futuro conector via Microsoft Graph API.")

# ==========================================================
# 2️⃣ Baixar arquivo do OneDrive (simulado)
# ==========================================================
st.divider()
st.subheader("2️⃣ Baixar arquivo do OneDrive (simulado)")

nome = st.text_input("Nome do arquivo no OneDrive:", placeholder="Ex.: Contrato_20251019.docx")

if st.button("📥 Simular Download", use_container_width=True):
    response = download_from_onedrive(nome)
    save_integration_log("download_onedrive", response)
    st.info(f"📄 {response['mensagem']}")
    st.caption("A operação representa o fluxo inverso de integração – recuperação de arquivos no repositório institucional.")

# ==========================================================
# 3️⃣ Logs e Auditoria das Simulações
# ==========================================================
st.divider()
st.subheader("3️⃣ Logs de Integração")

logs_dir = base / "exports" / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

log_files = sorted(logs_dir.glob("log_integration_*.json"), reverse=True)
if not log_files:
    st.info("🪶 Nenhum log de integração encontrado.")
else:
    with st.expander("📘 Visualizar logs recentes", expanded=False):
        for log_file in log_files[:5]:
            st.markdown(f"**{log_file.name}**")
            with open(log_file, "r", encoding="utf-8") as f:
                st.json(f.read())

# ==========================================================
# 📘 Rodapé institucional simplificado
# ==========================================================
st.markdown("---")
st.caption(
    f"SynapseNext – SAAB 5.0 • Tribunal de Justiça de São Paulo • Secretaria de Administração e Abastecimento (SAAB)  \n"
    f"Simulação Institucional – Gerado em {datetime.now():%d/%m/%Y %H:%M}"
)
