# ==========================================================
# agents/document_agent.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão: 2025-11-24 – vNext (DFD Moderno-Governança + Filtro Numérico)
# ==========================================================

from __future__ import annotations
import json
import os
import re
from datetime import datetime
from utils.ai_client import AIClient


# ==========================================================
# 🔧 (Opcional) Função interna de log em arquivo
# ==========================================================
def _registrar_log_document_agent(payload: dict) -> str:
    """
    Salva logs completos do DocumentAgent para auditoria e diagnóstico.
    (Atualmente não é usada no fluxo principal; apenas para futuro uso.)
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
# 🔒 Filtro numérico – impede valores que não constam no insumo
# ==========================================================
def _sanear_numeros_na_resposta(resposta_dict: dict, conteudo_fonte: str) -> dict:
    """
    Percorre todo o dicionário retornado pela IA e substitui números
    que NÃO estejam presentes literalmente no texto-fonte (conteudo_fonte)
    por um marcador institucional: [VALOR A DEFINIR].

    - Isso evita 'invenções' de valores.
    - Números que já apareçam no insumo são mantidos.
    """

    if not isinstance(resposta_dict, dict):
        return resposta_dict

    if not isinstance(conteudo_fonte, str):
        conteudo_fonte = str(conteudo_fonte or "")
    fonte = conteudo_fonte

    # Regex genérico para tokens numéricos (inclui decimais, milhares e percentuais)
    padrao_numeros = re.compile(r"\d[\d\.\,]*")

    def limpar_texto(txt: str) -> str:
        if not isinstance(txt, str):
            return txt

        def _substituir(match: re.Match) -> str:
            token = match.group(0)
            # Se o número aparecer literalmente no insumo, manter
            if token in fonte:
                return token
            # Caso contrário, substitui por marcador neutro
            return "[VALOR A DEFINIR]"

        return padrao_numeros.sub(_substituir, txt)

    def percorrer(obj):
        if isinstance(obj, dict):
            return {k: percorrer(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [percorrer(v) for v in obj]
        elif isinstance(obj, str):
            return limpar_texto(obj)
        else:
            return obj

    return percorrer(resposta_dict)


# ==========================================================
# 🤖 DOCUMENT AGENT – Geração de artefatos IA
# ==========================================================
class DocumentAgent:
    """
    Agente responsável por coordenar a geração de documentos formais via IA.
    Compatível com o pipeline atual e AIClient padronizado.
    """

    def __init__(self, artefato: str):
        self.artefato = artefato.upper()
        self.ai = AIClient()  # Cliente IA institucional

    # ======================================================
    # 🧠 GERAÇÃO DE CONTEÚDO VIA IA — vNext + LOGS + Filtro Numérico
    # ======================================================
    def generate(self, conteudo_base: str) -> dict:
        """
        Envia o conteúdo bruto para IA usando o prompt institucional.
        Retorna dicionário JSON estruturado, com:
        - logs básicos via print (diagnóstico)
        - filtro numérico seguro (não inventar valores)
        """

        # ============================
        # LOG 1 — registro inicial
        # ============================
        print("\n\n>>> [DocumentAgent] generate() chamado.")
        print(f">>> Artefato: {self.artefato}")
        print(f">>> Tamanho do conteúdo recebido: {len(conteudo_base or '')}")

        prompt = self._montar_prompt_institucional()

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

            # Se a IA não devolveu um dicionário, algo deu errado
            if not isinstance(resposta, dict):
                print(">>> [DocumentAgent][ERRO] Retorno não é dict.")
                return {"erro": "Resposta IA inválida ou vazia."}

            # ==================================================
            # CASO 1 – AIClient NÃO conseguiu json.loads()
            #         → devolveu {"resposta_texto": "..."}
            # ==================================================
            if "resposta_texto" in resposta:
                print(">>> [DocumentAgent] IA retornou resposta_texto (não JSON).")

                texto_bruto = (resposta.get("resposta_texto") or "").strip()
                if not texto_bruto:
                    print(">>> [DocumentAgent][ERRO] texto_bruto vazio.")
                    return {"erro": "IA não retornou conteúdo textual."}

                # Remover blocos ```json ... ``` se houver
                if texto_bruto.startswith("```json"):
                    texto_bruto = (
                        texto_bruto.replace("```json", "")
                        .replace("```", "")
                        .strip()
                    )

                # Tentativa de interpretar como JSON manualmente
                try:
                    parsed = json.loads(texto_bruto)
                    print(">>> [DocumentAgent] JSON reprocessado manualmente com sucesso.")

                    if isinstance(parsed, dict) and "DFD" in parsed:
                        resultado = parsed["DFD"]
                    else:
                        resultado = parsed

                    # Aplicar filtro numérico seguro antes de devolver
                    resultado_filtrado = _sanear_numeros_na_resposta(resultado, conteudo_base)
                    return resultado_filtrado

                except Exception as e:
                    print(f">>> [DocumentAgent][WARN] IA devolveu texto puro, sem JSON. Erro: {e}")
                    # Mesmo assim, aplica filtro numérico no texto bruto
                    resultado_texto = {"Conteúdo": texto_bruto}
                    resultado_filtrado = _sanear_numeros_na_resposta(resultado_texto, conteudo_base)
                    return resultado_filtrado

            # ==================================================
            # CASO 2 – AIClient JÁ devolveu JSON parseado
            #         (json.loads(texto) funcionou no ai_client)
            # ==================================================
            if "DFD" in resposta:
                print(">>> [DocumentAgent] JSON já contém DFD estruturado.")
                dfd = resposta.get("DFD")
                if isinstance(dfd, dict):
                    resultado = dfd
                else:
                    resultado = resposta
            else:
                # Estrutura genérica
                print(">>> [DocumentAgent] JSON genérico retornado.")
                resultado = resposta

            # Aplicar filtro numérico seguro antes de devolver
            resultado_filtrado = _sanear_numeros_na_resposta(resultado, conteudo_base)
            return resultado_filtrado

        except Exception as e:
            print(f">>> [DocumentAgent][ERRO FATAL] Exceção inesperada: {e}")
            return {"erro": f"Falha na geração do documento ({e})"}

    # ======================================================
    # 🧩 PROMPT INSTITUCIONAL – *vNext* (Modernizado)
    # ======================================================
    def _montar_prompt_institucional(self) -> str:

        # Prompt especializado para DFD
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
                "Liste informações administrativas que NÃO apareçam claramente no insumo "
                "(por exemplo, unidade demandante, responsável, prazo, valor estimado).\n\n"
                "=== FORMATO FINAL ===\n"
                "{ \"DFD\": { \"texto_narrativo\": \"...\", \"secoes\": { ... }, \"lacunas\": [] } }\n"
                "Responda APENAS com JSON válido."
            )

        # Prompt padrão para outros artefatos futuros (ETP, TR, EDITAL, CONTRATO)
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
