# ==========================================================
# agents/etp_agent.py — AGENTE ESPECÍFICO PARA ETP
# Extração estruturada de Estudos Técnicos Preliminares (Lei 14.133/2021)
# ==========================================================

from __future__ import annotations

import json
from datetime import datetime
from utils.ai_client import AIClient


# 27 seções padronizadas do ETP (Lei 14.133/2021, art. 18, §1º)
SECOES_ETP = [
    "objeto",                                    # 1
    "descricao_necessidade",                     # 2
    "previsao_pca",                              # 3
    "planejamento_estrategico",                  # 4
    "catalogo_padronizacao",                     # 5
    "requisitos_contratacao",                    # 6
    "condicoes_recebimento",                     # 7
    "condicoes_execucao_pagamento",              # 8
    "garantias",                                 # 9
    "modalidade_licitacao",                      # 10
    "estimativa_quantidades",                    # 11
    "levantamento_mercado",                      # 12
    "estimativa_valor",                          # 13
    "descricao_solucao",                         # 14
    "justificativa_parcelamento",                # 15
    "resultados_pretendidos",                    # 16
    "providencias_previas",                      # 17
    "contratacoes_correlatas",                   # 18
    "impactos_ambientais",                       # 19
    "possibilidade_compra_locacao",              # 20
    "participacao_consorcio",                    # 21
    "vistoria_visita_tecnica",                   # 22
    "cumprimento_resolucoes_cnj",                # 23
    "plano_riscos",                              # 24
    "equipe_planejamento",                       # 25
    "estimativa_prazo_vigencia",                 # 26
    "avaliacao_conclusiva",                      # 27
]


