"""
guide_agent.py
--------------------------------
Agente tutor responsável por:
1. Ler o estágio atual detectado (via stage_detector).
2. Carregar perguntas do question_bank.yaml.
3. Gerar orientações dinâmicas para o usuário preencher lacunas.
"""

import os
import yaml
from .stage_detector import detect_stage, get_next_stage, get_required_fields

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "journey")

def load_questions(stage: str) -> dict:
    """
    Carrega as perguntas específicas para o estágio (DFD, ETP, TR).
    """
    try:
        path = os.path.join(BASE_DIR, "question_bank.yaml")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get(stage.lower(), {})
    except Exception as e:
        return {"error": f"Erro ao carregar question_bank.yaml: {str(e)}"}


def generate_guidance(user_input: str) -> dict:
    """
    Gera orientações personalizadas com base no estágio atual e no texto do usuário.
    """
    stage = detect_stage(user_input)
    next_stage = get_next_stage(stage)
    doc_type = next_stage.get("doc", "dfd")

    # Carregar perguntas do banco
    questions = load_questions(doc_type)
    required_fields = get_required_fields(doc_type)

    # Construir retorno
    guidance = {
        "etapa_atual": stage,
        "proximo_passo": next_stage.get("next", "fim"),
        "descricao_etapa": next_stage.get("descricao", ""),
        "documento_em_foco": doc_type.upper(),
        "campos_minimos": required_fields,
        "perguntas_recomendadas": questions
    }

    return guidance


# === Integração com a Geração de Artefatos (DocumentAgent via AgentsBridge) ===
from utils.agents_bridge import AgentsBridge

def gerar_artefato_orquestrado(stage: str, metadata: dict) -> dict:
    """
    Gera o rascunho do artefato institucional com base no estágio detectado.
    Atua como ponte entre o agente orientador (guide_agent)
    e o agente gerador de documentos (DocumentAgent).

    Parâmetros:
    - stage: string indicando o módulo (ex.: "DFD", "ETP", "TR", "EDITAL", "CONTRATO")
    - metadata: dicionário de metadados coletados dos formulários ou respostas do usuário

    Retorna:
    - dict estruturado no formato:
      {
        "modulo": "DFD",
        "secoes": { "Contexto": "...", "Necessidade": "..." },
        "lacunas": ["..."]
      }
    """
    try:
        bridge = AgentsBridge(stage)
        result = bridge.generate(metadata)
        return result
    except Exception as e:
        return {
            "erro": f"Falha ao gerar artefato ({stage}): {e}",
            "modulo": stage,
            "metadata": metadata
        }


if __name__ == "__main__":
    # Exemplo de teste local
    texto_exemplo = """
    Gostaria de registrar uma solicitação de compra de mesas de audiência
    para o Fórum de Sorocaba. As atuais estão danificadas e representam risco.
    """
    resposta = generate_guidance(texto_exemplo)
    print("Orientação do agente tutor:")
    print(resposta)

    # Exemplo adicional de uso da nova função de geração de artefato
    exemplo_metadata = {
        "unidade": "SAAB/TJSP",
        "descricao": "Aquisição de notebooks para a equipe técnica",
        "estimativa_valor": 250000
    }
    rascunho = gerar_artefato_orquestrado("DFD", exemplo_metadata)
    print("\nRascunho gerado via AgentsBridge:")
    print(rascunho)
