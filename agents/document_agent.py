# ==========================================================
# agents/document_agent.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão: 2025-11-24 – vNext (DFD Moderno-Governança – Modo Estrito, Perfil Intermediário, Híbrido)
# ==========================================================

from __future__ import annotations
import json
import os
from datetime import datetime
from utils.ai_client import AIClient


# ==========================================================
# 🔧 Função interna de log institucional (diagnóstico)
# ==========================================================
def _registrar_log_document_agent(payload: dict) -> str:
    """
    Salva logs completos do DocumentAgent para auditoria e diagnóstico.
    Não interfere no fluxo principal (falhas de log são silenciosas).
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
        # Não deixa o log quebrar o agente
        return f"ERRO_LOG: {e}"


# ==========================================================
# 🤖 DOCUMENT AGENT – Geração de artefatos IA
# ==========================================================
class DocumentAgent:
    """
    Agente responsável por coordenar a geração de documentos formais via IA.
    Compatível com o pipeline atual (DFD, ETP, TR, Edital etc.).
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

        prompt = self._montar_prompt_institucional()

        log_payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "artefato": self.artefato,
            "conteudo_input_len": len(conteudo_base or ""),
            "conteudo_input_preview": (conteudo_base[:1500] if conteudo_base else ""),
            "prompt_usado": prompt,
        }

        try:
            resposta = self.ai.ask(
                prompt=prompt,
                conteudo=conteudo_base,
                artefato=self.artefato,
            )

            # Guarda a resposta bruta para auditoria
            log_payload["resposta_bruta"] = resposta

            # --------------------------------------------------
            # Validação básica
            # --------------------------------------------------
            if not isinstance(resposta, dict):
                return {"erro": "Resposta IA inválida ou vazia."}

            # Se a IA retornou erro interno, apenas repassa
            if "erro" in resposta:
                return resposta

            # ==================================================
            # CASO 1 – AIClient NÃO conseguiu json.loads()
            #         e devolveu {"resposta_texto": "..."}
            # ==================================================
            if "resposta_texto" in resposta:
                texto_bruto = (resposta.get("resposta_texto") or "").strip()

                if not texto_bruto:
                    return {"erro": "IA não retornou conteúdo textual."}

                # Limpeza de blocos ```json
                if texto_bruto.startswith("```"):
                    texto_bruto = (
                        texto_bruto.replace("```json", "")
                        .replace("```", "")
                        .strip()
                    )

                # Tenta interpretar como JSON
                try:
                    parsed = json.loads(texto_bruto)
                    log_payload["json_reprocessado"] = parsed

                    # Se vier no formato {"DFD": {...}}
                    if isinstance(parsed, dict) and "DFD" in parsed:
                        dfd = parsed.get("DFD") or {}
                        dfd = self._normalizar_dfd(dfd)
                        log_payload["dfd_normalizado"] = dfd
                        return dfd

                    return parsed

                except Exception:
                    # Conteúdo não era JSON → retorna como texto bruto
                    return {"Conteúdo": texto_bruto}

            # ==================================================
            # CASO 2 – AIClient JÁ devolveu JSON parseado
            #         (json.loads(texto) funcionou)
            # ==================================================
            if isinstance(resposta, dict) and "DFD" in resposta:
                dfd = resposta.get("DFD") or {}
                if isinstance(dfd, dict):
                    dfd = self._normalizar_dfd(dfd)
                    log_payload["dfd_normalizado"] = dfd
                    return dfd

            # Caso geral: já é a estrutura final
            return resposta

        finally:
            # Sempre registra o log (mesmo em caso de erro)
            _registrar_log_document_agent(log_payload)

    # ======================================================
    # 🔧 Normalização da estrutura DFD (formato híbrido)
    # ======================================================
    def _normalizar_dfd(self, dfd: dict) -> dict:
        """
        Garante que o DFD tenha o formato híbrido esperado:
          - texto_narrativo
          - secoes (11 seções)
          - lacunas
          - tradicional.{descricao_necessidade, motivacao}
          - descricao_necessidade e motivacao também no topo (compatibilidade)
        """

        if not isinstance(dfd, dict):
            return {}

        tradicional = dfd.get("tradicional")
        if isinstance(tradicional, dict):
            desc_trad = tradicional.get("descricao_necessidade")
            mot_trad = tradicional.get("motivacao")

            # Se existirem em 'tradicional' e não estiverem no topo, sobe
            if desc_trad and not dfd.get("descricao_necessidade"):
                dfd["descricao_necessidade"] = desc_trad
            if mot_trad and not dfd.get("motivacao"):
                dfd["motivacao"] = mot_trad

        # Garante presença de chaves principais, mesmo que vazias
        dfd.setdefault("texto_narrativo", "")
        dfd.setdefault("secoes", {})
        dfd.setdefault("lacunas", [])

        return dfd

    # ======================================================
    # 🧩 PROMPT INSTITUCIONAL – DFD (Modo Estrito, Perfil Intermediário)
    # ======================================================
    def _montar_prompt_institucional(self) -> str:

        # ======================================================
        # 📌 PROMPT ESPECIALIZADO PARA DFD
        # ======================================================
        if self.artefato == "DFD":
            return (
                "Você é o agente de Formalização da Demanda (DFD) da Secretaria de Administração e Abastecimento "
                "(SAAB) do Tribunal de Justiça do Estado de São Paulo (TJSP). "
                "Com base EXCLUSIVAMENTE no texto fornecido (insumo), produza um DFD completo, em linguagem "
                "administrativa, formal, impessoal e alinhada às práticas da SAAB/TJSP.\n\n"

                "=== OBJETIVO GERAL ===\n"
                "Gerar um DFD estruturado, claro e objetivo, contendo:\n"
                "1) Um texto narrativo consolidado numerado de 1 a 11 (campo 'texto_narrativo').\n"
                "2) Um objeto 'secoes' com as 11 seções formais do modelo Moderno-Governança.\n"
                "3) Um objeto 'tradicional' com 'descricao_necessidade' e 'motivacao'.\n"
                "4) Uma lista 'lacunas' com informações administrativas RELEVANTES que NÃO aparecem no insumo.\n\n"

                "=== MODO ESTRITO (NÃO INVENTAR DADOS) ===\n"
                "• NÃO invente dados administrativos ou técnicos específicos que não estejam presentes no insumo.\n"
                "• NÃO crie: nomes de pessoas, cargos, CPFs, CNPJs, números de processo, prazos, datas, valores exatos, "
                "quantidades, marcas, modelos, capacidades, códigos de contratos, ou qualquer dado sensível.\n"
                "• Você PODE generalizar conceitos (ex.: 'empresa especializada', 'equipamentos de ar-condicionado'), "
                "mas SEM inventar detalhes numéricos ou nomes.\n\n"

                "=== TEXTO NARRATIVO (campo 'texto_narrativo') ===\n"
                "• Produza um texto de síntese numerado de 1 a 11.\n"
                "• CADA número (1., 2., 3., ..., 11.) deve iniciar em um NOVO PARÁGRAFO, separado por quebra de linha dupla.\n"
                "• Cada item deve ter DE 1 A 2 parágrafos curtos (no máximo 6 frases por parágrafo).\n"
                "• NÃO use bullets, listas com hífen, marcadores gráficos ou emojis. Apenas texto corrido numerado.\n"
                "• Evite repetir exatamente o mesmo texto em itens diferentes.\n\n"

                "=== SEÇÕES OBRIGATÓRIAS (objeto 'secoes') ===\n"
                "O objeto 'secoes' DEVE conter exatamente estas 11 chaves, com texto objetivo em cada uma:\n"
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
                "Para cada seção:\n"
                "• Produza DE 1 A 2 parágrafos curtos, alinhados ao insumo, sem floreios.\n"
                "• NÃO copie integralmente o mesmo parágrafo em seções diferentes.\n"
                "• Mantenha foco administrativo: contexto, necessidade, resultados, riscos, critérios.\n\n"

                "=== BLOCO TRADICIONAL (objeto 'tradicional') ===\n"
                "Crie também um objeto 'tradicional' com a síntese tradicional do DFD, contendo:\n"
                "- 'descricao_necessidade': uma síntese objetiva do problema e da necessidade da contratação.\n"
                "- 'motivacao': combinação de objetivos, resultados esperados, benefícios e justificativa legal.\n"
                "Use o mesmo estilo dos DFDs institucionais: texto direto, sem excesso de detalhes, com 1 a 3 parágrafos.\n\n"

                "Além disso, reproduza esses mesmos textos como campos de topo em 'DFD':\n"
                "- 'descricao_necessidade' e 'motivacao' no nível de 'DFD' (espelho de 'tradicional').\n\n"

                "=== LACUNAS (lista 'lacunas') ===\n"
                "A lista 'lacunas' deve conter frases curtas indicando apenas INFORMAÇÕES ADMINISTRATIVAS relevantes "
                "que NÃO aparecem claramente no insumo. Exemplos de lacunas válidas:\n"
                "- 'Unidade demandante não identificada no insumo.'\n"
                "- 'Responsável pela demanda não identificado no insumo.'\n"
                "- 'Prazo estimado para a contratação não indicado no insumo.'\n"
                "- 'Estimativa de valor da contratação não localizada no insumo.'\n"
                "NÃO inclua lacunas que pertençam a estágios futuros (Termo de Referência, Edital, Contrato ou critérios "
                "detalhados de julgamento de propostas).\n\n"

                "=== ESTILO E TOM ===\n"
                "• Linguagem formal, impessoal e administrativa, alinhada aos exemplos da SAAB/TJSP.\n"
                "• Frases diretas, sem adjetivos desnecessários.\n"
                "• Evite termos genéricos vazios (como 'extremamente relevante', 'altamente crítico', etc.).\n\n"

                "=== FORMATO EXATO DA RESPOSTA (APENAS JSON) ===\n"
                "Retorne APENAS um JSON válido, seguindo este modelo (estrutura):\n"
                "{\n"
                "  \"DFD\": {\n"
                "    \"texto_narrativo\": \"1. ...\\n\\n2. ...\\n\\n3. ...\",\n"
                "    \"secoes\": {\n"
                "      \"Contexto Institucional\": \"...\",\n"
                "      \"Diagnóstico da Situação Atual\": \"...\",\n"
                "      \"Fundamentação da Necessidade\": \"...\",\n"
                "      \"Objetivos da Contratação\": \"...\",\n"
                "      \"Escopo Inicial da Demanda\": \"...\",\n"
                "      \"Resultados Esperados\": \"...\",\n"
                "      \"Benefícios Institucionais\": \"...\",\n"
                "      \"Justificativa Legal\": \"...\",\n"
                "      \"Riscos da Não Contratação\": \"...\",\n"
                "      \"Requisitos Mínimos\": \"...\",\n"
                "      \"Critérios de Sucesso\": \"...\"\n"
                "    },\n"
                "    \"tradicional\": {\n"
                "      \"descricao_necessidade\": \"...\",\n"
                "      \"motivacao\": \"...\"\n"
                "    },\n"
                "    \"descricao_necessidade\": \"...\",\n"
                "    \"motivacao\": \"...\",\n"
                "    \"lacunas\": [\"...\"]\n"
                "  }\n"
                "}\n\n"
                "Não inclua comentários, explicações, texto fora do JSON ou qualquer outro conteúdo."
            )

        # ======================================================
        # PROMPT PADRÃO (ETP, TR, EDITAL, CONTRATO) – futuro
        # ======================================================
        return (
            f"Você é o agente institucional do TJSP responsável pelo artefato {self.artefato}. "
            "Produza um documento administrativo formal e retorne APENAS JSON estruturado."
        )


# ======================================================
# 🔌 Função pública usada pelo pipeline DFD
# ======================================================
def processar_dfd_com_ia(conteudo_textual: str = "") -> dict:
    """
    Função chamada pelo pipeline de INSUMOS.
    Recebe o texto extraído do PDF e retorna o DFD estruturado.
    """

    if not conteudo_textual or len(conteudo_textual.strip()) < 15:
        return {"erro": "Conteúdo insuficiente para processamento IA."}

    agente = DocumentAgent("DFD")
    resultado = agente.generate(conteudo_textual)

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "resultado_ia": resultado,
    }
