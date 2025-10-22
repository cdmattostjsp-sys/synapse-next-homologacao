import os
import fitz  # PyMuPDF
import docx2txt
import streamlit as st
from openai import OpenAI


# ==========================================================
# 🧠 Função de inicialização híbrida do cliente OpenAI
# ==========================================================
def get_openai_client():
    """
    Inicializa o cliente OpenAI de forma compatível com múltiplos formatos de secrets.
    Aceita:
      - [openai] api_key = "..."
      - openai.api_key = "..."
      - OPENAI_API_KEY = "..."
    """
    secrets = dict(st.secrets)

    # tenta múltiplos formatos
    api_key = (
        secrets.get("openai", {}).get("api_key")
        if isinstance(secrets.get("openai"), dict)
        else None
    )
    api_key = api_key or secrets.get("openai.api_key") or secrets.get("OPENAI_API_KEY")
    model = (
        secrets.get("openai", {}).get("model")
        if isinstance(secrets.get("openai"), dict)
        else None
    )
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
# 📂 Função: salvar insumo enviado
# ==========================================================
def salvar_insumo(file, artefato):
    """Salva o arquivo enviado e retorna o caminho."""
    if not file:
        return None

    upload_dir = f"./uploads/{artefato}"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.name)

    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    return file_path


# ==========================================================
# 📄 Função: extrair texto de documentos
# ==========================================================
def extrair_texto(caminho_arquivo):
    """Lê e extrai texto de PDF, DOCX ou TXT."""
    try:
        if caminho_arquivo.endswith(".pdf"):
            texto = ""
            with fitz.open(caminho_arquivo) as doc:
                for pagina in doc:
                    texto += pagina.get_text()
            return texto

        elif caminho_arquivo.endswith(".docx"):
            return docx2txt.process(caminho_arquivo)

        elif caminho_arquivo.endswith(".txt"):
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                return f.read()

        else:
            return "Formato de arquivo não suportado."

    except Exception as e:
        return f"Erro ao extrair texto: {e}"


# ==========================================================
# 🤖 Função: processar insumo via IA
# ==========================================================
def process_insumo_text(texto):
    """Analisa o texto do insumo via IA e retorna campos estruturados."""
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
        Retorne um JSON estruturado com os seguintes campos:
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
                {"role": "system", "content": "Você é um assistente que organiza informações de contratações públicas."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        conteudo = resposta.choices[0].message.content.strip()
        return {"campos_ai": conteudo, "erro": None}

    except Exception as e:
        return {
            "erro": f"Erro ao processar o texto via IA: {e}",
            "campos_ai": {},
            "observacao": "Verifique se há créditos disponíveis na conta OpenAI.",
        }


# ==========================================================
# 📋 Função: listar insumos existentes
# ==========================================================
def listar_insumos():
    """Lista arquivos de insumos já enviados."""
    uploads_dir = "./uploads"
    if not os.path.exists(uploads_dir):
        return []
    arquivos = []
    for root, _, files in os.walk(uploads_dir):
        for file in files:
            arquivos.append(os.path.join(root, file))
    return arquivos
