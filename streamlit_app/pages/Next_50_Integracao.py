# streamlit_app/pages/Next_50_Integracao.py
# ==========================================================
# SynapseNext – Fase Brasília
# Placeholders de integração (SharePoint / OneDrive)
# ==========================================================

import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# ==========================================================
# Correção de caminho robusta
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
# Configuração da página
# ==========================================================
st.set_page_config(page_title="SynapseNext – Integração", layout="wide")

st.title("Integração Institucional – Placeholders (Fase Brasília)")
st.caption(
    "Simulação de conectividade com SharePoint e OneDrive, para futura integração via Microsoft Graph."
)

st.divider()
st.subheader("1️⃣ Enviar arquivo para SharePoint (simulado)")

# ==========================================================
# Bloco 1 – Envio para SharePoint
# ==========================================================
base = Path(__file__).resolve().parents[2]
rascunhos_dir = base / "exports" / "rascunhos"
rascunhos_dir.mkdir(parents=True, exist_ok=True)

arquivos = sorted(rascunhos_dir.glob("*.docx"), reverse=True)
if not arquivos:
    st.info("Nenhum arquivo encontrado em `exports/rascunhos`.")
else:
    arquivo_escolhido = st.selectbox("Selecione o arquivo para envio:", [a.name for a in arquivos])
    destino = st.text_input("Destino (SharePoint Site / Pasta):", placeholder="Ex.: /sites/SynapseNext/DocumentosGerados")

    if st.button("📤 Enviar para SharePoint"):
        response = upload_to_sharepoint(arquivo_escolhido, destino)
        save_integration_log("upload_sharepoint", response)
        st.success(f"✅ Simulação concluída: {response['mensagem']}")

st.divider()
st.subheader("2️⃣ Baixar arquivo do OneDrive (simulado)")

# ==========================================================
# Bloco 2 – Download do OneDrive
# ==========================================================
nome = st.text_input("Nome do arquivo no OneDrive:", placeholder="Ex.: Contrato_20251019.docx")
if st.button("📥 Simular Download"):
    response = download_from_onedrive(nome)
    save_integration_log("download_onedrive", response)
    st.info(f"📄 {response['mensagem']}")
