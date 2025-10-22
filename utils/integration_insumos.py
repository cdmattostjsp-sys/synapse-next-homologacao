import sys, os
from pathlib import Path

# Garante que a pasta 'utils' seja encontrada pelo Python, mesmo fora do diretório 'pages'
sys.path.append(str(Path(__file__).resolve().parents[1] / "utils"))

# ==========================================================
# 📁 integration_insumos.py
# SynapseNext – Módulo de Upload e Controle de Insumos Institucionais
# Secretaria de Administração e Abastecimento – SAAB 5.0
# ==========================================================

from datetime import datetime
from pathlib import Path
import json

def salvar_insumo(artefato: str, arquivo, usuario: str = "anônimo", descricao: str = "") -> dict:
    """
    Salva um arquivo de insumo dentro da pasta 'uploads/<artefato>/'
    e registra o evento no log de integrações.
    
    Parâmetros:
        artefato (str): Nome do artefato (ex.: DFD, ETP, TR, Edital, Contrato)
        arquivo (UploadedFile): Arquivo carregado via Streamlit
        usuario (str): Nome do usuário remetente
        descricao (str): Descrição ou contexto do envio
    
    Retorna:
        dict: Mensagem e caminho do arquivo salvo
    """
    base = Path(__file__).resolve().parents[1]
    destino_dir = base / "uploads" / artefato
    destino_dir.mkdir(parents=True, exist_ok=True)

    # Salvar o arquivo no diretório correspondente
    save_path = destino_dir / arquivo.name
    with open(save_path, "wb") as f:
        f.write(arquivo.getbuffer())

    # Gerar log do envio
    log_entry = {
        "artefato": artefato,
        "arquivo": arquivo.name,
        "usuario": usuario,
        "descricao": descricao,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "path": str(save_path)
    }

    log_dir = base / "exports" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"insumos_{datetime.now().strftime('%Y%m%d')}.json"

    if log_path.exists():
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
    else:
        logs = []

    logs.append(log_entry)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)

    return {
        "mensagem": f"Arquivo '{arquivo.name}' salvo com sucesso em '{destino_dir}'.",
        "path": str(save_path)
    }


def listar_insumos(artefato: str) -> list:
    """
    Retorna uma lista de arquivos armazenados para o artefato informado.
    """
    base = Path(__file__).resolve().parents[1]
    destino_dir = base / "uploads" / artefato
    if not destino_dir.exists():
        return []
    return [f.name for f in destino_dir.iterdir() if f.is_file()]

# ==========================================================
# 🧠 Processamento semântico via OpenAI (integração com SynapseNext)
# ==========================================================
import re
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def process_insumo_text(text: str, artefato: str = "DFD") -> dict:
    """
    Analisa o conteúdo textual de um documento e retorna campos inferidos por IA.
    Utiliza seções numeradas (1. Objeto, 2. Justificativa, etc.) e inferência semântica.
    """
    # Divide o texto em seções numeradas multilinha
    sections = re.split(r"\n\s*\d+\.\s*(?=[A-ZÁÉÍÓÚ])", text)
    parsed = {}
    for sec in sections:
        if not sec.strip():
            continue
        match = re.match(r"([A-Za-zÁÉÍÓÚâêôçãõ\s\-]+)\n", sec)
        if match:
            title = match.group(1).strip()
            content = sec[len(title):].strip()
            parsed[title] = content

    joined_text = "\n".join([f"{k}: {v}" for k, v in parsed.items()])

    prompt = f"""
Você é um analista técnico especializado em documentos administrativos do setor público.
Extraia os principais campos de um artefato do tipo {artefato}, no formato JSON:

{{
  "unidade": "",
  "responsavel": "",
  "objeto": "",
  "justificativa": "",
  "quantidade": "",
  "urgencia": "",
  "riscos": "",
  "alinhamento": ""
}}

Texto base:
{joined_text[:8000]}
"""

    try:
        response = client.chat.completions.create(
            model=st.secrets["openai"]["model"],
            messages=[
                {"role": "system", "content": "Você é um extrator de informações técnicas para processos administrativos públicos."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"resultado_bruto": content}
    except Exception as e:
        return {"erro": str(e)}


