# ==============================
# utils/integration_insumos.py
# ==============================
import os
import fitz  # PyMuPDF
import docx2txt
import streamlit as st
from openai import OpenAI
from typing import Dict, Any, List, Optional

# ==========================================================
# 🧠 Inicialização resiliente do cliente OpenAI
# ==========================================================

def get_openai_client():
    """
    Inicializa o cliente OpenAI de forma compatível com múltiplos formatos de secrets.
    Aceita:
      - [openai] api_key = "..."
      - openai.api_key = "..."
      - OPENAI_API_KEY = "..."
      - [openai] model = "gpt-4o-mini" (opcional, com fallback)
    Retorna: (client | None, model_str)
    """
    secrets = dict(st.secrets) if hasattr(st, "secrets") else {}

    api_key = None
    if isinstance(secrets.get("openai"), dict):
        api_key = secrets.get("openai", {}).get("api_key")
    api_key = api_key or secrets.get("openai.api_key") or secrets.get("OPENAI_API_KEY")

    model = None
    if isinstance(secrets.get("openai"), dict):
        model = secrets.get("openai", {}).get("model")
    model = model or secrets.get("openai.model") or "gpt-4o-mini"

    if not api_key:
        st.warning("⚠️ A chave OpenAI não foi encontrada. Verifique o painel de Secrets.")
        return None, model

    try:
        client = OpenAI(api_key=api_key)
        return client, model
    except Exception as e:
        st.error(f"Erro ao inicializar o cliente OpenAI: {e}")
        return None, model


# ==========================================================
# 📂 Salvar insumo
# ==========================================================

def salvar_insumo(file, artefato: str) -> Optional[str]:
    """Salva o arquivo enviado na pasta ./uploads/<artefato> e retorna o caminho."""
    if not file:
        return None

    artefato = (artefato or "Diversos").upper()
    upload_dir = os.path.join("./uploads", artefato)
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.name)

    # file may be a SpooledTemporaryFile; use getbuffer when available
    try:
        data = file.getbuffer()
    except Exception:
        file.seek(0)
        data = file.read()

    with open(file_path, "wb") as f:
        f.write(data)

    return file_path


# ==========================================================
# 📄 Extração de texto
# ==========================================================

def extrair_texto(caminho_arquivo: str) -> str:
    """Extrai texto de PDF, DOCX ou TXT. Retorna string (ou mensagem de erro)."""
    try:
        lower = caminho_arquivo.lower()
        if lower.endswith(".pdf"):
            texto = []
            with fitz.open(caminho_arquivo) as doc:
                for pagina in doc:
                    texto.append(pagina.get_text())
            return "".join(texto)

        if lower.endswith(".docx"):
            return docx2txt.process(caminho_arquivo)

        if lower.endswith(".txt"):
            with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        return "Formato de arquivo não suportado."

    except Exception as e:
        return f"Erro ao extrair texto: {e}"


# ==========================================================
# 🤖 Processamento IA
# ==========================================================

def process_insumo_text(texto: str) -> Dict[str, Any]:
    """Analisa o texto via IA e retorna um dicionário com os campos estruturados (ou erro)."""
    client, model = get_openai_client()

    if not client:
        return {
            "erro": "⚠️ A chave OpenAI não foi encontrada ou é inválida.",
            "campos_ai": {},
            "observacao": "Upload e histórico continuam funcionando normalmente.",
        }

    try:
        prompt = f"""
        Você é um assistente técnico do Tribunal de Justiça de São Paulo.
        Extraia do texto abaixo as informações relevantes para preencher um Documento de Formalização da Demanda (DFD).
        Retorne um JSON estritamente válido com os campos:
        {{
            "unidade_solicitante": "",
            "responsavel": "",
            "objeto": "",
            "justificativa": "",
            "quantidade": "",
            "urgencia": "",
            "riscos": "",
            "alinhamento_planejamento": ""
        }}
        Texto-base:
        {texto}
        """

        resposta = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você organiza informações de contratações públicas e SEMPRE devolve JSON válido."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )

        conteudo = resposta.choices[0].message.content.strip()
        return {"campos_ai": conteudo, "erro": None}

    except Exception as e:
        return {
            "erro": f"Erro ao processar o texto via IA: {e}",
            "campos_ai": {},
            "observacao": "Verifique créditos da conta OpenAI e o modelo em st.secrets.",
        }


# ==========================================================
# 📋 Listagem de insumos
# ==========================================================

def listar_insumos(artefato: Optional[str] = None) -> List[str]:
    """
    Lista arquivos de insumos já enviados.
    - Sem parâmetro: lista todos.
    - Com artefato: lista apenas ./uploads/<ARTEFATO>
    """
    base = "./uploads"
    if not os.path.exists(base):
        return []

    if artefato and artefato.upper() != "TODOS":
        pasta = os.path.join(base, artefato.upper())
        if not os.path.exists(pasta):
            return []
        return [os.path.join(pasta, f) for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]

    # lista recursiva
    arquivos: List[str] = []
    for root, _, files in os.walk(base):
        for file in files:
            arquivos.append(os.path.join(root, file))
    return arquivos


# ==============================
# pages/01_🔧 Insumos.py
# ==============================

import streamlit as st
from datetime import datetime
from io import BytesIO
from pathlib import Path
import sys
import docx2txt

# Configuração da página deve vir antes de qualquer renderização
st.set_page_config(page_title="🔧 Insumos", layout="wide")

