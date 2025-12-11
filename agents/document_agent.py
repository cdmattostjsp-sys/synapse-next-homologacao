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
            "de documentos (ETP, TR, DFD, Editais, Contratos) e estruturá-las no formato DFD completo.\n\n"
            
            "INSTRUÇÕES CRÍTICAS:\n"
            "1. IDENTIFIQUE o tipo de documento (ETP, TR, Edital, Contrato, Licitação)\n"
            "2. EXTRAIA todas as informações disponíveis, não deixe campos com 'Não especificado'\n"
            "3. Se o documento for um EDITAL DE LICITAÇÃO:\n"
            "   - Unidade demandante: extraia do cabeçalho (UNIDADE GESTORA/UASG ou Secretaria)\n"
            "   - Objeto: extraia da seção OBJETO (descrição completa)\n"
            "   - Valor estimado: procure por valores de orçamento (se não houver, coloque 'Valor não divulgado')\n"
            "   - Justificativa: extraia de seções como JUSTIFICATIVA ou contexto\n"
            "   - Escopo: detalhamento técnico do OBJETO\n"
            "   - Fundamentação legal: todas as leis citadas (Lei 14.133/2021, etc.)\n"
            "4. Se o documento for um ETP:\n"
            "   - Unidade demandante: seção EQUIPE DE PLANEJAMENTO\n"
            "   - Responsável/Gestor: seção EQUIPE DE PLANEJAMENTO\n"
            "   - Valor estimado: seção ESTIMATIVA DE VALOR\n"
            "   - Descrição: seções OBJETO + NECESSIDADE\n"
            "   - Motivação: seção PLANEJAMENTO ESTRATÉGICO\n"
            "5. Para CADA SEÇÃO do DFD, extraia o máximo de informação possível do documento\n"
            "6. Se uma informação não estiver explícita mas puder ser INFERIDA logicamente, faça isso\n"
            "7. NUNCA deixe campos vazios ou com 'Não especificado' se houver dados no documento\n\n"
            
            "MAPEAMENTO PARA EDITAIS:\n"
            "- Contexto Institucional → Cabeçalho + Unidade gestora\n"
            "- Diagnóstico da Situação Atual → Justificativa do edital (inferir necessidade)\n"
            "- Fundamentação da Necessidade → Por que esta licitação é necessária (contextualizar)\n"
            "- Objetivos da Contratação → Finalidade da contratação\n"
            "- Escopo Inicial da Demanda → Descrição completa do OBJETO\n"
            "- Resultados Esperados → Benefícios esperados da contratação (inferir)\n"
            "- Benefícios Institucionais → Melhorias que a contratação trará\n"
            "- Justificativa Legal → Todas as leis, decretos, resoluções citadas\n"
            "- Riscos da Não Contratação → Consequências de não contratar (inferir)\n"
            "- Requisitos Mínimos → Especificações técnicas/qualificações exigidas\n"
            "- Critérios de Sucesso → Indicadores de sucesso (inferir do escopo)\n\n"
            
            "Responda SOMENTE com JSON no formato:\n\n"
            "{\n"
            "  \"DFD\": {\n"
            "    \"unidade_demandante\": \"[extrair do documento - NUNCA deixe vazio]\",\n"
            "    \"responsavel\": \"[extrair se disponível, senão: 'A definir']\",\n"
            "    \"prazo_estimado\": \"[extrair se disponível, senão inferir do cronograma]\",\n"
            "    \"valor_estimado\": \"[extrair - se não houver: 'Valor não divulgado']\",\n"
            "    \"descricao_necessidade\": \"[descrição COMPLETA e detalhada do objeto]\",\n"
            "    \"motivacao\": \"[justificativa COMPLETA - contextualizar necessidade institucional]\",\n"
            "    \"texto_narrativo\": \"[consolidação DETALHADA de todo o documento]\",\n"
            "    \"secoes\": {\n"
            "      \"Contexto Institucional\": \"[PREENCHA com dados do documento]\",\n"
            "      \"Diagnóstico da Situação Atual\": \"[PREENCHA - descreva situação atual]\",\n"
            "      \"Fundamentação da Necessidade\": \"[PREENCHA - por que é necessário]\",\n"
            "      \"Objetivos da Contratação\": \"[PREENCHA com objetivos claros]\",\n"
            "      \"Escopo Inicial da Demanda\": \"[PREENCHA com descrição técnica completa]\",\n"
            "      \"Resultados Esperados\": \"[PREENCHA com resultados mensuráveis]\",\n"
            "      \"Benefícios Institucionais\": \"[PREENCHA com benefícios concretos]\",\n"
            "      \"Justificativa Legal\": \"[PREENCHA com TODAS as bases legais citadas]\",\n"
            "      \"Riscos da Não Contratação\": \"[PREENCHA com riscos identificados]\",\n"
            "      \"Requisitos Mínimos\": \"[PREENCHA com requisitos técnicos]\",\n"
            "      \"Critérios de Sucesso\": \"[PREENCHA com indicadores]\"\n"
            "    },\n"
            "    \"lacunas\": [\"liste APENAS campos que realmente não existem no documento\"]\n"
            "  }\n"
            "}\n\n"
            "IMPORTANTE: Seja DETALHADO e COMPLETO. Não resuma demais. Extraia TODO o conteúdo relevante."
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
