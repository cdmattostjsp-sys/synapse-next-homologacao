import os
import json
import fitz  # PyMuPDF
import docx2txt
import streamlit as st
from openai import OpenAI

# =========================================================
# 🔐 Função de inicialização segura do cliente OpenAI
# =========================================================
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
    model = model or secrets.get("openai.model") or "gpt-4o"

    if not api_key:
        raise ValueError("⚠️ A chave OpenAI não foi encontrada em st.secrets.")

    client = OpenAI(api_key=api_key)
    return client, model


# =========================================================
# 📥 Funções auxiliares de upload e listagem
# =========================================================
def salvar_insumo(arquivo, pasta_destino="uploads"):
    """
    Salva o arquivo enviado pelo usuário na pasta de uploads.
    """
    os.makedirs(pasta_destino, exist_ok=True)
    caminho = os.path.join(pasta_destino, arquivo.name)
    with open(caminho, "wb") as f:
        f.write(arquivo.getbuffer())
    return caminho


def listar_insumos(pasta_destino="uploads"):
    """
    Lista os arquivos de insumos salvos localmente.
    """
    if not os.path.exists(pasta_destino):
        return []
    return [f for f in os.listdir(pasta_destino) if not f.startswith(".")]


# =========================================================
# 📄 Extração de texto
# =========================================================
def extrair_texto(caminho_arquivo):
    """
    Lê e extrai texto de arquivos PDF, DOCX ou TXT.
    """
    ext = os.path.splitext(caminho_arquivo)[1].lower()
    texto = ""

    if ext == ".pdf":
        with fitz.open(caminho_arquivo) as pdf:
            for pagina in pdf:
                texto += pagina.get_text("text") + "\n"
    elif ext == ".docx":
        texto = docx2txt.process(caminho_arquivo)
    elif ext == ".txt":
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            texto = f.read()
    else:
        raise ValueError("Formato de arquivo não suportado. Use PDF, DOCX ou TXT.")

    return texto.strip()


# =========================================================
# 🧠 Processamento via IA
# =========================================================
def process_insumo_text(conteudo_texto):
    """
    Envia o conteúdo do insumo para a IA e retorna campos estruturados (campos_ai).
    Se a IA devolver texto natural, faz parsing heurístico.
    """
    client, model = get_openai_client()

    prompt = f"""
    Extraia do texto abaixo as informações necessárias para o preenchimento
    do Documento de Formalização da Demanda (DFD) no formato JSON,
    com as chaves:
    unidade, responsavel, objeto, justificativa, quantidade, urgencia, riscos, alinhamento.
    
    Retorne SOMENTE o JSON, sem explicações adicionais.

    Texto:
    {conteudo_texto[:7000]}
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente técnico especializado em gestão pública e contratação governamental."
                },
                {"role": "user", "content": prompt}
            ],
            # GPT-5 não aceita temperature ≠ 1
            **({"temperature": 0.2} if not model.startswith("gpt-5") else {})
        )

        content = response.choices[0].message.content.strip()

        # tenta decodificar o retorno da IA como JSON
        try:
            campos = json.loads(content)
        except json.JSONDecodeError:
            # fallback simples: extrai pares "chave: valor" do texto
            campos = {}
            for line in content.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    campos[k.strip().lower()] = v.strip()

        # normaliza estrutura esperada
        for campo in [
            "unidade",
            "responsavel",
            "objeto",
            "justificativa",
            "quantidade",
            "urgencia",
            "riscos",
            "alinhamento",
        ]:
            campos.setdefault(campo, "")

        return campos

    except Exception as e:
        return {
            "erro": f"Falha na chamada à IA: {e}",
            "campos_ai": {},
            "observacao": "Upload e histórico continuam funcionando normalmente.",
        }


# =========================================================
# 🧭 Função principal de processamento de insumo
# =========================================================
def processar_insumo(caminho_arquivo):
    """
    Orquestra a leitura, extração e inferência de dados via IA.
    """
    try:
        texto = extrair_texto(caminho_arquivo)
        campos_ai = process_insumo_text(texto)

        resultado = {
            "arquivo": os.path.basename(caminho_arquivo),
            "texto_extraido": texto[:4000] + ("..." if len(texto) > 4000 else ""),
            "campos_ai": campos_ai,
        }

        # salva no session_state
        st.session_state["last_insumo"] = resultado
        return resultado

    except Exception as e:
        return {
            "erro": f"❌ Erro no processamento do insumo: {e}",
            "campos_ai": {},
            "observacao": "Verifique o formato do arquivo e tente novamente.",
        }
