# ==========================================================
# utils/ai_client.py — VERSÃO CORRIGIDA 2025-D08
# Compatível com Streamlit Cloud + OpenAI SDK >= 1.50
# Usa chat.completions.create (API oficial atual)
# ==========================================================

from dotenv import load_dotenv
load_dotenv()

import os
import json
from openai import OpenAI

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False


class AIClient:
    """
    Cliente institucional robusto para uso no Streamlit Cloud.
    Evita qualquer parâmetro legado, incluindo 'proxies',
    que é a causa do erro:
       Client.__init__() got an unexpected keyword argument 'proxies'
    
    Busca OPENAI_API_KEY em múltiplas fontes:
    1. Variável de ambiente (os.getenv)
    2. Streamlit secrets (st.secrets), se disponível
    """

    def __init__(self, model: str = None):
        print("[AIClient] Inicializando versão 2025-D08 (chat.completions.create)")

        # Tentar carregar da variável de ambiente primeiro
        api_key = os.getenv("OPENAI_API_KEY")

        # Se não encontrada, tentar carregar dos secrets do Streamlit
        if not api_key and STREAMLIT_AVAILABLE:
            try:
                api_key = st.secrets.get("OPENAI_API_KEY")
            except Exception:
                api_key = None

        # Se ainda não encontrada, lançar erro
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY não encontrada.")

        # Cliente OFICIAL - apenas com api_key, SEM argumentos extras
        self.client = OpenAI(api_key=api_key)
        print("[AIClient] OpenAI client inicializado com sucesso")

        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        print(f"[AIClient] Modelo configurado: {self.model}")


    # ------------------------------------------------------
    # Método principal
    # ------------------------------------------------------
    def ask(self, prompt: str, conteudo: str | bytes = "", artefato: str = "DFD") -> dict:

        # Normalização do conteúdo
        if isinstance(conteudo, bytes):
            conteudo = conteudo.decode("utf-8", errors="ignore")
        elif not isinstance(conteudo, str):
            conteudo = str(conteudo)

        conteudo = conteudo or ""
        trecho = conteudo[:8000]

        messages = [
            {
                "role": "system",
                "content": (
                    "Você é o assistente institucional do Tribunal de Justiça do Estado de São Paulo (TJSP). "
                    "Responda exclusivamente com JSON válido."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"{prompt}\n\n"
                    f"=== CONTEÚDO DO DOCUMENTO ===\n"
                    f"{trecho}\n\n"
                    f"Responda somente com JSON referente ao artefato {artefato}."
                ),
            },
        ]

        # ------------------------------------------------------
        # Chamada oficial OpenAI (chat.completions.create)
        # ------------------------------------------------------
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.0,
                max_tokens=6000,
            )

            texto = response.choices[0].message.content
            if not isinstance(texto, str):
                texto = str(texto)

        except Exception as e:
            return {"erro": f"Falha grave ao consultar OpenAI: {e}"}

        # ------------------------------------------------------
        # Tentar JSON direto
        # ------------------------------------------------------
        try:
            return json.loads(texto)
        except Exception:
            pass

        # Limpeza mínima
        try:
            texto_limpo = texto.replace("```json", "").replace("```", "").strip()
            return json.loads(texto_limpo)
        except Exception:
            return {"resposta_texto": texto}


    # ------------------------------------------------------
    # Método chat() para compatibilidade com integration_tr
    # ------------------------------------------------------
    def chat(self, messages: list) -> dict:
        """
        Método compatível com integration_tr.py
        Retorna dict com chave 'content'
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=4000,
            )
            
            content = response.choices[0].message.content
            return {"content": content}
            
        except Exception as e:
            return {"content": "", "erro": str(e)}