# ==========================================================
# 🔧 Correção de path (suporta execução em diferentes layouts de pasta)
# ==========================================================
current_dir = Path(__file__).resolve()
# Tenta localizar /utils a partir de diferentes profundidades
candidatos_utils = [current_dir.parent.parent / "utils", current_dir.parent / "utils", Path.cwd() / "utils"]
for cand in candidatos_utils:
    if cand.exists() and str(cand) not in sys.path:
        sys.path.insert(0, str(cand))

try:
    from integration_insumos import salvar_insumo, listar_insumos, process_insumo_text
except Exception:
    # Fallback quando projeto estiver estruturado como pacote utils.integration_insumos
    sys.path.insert(0, str((current_dir.parent.parent)))
    from utils.integration_insumos import salvar_insumo, listar_insumos, process_insumo_text  # type: ignore

# ==========================================================
# 🏛️ Cabeçalho
# ==========================================================
st.markdown(
    """
    <div style='padding: 1.2rem 0; text-align: center;'>
        <h1 style='color:#800000; margin-bottom:0.3rem;'>🔧 Upload de Insumos Institucionais</h1>
        <p style='font-size:1.05rem; color:#444;'>Integração inteligente entre artefatos e dados do SynapseNext</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
O módulo **INSUMOS** permite anexar documentos institucionais (DFD, ETP, TR, Edital, Contrato, etc.)  
que servirão de base para os artefatos gerados automaticamente pelo SynapseNext.  
Cada upload é registrado e o conteúdo pode ser processado semanticamente pela IA  
para preenchimento inteligente dos formulários correspondentes.
"""
)

# ==========================================================
# 📂 Upload de documento
# ==========================================================
st.divider()
st.subheader("📎 Enviar novo insumo")

col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    artefato = st.selectbox("Artefato relacionado", ["DFD", "ETP", "TR", "EDITAL", "CONTRATO"])
with col2:
    descricao = st.text_input("Descrição / Observação", placeholder="Ex: Estudo técnico preliminar revisado")
with col3:
    usuario = st.text_input("Nome do remetente", placeholder="Ex: Carlos Mattos")

arquivo = st.file_uploader("Selecione o arquivo (DOCX, PDF, TXT, etc.)", type=["docx", "pdf", "txt"])

if arquivo and st.button("📤 Enviar insumo"):
    with st.spinner("Salvando e processando o documento..."):
        # 💾 Salvar no diretório do artefato selecionado (corrigido)
        caminho_salvo = salvar_insumo(arquivo, artefato)
        st.success(f"Insumo '{arquivo.name}' salvo com sucesso em {caminho_salvo}")

        # 🔍 Extração de texto (usa buffer para evitar exaustão do stream)
        texto_extraido = ""
        try:
            nome = arquivo.name.lower()
            arquivo.seek(0)
            dados = arquivo.read()

            if nome.endswith(".pdf"):
                pdf = fitz.open(stream=dados, filetype="pdf")
                texto_extraido = "".join(page.get_text() for page in pdf)

            elif nome.endswith(".docx"):
                texto_extraido = docx2txt.process(BytesIO(dados))

            elif nome.endswith(".txt"):
                texto_extraido = dados.decode("utf-8", errors="ignore")
        except Exception as e:
            st.error(f"Erro ao extrair texto do arquivo: {e}")

        # 🤖 Processamento semântico com IA
        campos_ai = {}
        if texto_extraido.strip():
            st.info("IA processando o insumo e identificando campos relevantes...")
            try:
                dados_inferidos = process_insumo_text(texto_extraido)
                st.success(f"✅ Insumo '{arquivo.name}' registrado e processado com sucesso.")
                st.json(dados_inferidos)
                if isinstance(dados_inferidos, dict):
                    campos_ai = dados_inferidos
            except Exception as e:
                st.error(f"Erro no processamento IA: {e}")
        else:
            st.warning("⚠️ Não foi possível extrair texto legível do arquivo enviado.")

        # 🧠 Persistência para páginas seguintes (DFD/TR)
        st.session_state["last_insumo"] = {
            "nome": arquivo.name,
            "artefato": artefato,
            "conteudo": (texto_extraido or "")[:100000],
            "campos_ai": campos_ai,
            "usuario": usuario,
            "descricao": descricao,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        st.info("📎 Insumo ativo armazenado na sessão e disponível para o DFD/TR.")

# ==========================================================
# 🗂️ Histórico de uploads
# ==========================================================
st.divider()
st.subheader("🗂️ Histórico de Insumos Enviados")

artefato_hist = st.selectbox("Filtrar por artefato", ["Todos", "DFD", "ETP", "TR", "EDITAL", "CONTRATO"])

if artefato_hist == "Todos":
    # agrupa por pasta de artefato
    for tipo in ["DFD", "ETP", "TR", "EDITAL", "CONTRATO"]:
        arquivos = listar_insumos(tipo)
        st.markdown(f"#### 📘 {tipo} ({len(arquivos)} arquivos)")
        if arquivos:
            st.write(arquivos)
        else:
            st.caption("— sem arquivos —")
else:
    arquivos = listar_insumos(artefato_hist)
    st.markdown(f"#### 📘 {artefato_hist} ({len(arquivos)} arquivos)")
    if arquivos:
        st.write(arquivos)
    else:
        st.info("Nenhum insumo encontrado para o artefato selecionado.")
