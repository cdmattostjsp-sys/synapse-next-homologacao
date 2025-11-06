# ==========================================================
# utils/ai_client.py
# SynapseNext – Cliente Institucional OpenAI (TJSP)
# Revisão: Engenheiro Synapse – 2025-11-08 (vNext_r2)
# Compatibilidade: Streamlit 1.39.0 + openai 2.7.1
# ==========================================================

import os
import json
from openai import OpenAI


class AIClient:
    """
    Cliente institucional padronizado para uso interno dos agentes IA.
    Implementa controle de modelo, chave segura e tratamento de exceções.
    """

    def __init__(self, model: str = None):
        """
        Inicializa o cliente OpenAI institucional.

        Args:
            model (str, opcional): modelo a ser usado (ex.: "gpt-4o-mini").
                                   Se não informado, usa o modelo padrão
                                   configurado via variável de ambiente.
        """
        # Obtém chave da OpenAI (Streamlit secrets ou ambiente)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY não encontrada em ambiente (.env ou secrets.toml).")

        # Inicializa cliente OpenAI
        self.client = OpenAI(api_key=api_key)

        # Modelo padrão (configurável)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # ==========================================================
    # Método principal de inferência textual
    # ==========================================================
    def ask(self, prompt: str, conteudo: str | bytes = "", artefato: str = "DFD") -> dict:
        """
        Envia um prompt para o modelo de linguagem institucional e retorna a resposta.

        Args:
            prompt (str): instrução textual principal (pergunta ou template).
            conteudo (str | bytes): corpo do texto do documento analisado.
            artefato (str): tipo de artefato (DFD, ETP, TR, Edital...).

        Returns:
            dict: resposta estruturada em JSON (ou texto cru, se falhar).
        """

        try:
            # ======================================================
            # Garantia de tipo de conteúdo
            # ======================================================
            if isinstance(conteudo, bytes):
                conteudo = conteudo.decode("utf-8", errors="ignore")
            elif not isinstance(conteudo, str):
                conteudo = str(conteudo)

            # ======================================================
            # Montagem da mensagem de prompt contextualizada
            # ======================================================
            mensagem = (
                f"{prompt}\n\n"
                f"---\n"
                f"📄 Conteúdo do documento (trecho inicial):\n{conteudo[:4000]}\n"
                f"---\n"
                f"Responda no formato JSON estruturado para o artefato institucional: {artefato}."
            )

            # ======================================================
            # Chamada ao modelo OpenAI (chat.completions)
            # ======================================================
            resposta = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Você é um assistente técnico institucional do Tribunal de Justiça de São Paulo (TJSP). "
                            "Analise documentos administrativos e gere respostas estruturadas e compatíveis "
                            "com os modelos oficiais (DFD, ETP, TR, Edital, Contrato)."
                        ),
                    },
                    {"role": "user", "content": mensagem},
                ],
                temperature=0.4,
                max_tokens=2000,
            )

            # ======================================================
            # Processamento da resposta
            # ======================================================
            texto = resposta.choices[0].message.content.strip()

            # Tenta converter para JSON direto
            try:
                return json.loads(texto)
            except Exception:
                # Retorna texto cru caso a IA não respeite o formato JSON
                return {"resposta_texto": texto}

        # ======================================================
        # Tratamento de falhas de comunicação ou execução
        # ======================================================
        except Exception as e:
            return {
                "erro": f"❌ Falha na chamada OpenAI: {e}",
                "modelo_utilizado": self.model,
            }
