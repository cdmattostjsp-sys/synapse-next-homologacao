# ==============================
# utils/integration_insumos.py
# SynapseNext – SAAB / TJSP
# ==============================

import os
import re
import json
import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
from io import BytesIO
from openai import OpenAI

# Inicializa o cliente OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------------------
# 📘 Função: Extrair texto bruto do arquivo
# ---------------------------
def extrair_texto_arquivo(uploaded_file):
    """Extrai texto puro de arquivos PDF, DOCX e TXT."""
    nome = uploaded_file.name.lower()
    texto = ""

    try:
        if nome.endswith(".pdf"):
            pdf_reader = PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                texto += page.extract_text() + "\n"

        elif nome.endswith(".docx"):
            doc = Document(uploaded_file)
            for para in doc.paragraphs:
                texto += para.text + "\n"

        elif nome.endswith(".txt"):
            texto = uploaded_file.read().decode("utf-8", errors="ignore")

        else:
            st.warning("⚠️ Formato de arquivo não suportado. Use PDF, DOCX ou TXT.")
            return ""

        texto = re.sub(r"\s+", " ", texto).strip()
        return texto

    except Exception as e:
        st.error(f"Erro ao extrair texto: {e}")
        return ""


# ---------------------------
# 🧠 Função: Analisar texto com IA
# ---------------------------
def analisar_insumo(texto, artefato):
    """
    Realiza a análise semântica do texto conforme o artefato selecionado.
    """
    if not texto:
        return {}

    prompt = f"""
    Você é um assistente técnico do Tribunal de Justiça de São Paulo.
    Analise o texto abaixo e extraia informações relevantes para o artefato "{artefato}".
    Devolva um JSON com os campos inferidos.

    Texto:
    {texto[:8000]}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Você é um especialista em gestão pública e contratações."},
                      {"role": "user", "content": prompt}],
            temperature=0.2
        )
        conteudo = response.choices[0].message.content

        match = re.search(r"\{.*\}", conteudo, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            return {"resultado_ai": conteudo}

    except Exception as e:
        st.error(f"Erro ao processar IA: {e}")
        return {}


# ---------------------------
# 🧩 Função: Parser Institucional aprimorado
# ---------------------------
def parser_institucional(texto):
    """
    Extrai campos específicos de documentos administrativos e licitatórios
    com base em padrões comuns de editais, DFDs e TRs.
    """

    campos = {}

    # Lista de padrões chave-valor
    padroes = {
        "modalidade": r"(?i)modalidade\s*[:\-–]\s*([^\n\r\.]+)",
        "regime_execucao": r"(?i)regime\s+de\s+execu[cç][aã]o\s*[:\-–]\s*([^\n\r\.]+)",
        "criterio_julgamento": r"(?i)crit[eé]rio\s+de\s+julgamento\s*[:\-–]\s*([^\n\r\.]+)",
        "prazo_execucao": r"(?i)prazo\s+(?:de\s+execu[cç][aã]o|vig[eê]ncia)\s*[:\-–]\s*([^\n\r\.]+)",
        "forma_pagamento": r"(?i)forma\s+de\s+pagamento\s*[:\-–]\s*([^\n\r\.]+)",
        "penalidades": r"(?i)penalidades?\s*[:\-–]\s*([^\n\r\.]+)",
        "base_legal": r"(?i)(lei\s*n[ºo]?\s*\d{4,5}\s*/?\s*\d{4})",
        "objeto": r"(?i)objeto\s*[:\-–]\s*(.+?)(?=\n[A-Z0-9]+\s*[:\-–]|\Z)"
    }

    for campo, regex in padroes.items():
        match = re.search(regex, texto, re.DOTALL)
        if match:
            valor = match.group(1).strip()
            valor = re.sub(r"\s+", " ", valor)
            campos[campo] = valor

    # Fallback semântico básico
    if "modalidade" not in campos and "pregão" in texto.lower():
        campos["modalidade"] = "Pregão Eletrônico"
    if "regime_execucao" not in campos and "empreitada" in texto.lower():
        campos["regime_execucao"] = "Empreitada por preço unitário"
    if "criterio_julgamento" not in campos and "menor preço" in texto.lower():
        campos["criterio_julgamento"] = "Menor preço global"
    if "base_legal" not in campos and "14.133" in texto:
        campos["base_legal"] = "Lei nº 14.133/2021"

    return campos


# ---------------------------
# 💾 Função principal de processamento
# ---------------------------
def processar_insumo(uploaded_file, artefato):
    """Processa o insumo e retorna o dicionário consolidado."""
    texto_extraido = extrair_texto_arquivo(uploaded_file)

    if not texto_extraido:
        return None

    st.success(f"📘 Documento '{uploaded_file.name}' processado com sucesso.")
    st.write("IA processando o insumo e identificando campos relevantes...")

    resultado_ai = analisar_insumo(texto_extraido, artefato)
    campos_extrator = parser_institucional(texto_extraido)

    # Combina resultados (IA + Regex)
    campos_combinados = {**resultado_ai, **campos_extrator}

    # Guarda no estado da sessão
    st.session_state["last_insumo"] = {
        "nome_arquivo": uploaded_file.name,
        "artefato": artefato,
        "texto": texto_extraido,
        "campos_ai": campos_combinados
    }

    st.success(f"📄 Insumo '{uploaded_file.name}' registrado e processado com sucesso.")
    st.json(campos_combinados)

    return campos_combinados


# ---------------------------
# 📜 Funções auxiliares de integração
# ---------------------------
def salvar_insumo(uploaded_file, artefato):
    pasta = "insumos_processados"
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, uploaded_file.name)
    with open(caminho, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return caminho


def listar_insumos():
    pasta = "insumos_processados"
    if not os.path.exists(pasta):
        return []
    return [f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]
