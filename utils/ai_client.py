# ==========================================================
# utils/ai_client.py — vNext_D2 (robusto + anti-alucinação)
# Cliente Institucional OpenAI – TJSP / SAAB
# Compatível com DocumentAgent Moderno-Governança
# ==========================================================

from dotenv import load_dotenv
load_dotenv()

import os
import json
from openai import OpenAI


class AIClient:
    """
    Cliente institucional padronizado para consultas à OpenAI, com:
      ✓ Logs de diagnóstico controlados
      ✓ Estrutura system/user consistente
      ✓ Reforço para JSON válido
      ✓ Limpeza automática de blocos ```json
      ✓ Fallback seguro sem quebrar o pipeline
    """

    def __init__(self, model: str = None):

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY não encontrada no ambiente.")

        # Cliente OpenAI oficial
        self.client = OpenAI(api_key=api_key)

        # Modelo padrão: leve, rápido e excelente para JSON administrativo
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # ==========================================================
    # MÉTODO PRINCIPAL — Pergunta ao modelo
    # ==========================================================
    def ask(self, prompt: str, conteudo: str | bytes = "", artefato: str = "DFD") -> dict:
        """
        Envia ao modelo:
            • prompt institucional (regra do documento)
            • conteúdo bruto (texto extraído do insumo)

        Sempre tenta:
            • Retornar JSON estruturado (primeira prioridade)
            • Limpar blocos markdown
            • Prevenir alucinações
        """

        # ==================================================
        # Normalização do conteúdo
        # ==================================================
        if isinstance(conteudo, bytes):
            conteudo = conteudo.decode("utf-8", errors="ignore")
        elif not isinstance(conteudo, str):
            conteudo = str(conteudo)

        conteudo = conteudo or ""
        trecho = conteudo[:8000]  # Proteção contra requisições excessivas

        # ==================================================
        # Construção das mensagens OpenAI
        # ==================================================
        mensagens = [
            {
                "role": "system",
                "content": (
                    "Você é o assistente institucional do Tribunal de Justiça do Estado de São Paulo (TJSP). "
                    "Produza respostas formais, administrativas e SEMPRE em JSON válido, seguindo exatamente "
                    "as instruções do DocumentAgent e do artefato solicitado."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"{prompt}\n\n"
                    f"=== CONTEÚDO DO DOCUMENTO (INSUMO) ===\n"
                    f"{trecho}\n\n"
                    f"=== INSTRUÇÃO FINAL ===\n"
                    f"Responda EXCLUSIVAMENTE com um JSON válido, destinado ao artefato institucional: {artefato}."
                ),
            },
        ]

        # ==================================================
        # CHAMADA AO MODELO
        # ==================================================
        try:
            resposta = self.client.chat.completions.create(
                model=self.model,
                messages=mensagens,
                temperature=0.10,
                max_tokens=5000,
                response_format={"type": "json_object"},  # <=== FORÇA JSON VÁLIDO
            )

            texto = resposta.choices[0].message.content.strip()

        except Exception as e:
            print(f"[AIClient][ERRO FATAL] {e}")
            return {
                "erro": f"❌ Falha grave ao consultar OpenAI: {e}",
                "modelo_utilizado": self.model,
            }

        # ==================================================
        # Logs de diagnóstico — curtos e seguros
        # ==================================================
        try:
            print("\n===== AIClient DEBUG =====")
            print(f"[Modelo] {self.model} | [Artefato] {artefato}")
            print(f"[Prompt enviado] {len(prompt)} chars")
            print(f"[Trecho Documento] {len(trecho)} chars")
            print(f"[Resposta JSON bruta] {texto[:400]}...\n")
        except:
            pass  # Nunca interromper execução por causa de print

        # ==================================================
        # TENTATIVA 1 — JSON direto (response_format garantiu isso)
        # ==================================================
        try:
            parsed = json.loads(texto)
            return parsed
        except Exception:
            print("[AIClient] JSON direto falhou — tentando limpeza.")

        # ==================================================
        # TENTATIVA 2 — Limpeza de blocos ```json
        # ==================================================
        try:
            texto_limpo = (
                texto.replace("```json", "")
                .replace("```", "")
                .replace("“", '"')
                .replace("”", '"')
                .strip()
            )
            parsed = json.loads(texto_limpo)
            print("[AIClient] JSON recuperado após limpeza de blocos.")
            return parsed
        except Exception:
            print("[AIClient] Limpeza JSON falhou — retornando texto bruto.")

        # ==================================================
        # TENTATIVA 3 — fallback seguro
        # ==================================================
        return {"resposta_texto": texto}
