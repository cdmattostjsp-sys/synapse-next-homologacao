# ==============================
# utils/integration_insumos.py
# SynapseNext – SAAB / TJSP
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

def get_openai_client() -> tuple[Optional[OpenAI], str]:
    """Inicializa o cliente OpenAI de forma resiliente e compatível com múltiplos formatos de secrets."""
    secrets = st.secrets
    api_key = None

    openai_block = secrets.get("openai")

    # Caso 1 — formato TOML correto ([openai])
    if isinstance(openai_block, dict):
        api_key = openai_block.get("api_key")

    # Caso 2 — formato incorreto (string convertida indevidamente)
    elif isinstance(openai_block, str) and "api_key" in openai_block:
        import re
        match = re.search(r"api_key['\"]*:\s*['\"]([^'\"]+)['\"]", openai_block)
        if match:
            api_key = match.group(1)

    # Caso 3 — variáveis globais
    api_key = api_key or secrets.get("openai.api_key") or secrets.get("OPENAI_API_KEY")
    model = (secrets.get("openai", {}).get("model")
             if isinstance(secrets.get("openai"), dict)
             else None) or secrets.get("OPENAI_MODEL", "gpt-4o")

    # Se a chave não estiver disponível, apenas alerta — não quebra o app
    if not api_key:
        st.warning("⚠️ A chave OpenAI não foi encontrada. O processamento IA está temporariamente desativado.")
        return None, model

    try:
        client = OpenAI(api_key=api_key)
        return client, model
    except Exception as e:
        st.error(f"Erro ao inicializar cliente OpenAI: {e}")
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
                {
                    "role": "system",
                    "content": "Você organiza informações de contratações públicas e SEMPRE devolve JSON válido.",
                },
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
        return [
            os.path.join(pasta, f)
            for f in os.listdir(pasta)
            if os.path.isfile(os.path.join(pasta, f))
        ]

    # lista recursiva
    arquivos: List[str] = []
    for root, _, files in os.walk(base):
        for file in files:
            arquivos.append(os.path.join(root, file))
    return arquivos
