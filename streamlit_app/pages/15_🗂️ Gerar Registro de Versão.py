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
from home_utils.sidebar_organizer import apply_sidebar_grouping

# ==========================================================
# ⚙️ Configuração inicial (PRIMEIRO COMANDO ST)
# ==========================================================
st.set_page_config(
    page_title="🗂️ Gerar Registro de Versão – SynapseNext",
    layout="wide",
    page_icon="🗂️"
)
apply_sidebar_grouping()

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
REGISTROS_DIR = EXPORTS / "versoes"  # estrutura unificada e clara
REGISTROS_DIR.mkdir(parents=True, exist_ok=True)

ARTEFATOS = {
    "DFD": EXPORTS / "dfd_data.json",
    "ETP": EXPORTS / "etp_data.json",
    "TR": EXPORTS / "tr_data.json",
    "EDITAL": EXPORTS / "edital_data.json",
    "CONTRATO": EXPORTS / "contrato_data.json",
}

# Versão do sistema
VERSAO_SISTEMA = "v2025.1-homolog"

# ==========================================================
# 🔁 Funções auxiliares
# ==========================================================
def copiar_artefatos(destino: Path) -> list[Path]:
    """Copia artefatos existentes para o diretório de destino."""
    destino.mkdir(parents=True, exist_ok=True)
    copiados = []
    metadados_artefatos = []
    
    for nome, caminho in ARTEFATOS.items():
        if caminho.exists():
            destino_arquivo = destino / f"{nome}_versao.json"
            shutil.copy2(caminho, destino_arquivo)
            copiados.append(destino_arquivo)
            
            # Coletar metadados do artefato
            stat = caminho.stat()
            metadados_artefatos.append({
                "nome": nome,
                "arquivo": caminho.name,
                "tamanho_bytes": stat.st_size,
                "modificado_em": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    
    return copiados, metadados_artefatos

def criar_manifesto(destino: Path, metadados_artefatos: list, timestamp: str) -> Path:
    """Cria arquivo manifesto.json com metadados do registro."""
    manifesto = {
        "versao_sistema": VERSAO_SISTEMA,
        "data_criacao": datetime.now().isoformat(),
        "timestamp": timestamp,
        "total_artefatos": len(metadados_artefatos),
        "artefatos": metadados_artefatos,
        "instituicao": "TJSP - Tribunal de Justiça de São Paulo",
        "secretaria": "SAAB - Secretaria de Administração e Abastecimento",
        "tipo_registro": "snapshot_institucional"
    }
    
    manifesto_path = destino / "manifesto.json"
    with open(manifesto_path, "w", encoding="utf-8") as f:
        json.dump(manifesto, f, indent=2, ensure_ascii=False)
    
    return manifesto_path

def compactar_registro(pasta: Path) -> Path:
    """Compacta registro completo (artefatos + manifesto) em arquivo .zip."""
    zip_path = pasta.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for arquivo in pasta.glob("*.json"):
            zf.write(arquivo, arcname=arquivo.name)
    return zip_path

def listar_registros_existentes() -> list:
    """Lista todos os registros de versão existentes."""
    registros = []
    for item in sorted(REGISTROS_DIR.glob("registro_*"), reverse=True):
        if item.is_dir():
            manifesto = item / "manifesto.json"
            if manifesto.exists():
                with open(manifesto, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                    registros.append({
                        "pasta": item.name,
                        "data": meta.get("data_criacao", "N/A"),
                        "total_artefatos": meta.get("total_artefatos", 0),
                        "versao": meta.get("versao_sistema", "N/A")
                    })
            else:
                # Registro sem manifesto (legado)
                arquivos = list(item.glob("*.json"))
                registros.append({
                    "pasta": item.name,
                    "data": "N/A",
                    "total_artefatos": len(arquivos),
                    "versao": "legado"
                })
    return registros

# ==========================================================
# 🧩 Interface principal
# ==========================================================
st.subheader("1️⃣ O que faz esta função?")
st.markdown("""
Esta ferramenta permite **gerar registros de versão (snapshots institucionais)** dos artefatos:
**DFD**, **ETP**, **TR**, **Edital** e **Contrato**.

**Funcionalidades:**
- 📦 Preservar versões oficiais de cada documento processado
- 🔍 Realizar auditorias comparativas entre versões
- 📊 Gerar relatórios de coerência e evolução temporal
- 💾 Backup institucional com metadados completos

**Armazenamento:** `exports/versoes/registro_YYYYMMDD_HHMMSS/`
""")

# Exibir artefatos disponíveis
st.divider()
st.subheader("📄 Artefatos Disponíveis")
col1, col2, col3, col4, col5 = st.columns(5)
artefatos_disponiveis = 0
for idx, (nome, caminho) in enumerate(ARTEFATOS.items()):
    with [col1, col2, col3, col4, col5][idx]:
        if caminho.exists():
            size_kb = caminho.stat().st_size / 1024
            st.metric(nome, f"{size_kb:.1f} KB", "✅ Disponível")
            artefatos_disponiveis += 1
        else:
            st.metric(nome, "—", "❌ Ausente")

st.divider()
st.subheader("2️⃣ Gerar Novo Registro de Versão")

if artefatos_disponiveis == 0:
    st.warning("⚠️ Nenhum artefato disponível. Processe documentos antes de gerar registro.")
else:
    if st.button("🗂️ Gerar registro de versão agora", type="primary", use_container_width=True):
        with st.spinner("Gerando registro de versão..."):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            pasta_registro = REGISTROS_DIR / f"registro_{ts}"
            pasta_registro.mkdir(parents=True, exist_ok=True)

            # Copiar artefatos
            copiados, metadados_artefatos = copiar_artefatos(pasta_registro)
            
            if not copiados:
                st.error("Nenhum artefato disponível para gerar registro de versão.")
                st.stop()

            # Criar manifesto
            manifesto_path = criar_manifesto(pasta_registro, metadados_artefatos, ts)
            
            # Compactar
            zip_path = compactar_registro(pasta_registro)
            zip_size_kb = zip_path.stat().st_size / 1024

        st.success(f"✅ Registro criado com sucesso: `{pasta_registro.name}`")
        
        # Exibir detalhes
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Artefatos", len(copiados))
        col_b.metric("Tamanho ZIP", f"{zip_size_kb:.1f} KB")
        col_c.metric("Versão", VERSAO_SISTEMA)
        
        with st.expander("📋 Ver detalhes do registro", expanded=False):
            for meta in metadados_artefatos:
                st.markdown(f"**{meta['nome']}**: {meta['tamanho_bytes']} bytes")
        
        st.divider()
        
        # Download
        with open(zip_path, "rb") as f:
            st.download_button(
                label=f"⬇️ Baixar {zip_path.name}",
                data=f.read(),
                file_name=zip_path.name,
                mime="application/zip",
                use_container_width=True,
            )
        
        st.info(f"💾 Registro salvo em: `exports/versoes/{pasta_registro.name}`")

# Histórico de registros
st.divider()
st.subheader("3️⃣ Histórico de Registros")

registros = listar_registros_existentes()
if registros:
    st.markdown(f"**Total de registros:** {len(registros)}")
    
    # Tabela de registros
    import pandas as pd
    df_registros = pd.DataFrame(registros)
    st.dataframe(
        df_registros,
        column_config={
            "pasta": "Identificador",
            "data": "Data de Criação",
            "total_artefatos": "Artefatos",
            "versao": "Versão do Sistema"
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("📂 Nenhum registro encontrado. Crie o primeiro registro acima.")

# ==========================================================
# 📘 Rodapé institucional
# ==========================================================
st.markdown("---")
st.caption(
    f"SynapseNext • SAAB 5.0 – Tribunal de Justiça de São Paulo • "
    f"Secretaria de Administração e Abastecimento (SAAB)  \n"
    f"Versão institucional gerada em {datetime.now():%d/%m/%Y %H:%M}"
)
