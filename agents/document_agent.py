# ==========================================================
# agents/document_agent.py — VERSÃO 2025-D10 (ESTÁVEL)
# Totalmente compatível com AIClient (responses.create)
# ==========================================================

from __future__ import annotations

import json
from datetime import datetime
from utils.ai_client import AIClient


SECOES = [
    "Contexto Institucional",
    "Diagnóstico da Situação Atual",
    "Fundamentação da Necessidade",
    "Objetivos da Contratação",
    "Escopo Inicial da Demanda",
    "Resultados Esperados",
    "Benefícios Institucionais",
    "Justificativa Legal",
    "Riscos da Não Contratação",
    "Requisitos Mínimos",
    "Critérios de Sucesso",
]


class DocumentAgent:

    def __init__(self, artefato="DFD"):
        self.artefato = artefato
        try:
            self.ai = AIClient()
        except Exception as e:
            print(f"[DocumentAgent] ERRO ao inicializar AIClient: {e}")
            self.ai = None

    # ==========================================================
    # Processamento principal
    # ==========================================================
    def generate(self, conteudo_base: str) -> dict:
        
        # Verificar se AIClient foi inicializado
        if self.ai is None:
            return {
                "erro": "AIClient não disponível. Verifique OPENAI_API_KEY.",
                "DFD": self._get_template_vazio()
            }

        prompt = self._montar_prompt()

        resposta = self.ai.ask(
            prompt=prompt,
            conteudo=conteudo_base,
            artefato="DFD",
        )

        # Se a IA retornou erro → propagar
        if "erro" in resposta:
            return resposta

        # Extração da raiz {"DFD": {...}}
        if "DFD" in resposta and isinstance(resposta["DFD"], dict):
            d = resposta["DFD"]
        else:
            d = resposta

        # Sanitização mínima
        d.setdefault("texto_narrativo", "")
        d.setdefault("secoes", {})
        d.setdefault("lacunas", [])
        d.setdefault("descricao_necessidade", "")
        d.setdefault("motivacao", "")
        d.setdefault("unidade_demandante", "")
        d.setdefault("responsavel", "")
        d.setdefault("prazo_estimado", "")
        d.setdefault("valor_estimado", "0,00")

        # Garantir 11 seções
        secoes = d.get("secoes", {})
        for s in SECOES:
            secoes.setdefault(s, "Conteúdo não identificado no documento.")
        d["secoes"] = secoes

        d["gerado_em"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        d["origem"] = "document_agent_D10"

        return d
    
    # ==========================================================
    # Template vazio para fallback
    # ==========================================================
    def _get_template_vazio(self) -> dict:
        """Retorna estrutura vazia quando IA não está disponível"""
        secoes = {}
        for s in SECOES:
            secoes[s] = ""
        
        return {
            "unidade_demandante": "",
            "responsavel": "",
            "prazo_estimado": "",
            "valor_estimado": "0,00",
            "descricao_necessidade": "",
            "motivacao": "",
            "texto_narrativo": "",
            "secoes": secoes,
            "lacunas": [],
            "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": "template_vazio"
        }

    # ==========================================================
    # Prompt institucional
    # ==========================================================
    def _montar_prompt(self) -> str:
        return (
            "Você é o agente institucional do TJSP responsável por extrair informações "
            "de documentos (ETP, TR, DFD, Editais) e estruturá-las no formato DFD completo.\n\n"
            "INSTRUÇÕES CRÍTICAS:\n"
            "1. EXTRAIA os dados do documento fornecido\n"
            "2. Se o documento for um ETP, extraia:\n"
            "   - Unidade demandante da seção EQUIPE DE PLANEJAMENTO\n"
            "   - Responsável/Gestor da seção EQUIPE DE PLANEJAMENTO\n"
            "   - Valor estimado da seção ESTIMATIVA DE VALOR\n"
            "   - Descrição da necessidade das seções iniciais (OBJETO + NECESSIDADE)\n"
            "   - Motivação do PLANEJAMENTO ESTRATÉGICO\n"
            "3. Para texto_narrativo: consolide todo o conteúdo relevante\n"
            "4. Para cada seção do DFD, extraia informações correlatas do documento\n\n"
            "Responda SOMENTE com JSON no formato:\n\n"
            "{\n"
            "  \"DFD\": {\n"
            "    \"unidade_demandante\": \"[extrair da seção 25]\",\n"
            "    \"responsavel\": \"[extrair da seção 25]\",\n"
            "    \"prazo_estimado\": \"[extrair da seção 26 se houver]\",\n"
            "    \"valor_estimado\": \"[extrair da seção 13 - formato '0,00']\",\n"
            "    \"descricao_necessidade\": \"[seções 1 e 2 completas]\",\n"
            "    \"motivacao\": \"[seção 4 completa]\",\n"
            "    \"texto_narrativo\": \"[todo o documento estruturado]\",\n"
            "    \"secoes\": {\n"
            "      \"Contexto Institucional\": \"[extrair contexto do documento]\",\n"
            "      \"Diagnóstico da Situação Atual\": \"[seção 2 do ETP]\",\n"
            "      \"Fundamentação da Necessidade\": \"[seção 2 do ETP]\",\n"
            "      \"Objetivos da Contratação\": \"[seção 1 do ETP]\",\n"
            "      \"Escopo Inicial da Demanda\": \"[seção 6 do ETP]\",\n"
            "      \"Resultados Esperados\": \"[seção 16 do ETP]\",\n"
            "      \"Benefícios Institucionais\": \"[seção 16 do ETP]\",\n"
            "      \"Justificativa Legal\": \"[seções legais do ETP]\",\n"
            "      \"Riscos da Não Contratação\": \"[inferir do documento]\",\n"
            "      \"Requisitos Mínimos\": \"[seção 6 do ETP]\",\n"
            "      \"Critérios de Sucesso\": \"[seção 16 do ETP]\"\n"
            "    },\n"
            "    \"lacunas\": [\"liste campos que não foram encontrados\"]\n"
            "  }\n"
            "}"
        )

# ==========================================================
# Função universal — chamada pelo integration_dfd
# ==========================================================
def processar_dfd_com_ia(conteudo_textual: str = "") -> dict:
    """
    Wrapper universal utilizado pelo integration_dfd.
    Recebe texto puro e retorna:
        { "timestamp": "...", "resultado_ia": { ...DFD... } }
    """
    
    print(f"[processar_dfd_com_ia] Iniciando processamento...")
    print(f"[processar_dfd_com_ia] Tamanho do conteúdo: {len(conteudo_textual)} caracteres")

    if not conteudo_textual or len(conteudo_textual.strip()) < 15:
        return {
            "erro": "Conteúdo insuficiente para processamento IA.",
            "conteudo_recebido": conteudo_textual,
        }

    try:
        print("[processar_dfd_com_ia] Instanciando DocumentAgent...")
        agente = DocumentAgent("DFD")
        
        print("[processar_dfd_com_ia] Chamando agente.generate()...")
        resultado = agente.generate(conteudo_textual)
        
        print(f"[processar_dfd_com_ia] Resultado obtido: {type(resultado)}")

        # Se houve erro interno → propagar
        if isinstance(resultado, dict) and "erro" in resultado:
            print(f"[processar_dfd_com_ia] Erro no resultado: {resultado['erro']}")
            return {
                "erro": resultado["erro"],
                "conteudo_recebido": conteudo_textual[:500],
            }

        # ✅ NOVO: Registrar evento de auditoria
        try:
            from utils.audit_logger import registrar_evento_auditoria
            word_count = len(conteudo_textual.split())
            char_count = len(conteudo_textual)
            registrar_evento_auditoria(
                artefato="DFD",
                word_count=word_count,
                char_count=char_count,
                etapa="processamento",
                conteudo_textual=conteudo_textual
            )
        except Exception as e:
            print(f"[processar_dfd_com_ia] ⚠️ Falha ao registrar auditoria: {e}")

        print("[processar_dfd_com_ia] Processamento concluído com sucesso")
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "resultado_ia": resultado,
        }

    except Exception as e:
        print(f"[processar_dfd_com_ia] EXCEÇÃO: {e}")
        import traceback
        traceback.print_exc()
        return {
            "erro": f"Falha ao gerar DFD universal: {e}",
            "conteudo_recebido": conteudo_textual[:500],
        }
