# ==========================================================
# 📁 integration_insumos.py
# SynapseNext – Módulo de Upload e Controle de Insumos Institucionais
# Secretaria de Administração e Abastecimento – SAAB 5.0
# ==========================================================

import json
import re
from datetime import datetime
from pathlib import Path

# ==========================================================
# 💾 Função: salvar_insumo
# ==========================================================
def salvar_insumo(artefato: str, arquivo, usuario: str = "anônimo", descricao: str = "") -> dict:
    """
    Salva um arquivo de insumo dentro da pasta 'uploads/<artefato>/'
    e registra o evento no log de integrações.
    """
    base = Path(__file__).resolve().parents[1]
    destino_dir = base / "uploads" / artefato
    destino_dir.mkdir(parents=True, exist_ok=True)

    save_path = destino_dir / arquivo.name
    with open(save_path, "wb") as f:
        f.write(arquivo.getbuffer())

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

# ==========================================================
# 📂 Função: listar_insumos
# ==========================================================
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
# 🧠 Integração IA (OpenAI) — inicialização segura e sob demanda
# ==========================================================
def get_openai_client():
    """
    Inicializa o cliente OpenAI de forma segura e sob demanda.
    Evita KeyError durante o carregamento do módulo no Streamlit Cloud.
    """
    try:
        import streamlit as st
        from openai import OpenAI
    except Exception as e:
        raise RuntimeError(f"Erro ao importar dependências de IA: {e}")

    # Acesso seguro aos segredos
    secrets = st.secrets.get("openai", {})
    api_key = secrets.get("api_key")
    model = secrets.get("model", "gpt-4o-mini")

    if not api_key:
        raise ValueError(
            "⚠️ A chave OpenAI não foi encontrada em st.secrets['openai']['api_key'].\n"
            "Verifique se ela está configurada corretamente no painel do Streamlit Cloud."
        )

    try:
        client = OpenAI(api_key=api_key)
        return client, model
    except Exception as e:
        raise RuntimeError(f"Erro ao inicializar o cliente OpenAI: {e}")

# ==========================================================
# 🤖 Função: process_insumo_text
# ==========================================================
def process_insumo_text(text: str, artefato: str = "DFD") -> dict:
    """
    Analisa o conteúdo textual de um documento e retorna campos inferidos por IA.
    Compatível com Streamlit Cloud mesmo sem chave OpenAI configurada.
    """

    # ----------------------------
    # 🔍 Parsing básico do texto
    # ----------------------------
    sections = re.split(r"\n\s*\d+\.\s*(?=[A-ZÁÉÍÓÚ])", text or "")
    parsed = {}
    for sec in sections:
        if not sec.strip():
            continue
        match = re.match(r"([A-Za-zÁÉÍÓÚâêôçãõ\s\-]+)\n", sec)
        if match:
            title = match.group(1).strip()
            content = sec[len(title):].strip()
            parsed[title] = content

    joined_text = "\n".join([f"{k}: {v}" for k, v in parsed.items()]) or text

    # ----------------------------
    # 🤖 Inicialização da IA
    # ----------------------------
    try:
        client, model = get_openai_client()
    except Exception as e:
        # Não interrompe a página se a IA falhar ou chave não existir
        return {
            "erro": str(e),
            "campos_ai": {},
            "observacao": "Upload e histórico continuam funcionando normalmente."
        }

    # ----------------------------
    # 🧩 Prompt de análise semântica
    # ----------------------------
    prompt = f"""
Você é um analista técnico especializado em documentos administrativos do setor público.
Extraia os principais campos de um artefato do tipo {artefato}, retornando um JSON com as chaves:

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

    # ----------------------------
    # 🧠 Chamada ao modelo OpenAI
    # ----------------------------
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um extrator de informações técnicas para processos administrativos públicos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"resultado_bruto": content}

    except Exception as e:
        return {"erro": f"Falha na chamada à IA: {e}"}
