# ==========================
# agents/document_agent.py — vNext com melhorias completas
# ==========================

from __future__ import annotations
import json
import os
from datetime import datetime
from utils.ai_client import AIClient


def _registrar_log_document_agent(payload: dict) -> str:
    try:
        logs_dir = os.path.join("exports", "logs")
        os.makedirs(logs_dir, exist_ok=True)
        filename = f"document_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = os.path.join(logs_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)
        return path
    except Exception as e:
        return f"ERRO_LOG: {e}"


class DocumentAgent:
    def __init__(self, artefato: str):
        self.artefato = artefato.upper()
        self.ai = AIClient()

    def generate(self, conteudo_base: str) -> dict:
        prompt = self._montar_prompt_institucional()

        log_payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "artefato": self.artefato,
            "conteudo_input_len": len(conteudo_base or ""),
            "conteudo_input_preview": (conteudo_base[:1500] if conteudo_base else ""),
            "prompt_usado": prompt,
        }

        try:
            resposta = self.ai.ask(prompt=prompt, conteudo=conteudo_base, artefato=self.artefato)
            log_payload["resposta_bruta"] = resposta

            if not isinstance(resposta, dict):
                return {"erro": "Resposta IA inválida ou vazia."}

            if "resposta_texto" in resposta:
                texto_bruto = (resposta.get("resposta_texto") or "").strip()
                if texto_bruto.startswith("```json"):
                    texto_bruto = texto_bruto.replace("```json", "").replace("```", "").strip()
                try:
                    parsed = json.loads(texto_bruto)
                    log_payload["json_reprocessado"] = parsed
                    if isinstance(parsed, dict) and "DFD" in parsed:
                        return parsed["DFD"]
                    return parsed
                except Exception:
                    return {"Conteudo": texto_bruto}

            if "DFD" in resposta and isinstance(resposta.get("DFD"), dict):
                return resposta["DFD"]

            return resposta

        finally:
            _registrar_log_document_agent(log_payload)

    def _montar_prompt_institucional(self) -> str:
        if self.artefato == "DFD":
            return (
                "Você é o agente de Formalização da Demanda (DFD) da Secretaria de Administração e Abastecimento "
                "(SAAB) do Tribunal de Justiça do Estado de São Paulo (TJSP). Produza um DFD completo, institucional, "
                "conforme a Lei 14.133/2021.\n\n"
                "=== OBRIGAÇÕES ===\n"
                "1) Criar 'texto_narrativo' numerado de 1 a 11, sendo CADA NÚMERO EM NOVO PARÁGRAFO com quebra dupla.\n"
                "2) Criar objeto 'secoes' com 11 seções formais.\n"
                "3) Criar lista 'lacunas' SOMENTE com itens realmente faltantes NO CONTEXTO DE DFD (não TR, não Edital).\n\n"
                "=== SEÇÕES OBRIGATÓRIAS ===\n"
                "- Contexto Institucional\n"
                "- Diagnóstico da Situação Atual\n"
                "- Fundamentação da Necessidade\n"
                "- Objetivos da Contratação\n"
                "- Escopo Inicial da Demanda\n"
                "- Resultados Esperados\n"
                "- Benefícios Institucionais\n"
                "- Justificativa Legal\n"
                "- Riscos da Não Contratação\n"
                "- Requisitos Mínimos\n"
                "- Critérios de Sucesso\n\n"
                "=== REGRAS ===\n"
                "• Parágrafos curtos.\n"
                "• Nada de bullets no texto narrativo.\n"
                "• Não inventar dados sensíveis.\n"
                "• Lacunas restritas a informações ADMINISTRATIVAS do DFD.\n\n"
                "=== SAÍDA EXATA ===\n"
                "{ 'DFD': { 'texto_narrativo': '...', 'secoes': {...}, 'lacunas': [] } }\n"
                "Responda APENAS JSON válido."
            )

        return (
            f"Você é o agente institucional do TJSP para o artefato {self.artefato}. "
            "Produza apenas JSON estruturado."
        )


def processar_dfd_com_ia(conteudo_textual: str = "") -> dict:
    if not conteudo_textual or len(conteudo_textual.strip()) < 15:
        return {"erro": "Conteúdo insuficiente para processamento IA."}
    agente = DocumentAgent("DFD")
    resultado = agente.generate(conteudo_textual)
    return {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "resultado_ia": resultado}


# ==========================
# utils/ai_client.py — vNext com ajustes sugeridos
# ==========================

from dotenv import load_dotenv
load_dotenv()

import os
import json
from openai import OpenAI


class AIClient:
    def __init__(self, model: str = None):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não encontrada.")
        self.client = OpenAI(api_key=api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def ask(self, prompt: str, conteudo: str | bytes = "", artefato: str = "DFD") -> dict:
        if isinstance(conteudo, bytes):
            conteudo = conteudo.decode("utf-8", errors="ignore")
        conteudo = conteudo or ""
        trecho = conteudo[:8000]

        mensagens = [
            {
                "role": "system",
                "content": (
                    "Você é o assistente institucional do TJSP. Siga integralmente o prompt institucional."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"{prompt}\n\n=== CONTEÚDO DO DOCUMENTO ===\n{trecho}\n\n"
                    f"Responda SOMENTE com JSON válido para o artefato: {artefato}."
                ),
            },
        ]

        try:
            resposta = self.client.chat.completions.create(
                model=self.model,
                messages=mensagens,
                temperature=0.2,
                max_tokens=3500,
            )
            texto = resposta.choices[0].message.content.strip()

            try:
                return json.loads(texto)
            except Exception:
                if texto.startswith("```"):
                    texto = texto.replace("```json", "").replace("```", "").strip()
                try:
                    return json.loads(texto)
                except Exception:
                    return {"resposta_texto": texto}

        except Exception as e:
            return {"erro": f"Falha na chamada OpenAI: {e}", "modelo": self.model}
