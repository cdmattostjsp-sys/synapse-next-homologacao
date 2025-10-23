# ==============================
# utils/integration_insumos.py
# SynapseNext – SAAB / TJSP
# ==============================

import os
import re
import json
import fitz  # PyMuPDF
import docx2txt
import streamlit as st
from openai import OpenAI
from typing import Dict, Any, List, Optional, Tuple

# ==========================================================
# 🧠 Inicialização resiliente do cliente OpenAI
# ==========================================================

def get_openai_client() -> Tuple[Optional[OpenAI], Optional[str]]:
    """Inicializa o cliente OpenAI de forma resiliente e segura."""
    secrets = st.secrets
    api_key = None

    openai_block = secrets.get("openai")

    # Caso [openai] seja um dicionário (formato correto)
    if isinstance(openai_block, dict):
        api_key = openai_block.get("api_key")

    # Caso seja uma string (formato incorreto, mas lido como texto)
    elif isinstance(openai_block, str) and "api_key" in openai_block:
        match = re.search(r"api_key['\"]*:\s*['\"]([^'\"]+)['\"]", openai_block)
        if match:
            api_key = match.group(1)

    # Fallbacks alternativos
    api_key = api_key or secrets.get("openai.api_key") or secrets.get("OPENAI_API_KEY")
    model = (
        secrets.get("openai", {}).get("model")
        if isinstance(secrets.get("openai"), dict)
        else secrets.get("OPENAI_MODEL", "gpt-4o")
    )

    if not api_key:
        st.warning("⚠️ A chave OpenAI não foi encontrada. Verifique o painel de *Secrets* antes de usar o processamento IA.")
        return None, None

    try:
        client = OpenAI(api_key=api_key)
        return client, model
    except Exception as e:
        st.error(f"❌ Erro ao inicializar o cliente OpenAI: {e}")
        return None, None


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

    # file pode ser SpooledTemporaryFile; usar getbuffer quando disponível
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
# 🔧 Utilitário: normalização de JSON
# ==========================================================

_CODEFENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE | re.MULTILINE)

def _coerce_json(obj: Any) -> Dict[str, Any]:
    """
    Converte conteúdo textual em dicionário JSON.
    - Remove cercas de código (```json ... ```).
    - Retorna {} em caso de erro.
    """
    if isinstance(obj, dict):
        return obj
    if not isinstance(obj, str):
        return {}

    cleaned = _CODEFENCE_RE.sub("", obj).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {}


# ==========================================================
# 🤖 Processamento IA
# ==========================================================

def process_insumo_text(texto: str) -> Dict[str, Any]:
    """
    Analisa o texto via IA e retorna:
    {
        "campos_ai": { ...campos estruturados... },
        "erro": None|str,
        "raw": "<json como string>"
    }
    """
    client, model = get_openai_client()

    if not client:
        return {
            "erro": "⚠️ A chave OpenAI não foi encontrada ou é inválida.",
            "campos_ai": {},
            "raw": "",
            "observacao": "Upload e histórico continuam funcionando normalmente.",
        }

    try:
        prompt = f"""
Você é um assistente técnico do Tribunal de Justiça de São Paulo.
Extraia do texto abaixo as informações relevantes para preencher um Documento de Formalização da Demanda (DFD).
Retorne **apenas** um JSON estritamente válido, com as chaves exatamente assim:

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

# Texto-base:
{texto}
        """.strip()

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

        conteudo = (resposta.choices[0].message.content or "").strip()
        campos_dict = _coerce_json(conteudo)

        # Garante chaves esperadas mesmo que ausentes
        for k in [
            "unidade_solicitante",
            "responsavel",
            "objeto",
            "justificativa",
            "quantidade",
            "urgencia",
            "riscos",
            "alinhamento_planejamento",
        ]:
            campos_dict.setdefault(k, "")

        return {"campos_ai": campos_dict, "erro": None, "raw": conteudo}

    except Exception as e:
        return {
            "erro": f"Erro ao processar o texto via IA: {e}",
            "campos_ai": {},
            "raw": "",
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

    # Lista recursiva
    arquivos: List[str] = []
    for root, _, files in os.walk(base):
        for file in files:
            arquivos.append(os.path.join(root, file))
    return arquivos
