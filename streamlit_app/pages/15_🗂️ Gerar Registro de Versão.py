# -*- coding: utf-8 -*-
"""
🗂️ Gerar Registro de Versão – SynapseNext (vNext+)
==============================================================
Criação de registros de versão (cópias de auditoria) dos artefatos
institucionais – DFD, ETP, TR, Edital e Contrato.

Autor: Equipe Synapse.Engineer
Instituição: Secretaria de Administração e Abastecimento – TJSP
Versão: SAAB 5.0 (vNext+)
==============================================================
"""

import sys
import os
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

# Configuração de caminhos ANTES de importar streamlit
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)

# Import do Streamlit
import streamlit as st

# ==========================================================
# ⚙️ Configuração inicial (PRIMEIRO COMANDO ST)
# ==========================================================
st.set_page_config(
    page_title="🗂️ Gerar Registro de Versão – SynapseNext",
    layout="wide",
    page_icon="🗂️"
)

# ==========================================================
# 🔧 Imports institucionais
# ==========================================================
try:
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except Exception:
    aplicar_estilo_global = lambda: None
    exibir_cabecalho_padrao = lambda *a, **kw: None

aplicar_estilo_global()
exibir_cabecalho_padrao(
    "🗂️ Gerar Registro de Versão",
    "Crie cópias de auditoria (versões salvas) dos artefatos institucionais – SAAB 5.0"
)
st.divider()

# ==========================================================
# 📦 Caminhos institucionais
# ==========================================================
EXPORTS = Path("exports")
REGISTROS_DIR = EXPORTS / "snapshots"  # mantém compatibilidade técnica
REGISTROS_DIR.mkdir(parents=True, exist_ok=True)

ARTEFATOS = {
    "DFD": EXPORTS / "dfd_data.json",
    "ETP": EXPORTS / "etp_data.json",
    "TR": EXPORTS / "tr_data.json",
    "EDITAL": EXPORTS / "edital_data.json",
    "CONTRATO": EXPORTS / "contrato_data.json",
}

# ==========================================================
# 🔁 Funções auxiliares
# ==========================================================
def copiar_artefatos(destino: Path) -> list[Path]:
    destino.mkdir(parents=True, exist_ok=True)
    copiados = []
    for nome, caminho in ARTEFATOS.items():
        if caminho.exists():
            destino_arquivo = destino / f"{nome}_versao.json"
            shutil.copy2(caminho, destino_arquivo)
            copiados.append(destino_arquivo)
    return copiados

def compactar_registro(pasta: Path) -> Path:
    zip_path = pasta.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for arquivo in pasta.glob("*.json"):
            zf.write(arquivo, arcname=arquivo.name)
    return zip_path

# ==========================================================
# 🧩 Interface principal
# ==========================================================
st.subheader("1️⃣ O que faz esta função?")
st.markdown("""
Esta ferramenta permite **gerar registros de versão (cópias de auditoria)** dos artefatos:
**DFD**, **ETP**, **TR**, **Edital** e **Contrato**.

Esses registros são usados para:
- preservar versões oficiais de cada documento,
- realizar auditorias comparativas,
- gerar relatórios de coerência.

Todos os arquivos serão armazenados em:
`exports/snapshots/`
""")

st.divider()
st.subheader("2️⃣ Gerar registro de versão agora")

if st.button("🗂️ Gerar e salvar cópias de auditoria", type="primary", use_container_width=True):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta_registro = REGISTROS_DIR / f"registro_{ts}"
    pasta_registro.mkdir(parents=True, exist_ok=True)

    copiados = copiar_artefatos(pasta_registro)
    if not copiados:
        st.error("Nenhum artefato disponível para gerar registro de versão.")
        st.stop()

    st.success(f"✅ {len(copiados)} artefato(s) copiado(s) para auditoria.")
    for arq in copiados:
        st.write(f"- {arq.name}")

    zip_path = compactar_registro(pasta_registro)
    st.divider()
    with open(zip_path, "rb") as f:
        st.download_button(
            label="⬇️ Baixar pacote de registro (.zip)",
            data=f.read(),
            file_name=zip_path.name,
            mime="application/zip",
            use_container_width=True,
        )

    st.info(f"Registro salvo em `{pasta_registro}` e disponível para download.")

else:
    st.info("Clique no botão acima para gerar o registro de versão atual dos artefatos.")

# ==========================================================
# 📘 Rodapé institucional
# ==========================================================
st.markdown("---")
st.caption(
    f"SynapseNext • SAAB 5.0 – Tribunal de Justiça de São Paulo • "
    f"Secretaria de Administração e Abastecimento (SAAB)  \n"
    f"Versão institucional gerada em {datetime.now():%d/%m/%Y %H:%M}"
)