class ETPAgent:
    """
    Agente especializado em extrair e estruturar ETPs (Lei 14.133/2021).
    Otimizado para identificar as 27 seções padronizadas.
    """

    def __init__(self):
        try:
            self.ai = AIClient()
        except Exception as e:
            print(f"[ETPAgent] ERRO ao inicializar AIClient: {e}")
            self.ai = None

    # ==========================================================
    # Processamento principal
    # ==========================================================
    def generate(self, conteudo_base: str) -> dict:
        """
        Processa o texto do ETP e retorna estrutura completa com 27 seções.
        """
        
        # Verificar se AIClient foi inicializado
        if self.ai is None:
            return {
                "erro": "AIClient não disponível. Verifique OPENAI_API_KEY.",
                "ETP": self._get_template_vazio()
            }

        prompt = self._montar_prompt()

        resposta = self.ai.ask(
            prompt=prompt,
            conteudo=conteudo_base,
            artefato="ETP",
        )

        # Se a IA retornou erro → propagar
        if "erro" in resposta:
            return resposta

        # Extração da raiz {"ETP": {...}}
        if "ETP" in resposta and isinstance(resposta["ETP"], dict):
            d = resposta["ETP"]
        else:
            d = resposta

        # Sanitização mínima - garantir todos os campos
        d.setdefault("unidade_demandante", "")
        d.setdefault("responsavel", "")
        d.setdefault("prazo_estimado", "")
        d.setdefault("valor_estimado", "0,00")

        # Garantir 27 seções padronizadas
        secoes = d.get("secoes", {})
        for s in SECOES_ETP:
            secoes.setdefault(s, "")
        d["secoes"] = secoes

        d.setdefault("lacunas", [])
        d["gerado_em"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        d["origem"] = "etp_agent_v1"

        return d
    
    # ==========================================================
    # Template vazio para fallback
    # ==========================================================
    def _get_template_vazio(self) -> dict:
        """Retorna estrutura vazia quando IA não está disponível"""
        secoes = {}
        for s in SECOES_ETP:
            secoes[s] = ""
        
        return {
            "unidade_demandante": "",
            "responsavel": "",
            "prazo_estimado": "",
            "valor_estimado": "0,00",
            "secoes": secoes,
            "lacunas": [],
            "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": "template_vazio"
        }

    # ==========================================================
    # Prompt institucional otimizado para ETP
    # ==========================================================
    def _montar_prompt(self) -> str:
        return (
            "Você é o agente especializado do TJSP em Estudos Técnicos Preliminares (ETP) "
            "conforme Lei 14.133/2021, art. 18, §1º.\n\n"
            "TAREFA: Extrair e estruturar as 27 seções obrigatórias do ETP do documento fornecido.\n\n"
            "INSTRUÇÕES CRÍTICAS:\n"
            "1. LOCALIZE no documento as seções numeradas (1 a 27)\n"
            "2. EXTRAIA o conteúdo completo de cada seção\n"
            "3. IDENTIFIQUE na seção 25 (EQUIPE DE PLANEJAMENTO):\n"
            "   - Unidade solicitante\n"
            "   - Gestor/Coordenador responsável\n"
            "4. EXTRAIA da seção 13:\n"
            "   - Valor estimado (formato: '0,00')\n"
            "5. EXTRAIA da seção 26:\n"
            "   - Prazo estimado de vigência\n"
            "6. Para cada seção, extraia o texto COMPLETO (não resuma)\n\n"
            "MAPEAMENTO DAS SEÇÕES:\n"
            "- Seção 1  → objeto\n"
            "- Seção 2  → descricao_necessidade\n"
            "- Seção 3  → previsao_pca\n"
            "- Seção 4  → planejamento_estrategico\n"
            "- Seção 5  → catalogo_padronizacao\n"
            "- Seção 6  → requisitos_contratacao\n"
            "- Seção 7  → condicoes_recebimento\n"
            "- Seção 8  → condicoes_execucao_pagamento\n"
            "- Seção 9  → garantias\n"
            "- Seção 10 → modalidade_licitacao\n"
            "- Seção 11 → estimativa_quantidades\n"
            "- Seção 12 → levantamento_mercado\n"
            "- Seção 13 → estimativa_valor\n"
            "- Seção 14 → descricao_solucao\n"
            "- Seção 15 → justificativa_parcelamento\n"
            "- Seção 16 → resultados_pretendidos\n"
            "- Seção 17 → providencias_previas\n"
            "- Seção 18 → contratacoes_correlatas\n"
            "- Seção 19 → impactos_ambientais\n"
            "- Seção 20 → possibilidade_compra_locacao\n"
            "- Seção 21 → participacao_consorcio\n"
            "- Seção 22 → vistoria_visita_tecnica\n"
            "- Seção 23 → cumprimento_resolucoes_cnj\n"
            "- Seção 24 → plano_riscos\n"
            "- Seção 25 → equipe_planejamento\n"
            "- Seção 26 → estimativa_prazo_vigencia\n"
            "- Seção 27 → avaliacao_conclusiva\n\n"
            "Responda SOMENTE com JSON no formato:\n\n"
            "{\n"
            "  \"ETP\": {\n"
            "    \"unidade_demandante\": \"[extrair da seção 25 - Unidade solicitante]\",\n"
            "    \"responsavel\": \"[extrair da seção 25 - Gestor/Coordenador]\",\n"
            "    \"prazo_estimado\": \"[extrair da seção 26]\",\n"
            "    \"valor_estimado\": \"[extrair da seção 13 - formato '0,00']\",\n"
            "    \"secoes\": {\n"
            "      \"objeto\": \"[texto completo da seção 1]\",\n"
            "      \"descricao_necessidade\": \"[texto completo da seção 2]\",\n"
            "      \"previsao_pca\": \"[texto completo da seção 3]\",\n"
            "      \"planejamento_estrategico\": \"[texto completo da seção 4]\",\n"
            "      \"catalogo_padronizacao\": \"[texto completo da seção 5]\",\n"
            "      \"requisitos_contratacao\": \"[texto completo da seção 6]\",\n"
            "      \"condicoes_recebimento\": \"[texto completo da seção 7]\",\n"
            "      \"condicoes_execucao_pagamento\": \"[texto completo da seção 8]\",\n"
            "      \"garantias\": \"[texto completo da seção 9]\",\n"
            "      \"modalidade_licitacao\": \"[texto completo da seção 10]\",\n"
            "      \"estimativa_quantidades\": \"[texto completo da seção 11]\",\n"
            "      \"levantamento_mercado\": \"[texto completo da seção 12]\",\n"
            "      \"estimativa_valor\": \"[texto completo da seção 13]\",\n"
            "      \"descricao_solucao\": \"[texto completo da seção 14]\",\n"
            "      \"justificativa_parcelamento\": \"[texto completo da seção 15]\",\n"
            "      \"resultados_pretendidos\": \"[texto completo da seção 16]\",\n"
            "      \"providencias_previas\": \"[texto completo da seção 17]\",\n"
            "      \"contratacoes_correlatas\": \"[texto completo da seção 18]\",\n"
            "      \"impactos_ambientais\": \"[texto completo da seção 19]\",\n"
            "      \"possibilidade_compra_locacao\": \"[texto completo da seção 20]\",\n"
            "      \"participacao_consorcio\": \"[texto completo da seção 21]\",\n"
            "      \"vistoria_visita_tecnica\": \"[texto completo da seção 22]\",\n"
            "      \"cumprimento_resolucoes_cnj\": \"[texto completo da seção 23]\",\n"
            "      \"plano_riscos\": \"[texto completo da seção 24]\",\n"
            "      \"equipe_planejamento\": \"[texto completo da seção 25]\",\n"
            "      \"estimativa_prazo_vigencia\": \"[texto completo da seção 26]\",\n"
            "      \"avaliacao_conclusiva\": \"[texto completo da seção 27]\"\n"
            "    },\n"
            "    \"lacunas\": [\"liste campos que não foram encontrados ou estão incompletos\"]\n"
            "  }\n"
            "}"
        )


# ==========================================================
# Função universal — chamada pelo integration_etp
# ==========================================================
def processar_etp_com_ia(conteudo_textual: str = "") -> dict:
    """
    Wrapper universal utilizado pelo integration_etp.
    Recebe texto puro e retorna:
        { "timestamp": "...", "resultado_ia": { ...ETP... } }
    """
    
    print(f"[processar_etp_com_ia] Iniciando processamento...")
    print(f"[processar_etp_com_ia] Tamanho do conteúdo: {len(conteudo_textual)} caracteres")

    if not conteudo_textual or len(conteudo_textual.strip()) < 15:
        return {
            "erro": "Conteúdo insuficiente para processamento IA.",
            "conteudo_recebido": conteudo_textual,
        }

    try:
        print("[processar_etp_com_ia] Instanciando ETPAgent...")
        agente = ETPAgent()
        
        print("[processar_etp_com_ia] Chamando agente.generate()...")
        resultado = agente.generate(conteudo_textual)
        
        print(f"[processar_etp_com_ia] Resultado obtido: {type(resultado)}")

        # Se houve erro interno → propagar
        if isinstance(resultado, dict) and "erro" in resultado:
            print(f"[processar_etp_com_ia] Erro no resultado: {resultado['erro']}")
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
                artefato="ETP",
                word_count=word_count,
                char_count=char_count,
                etapa="processamento",
                conteudo_textual=conteudo_textual
            )
        except Exception as e:
            print(f"[processar_etp_com_ia] ⚠️ Falha ao registrar auditoria: {e}")

        print("[processar_etp_com_ia] Processamento concluído com sucesso")
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "resultado_ia": resultado,
        }

    except Exception as e:
        print(f"[processar_etp_com_ia] EXCEÇÃO: {e}")
        import traceback
        traceback.print_exc()
        return {
            "erro": f"Falha ao gerar ETP: {e}",
            "conteudo_recebido": conteudo_textual[:500],
        }
