# ==========================================================
# agents/document_agent.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão: 2025-11-20 – vNext (DFD Moderno-Governança + Logs)
# ==========================================================

from __future__ import annotations
import json
import os
from datetime import datetime
from utils.ai_client import AIClient


# ==========================================================
# 🔧 Função interna de log institucional
# ==========================================================
def _registrar_log_document_agent(payload: dict) -> str:
    """
    Salva logs completos do DocumentAgent para auditoria e diagnóstico.
    """
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


# ==========================================================
# 🤖 DOCUMENT AGENT – Geração de artefatos IA
# ==========================================================
class DocumentAgent:
    """
    Agente responsável por coordenar a geração de documentos formais via IA.
    Agora com rastreamento completo via logs.
    """

    def __init__(self, artefato: str):
        self.artefato = artefato.upper()
        self.ai = AIClient()  # Cliente IA institucional

    # ======================================================
    # 🧠 GERAÇÃO DE CONTEÚDO VIA IA — vNext + LOGS
    # ======================================================
    def generate(self, conteudo_base: str) -> dict:
        """
        Envia o conteúdo bruto para IA usando o prompt institucional.
        Retorna dicionário JSON estruturado e registra logs detalhados.
        """

        # ============================
        # LOG 1 — registro inicial
        # ============================
        print("\n\n>>> [DocumentAgent] generate() chamado.")
        print(f">>> Artefato: {self.artefato}")
        print(f">>> Tamanho do conteúdo recebido: {len(conteudo_base or '')}")

        prompt = self._montar_prompt_institucional()

        # Criar payload de auditoria
        log_payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "artefato": self.artefato,
            "conteudo_input_len": len(conteudo_base or ""),
            "conteudo_input_preview": (conteudo_base[:1500] if conteudo_base else ""),
            "prompt_usado": prompt,
        }

        print(">>> [DocumentAgent] Prompt institucional carregado.")
        print(">>> [DocumentAgent] Prévia do prompt:")
        print(prompt[:500], "...\n")

        try:
            print(">>> [DocumentAgent] Chamando AIClient.ask() ...")
            resposta = self.ai.ask(
                prompt=prompt,
                conteudo=conteudo_base,
                artefato=self.artefato,
            )

            print(">>> [DocumentAgent] Retorno bruto da IA:")
            print(resposta)

            # Resposta precisa ser um dicionário
            if not isinstance(resposta, dict):
                print(">>> [DocumentAgent][ERRO] Retorno não é dict.")
                return {"erro": "Resposta IA inválida ou vazia."}

            # ==================================================
            # CASO 1 – AIClient NÃO conseguiu json.loads()
            #         e devolveu {"resposta_texto": "..."}
            # ==================================================
            if "resposta_texto" in resposta:
                print(">>> [DocumentAgent] IA retornou resposta_texto (não JSON).")

                texto_bruto = (resposta.get("resposta_texto") or "").strip()

                if not texto_bruto:
                    print(">>> [DocumentAgent][ERRO] texto_bruto vazio.")
                    return {"erro": "IA não retornou conteúdo textual."}

                if texto_bruto.startswith("```json"):
                    texto_bruto = (
                        texto_bruto.replace("```json", "")
                        .replace("```", "")
                        .strip()
                    )

                try:
                    parsed = json.loads(texto_bruto)
                    print(">>> [DocumentAgent] JSON reprocessado manualmente com sucesso.")

                    if isinstance(parsed, dict) and "DFD" in parsed:
                        return parsed["DFD"]

                    return parsed

                except Exception as e:
                    print(f">>> [DocumentAgent][WARN] IA devolveu texto puro, sem JSON. Erro: {e}")
                    return {"Conteúdo": texto_bruto}

            # ==================================================
            # CASO 2 – AIClient JÁ devolveu JSON parseado
            # ==================================================
            if "DFD" in resposta:
                print(">>> [DocumentAgent] JSON já contém DFD estruturado.")

                dfd = resposta.get("DFD")
                
                # 🔥 registrar log
                log_payload["resposta_bruta_ia"] = resposta
                logfile = _registrar_log_document_agent(log_payload)
                print(f">>> [DocumentAgent] Log salvo em: {logfile}")

                if isinstance(dfd, dict):
                    return dfd

            # Caso geral
            print(">>> [DocumentAgent] JSON retornado diretamente.")

            # 🔥 registrar log
            log_payload["resposta_bruta_ia"] = resposta
            logfile = _registrar_log_document_agent(log_payload)
            print(f">>> [DocumentAgent] Log salvo em: {logfile}")

            return resposta

        except Exception as e:
            print(f">>> [DocumentAgent][ERRO FATAL] Exceção inesperada: {e}")

            # 🔥 registrar log de erro
            log_payload["erro"] = str(e)
            logfile = _registrar_log_document_agent(log_payload)
            print(f">>> [DocumentAgent] Log salvo em: {logfile}")

            return {"erro": f"Falha na geração do documento ({e})"}


    # ======================================================
    # 🧩 PROMPT INSTITUCIONAL – *vNext* (Modernizado)
    # ======================================================
    def _montar_prompt_institucional(self) -> str:

        if self.artefato == "DFD":
            return (
                "Você é o agente de Formalização da Demanda (DFD) da Secretaria de Administração e Abastecimento "
                "(SAAB) do Tribunal de Justiça do Estado de São Paulo (TJSP). "
                "Com base exclusivamente no texto fornecido (insumo), produza um DFD completo, institucional, "
                "em conformidade com a Lei nº 14.133/2021 e boas práticas de governança.\n\n"
                "=== OBJETIVO ===\n"
                "Gerar um documento robusto, organizado e pronto para análise administrativa, contendo:\n"
                "1) Texto narrativo numerado ('texto_narrativo'), com 11 seções formais.\n"
                "2) Objeto 'secoes' contendo as mesmas 11 seções individualmente.\n"
                "3) Lista 'lacunas' com informações ausentes relevantes.\n\n"
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
                "=== TEXTO NARRATIVO ===\n"
                "Elabore texto contínuo, numerado de 1 a 11, apenas texto limpo.\n\n"
                "=== LACUNAS ===\n"
                "Liste informações administrativas que NÃO apareçam no insumo.\n\n"
                "=== FORMATO FINAL ===\n"
                "{ \"DFD\": { \"texto_narrativo\": \"...\", \"secoes\": { ... }, \"lacunas\": [] } }\n"
                "Responda APENAS com JSON válido."
            )

        # Outros artefatos (ETP / TR / EDITAL etc.)
        return (
            f"Você é o agente institucional do TJSP responsável pelo artefato {self.artefato}. "
            "Produza um documento administrativo formal e retorne APENAS JSON estruturado."
        )


# ======================================================
# 🔌 Função pública usada pelo pipeline DFD
# ======================================================
def processar_dfd_com_ia(conteudo_textual: str = "") -> dict:

    if not conteudo_textual or len(conteudo_textual.strip()) < 15:
        return {"erro": "Conteúdo insuficiente para processamento IA."}

    agente = DocumentAgent("DFD")
    resultado = agente.generate(conteudo_textual)

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "resultado_ia": resultado,
    }
