# ==========================================================
# 📘 SynapseNext – Módulo de Validação Semântica de Editais
# Secretaria de Administração e Abastecimento (SAAB 5.0)
# ==========================================================
# Este módulo realiza a verificação semântica dos artefatos
# de Edital, avaliando coerência, clareza e completude textual.
# ==========================================================

from typing import Tuple, List, Dict
import re
import json

# ==========================================================
# 🧠 Função principal de validação semântica
# ==========================================================

def semantic_validate_edital(doc_input: str, client) -> Tuple[float, List[Dict]]:
    """
    Executa validação semântica de um texto de Edital.

    Args:
        doc_input (str): Texto completo do edital a ser analisado.
        client: Instância do modelo de linguagem (por exemplo, OpenAI client).

    Returns:
        Tuple contendo:
            - Score de coerência geral (float)
            - Lista de alertas e recomendações (List[Dict])
    """

    # Remover espaços excessivos e normalizar o texto
    texto = re.sub(r"\s+", " ", doc_input.strip())

    # Verificações básicas de conteúdo
    alertas = []

    if len(texto) < 1000:
        alertas.append({
            "tipo": "estrutura",
            "mensagem": "O texto do edital parece incompleto ou excessivamente curto.",
            "gravidade": "alta"
        })

    # Termos obrigatórios mínimos
    obrigatorios = [
        "objeto",
        "condições de participação",
        "propostas",
        "critério de julgamento",
        "prazo de execução",
        "penalidades"
    ]

    faltantes = [t for t in obrigatorios if t.lower() not in texto.lower()]
    if faltantes:
        alertas.append({
            "tipo": "conteúdo",
            "mensagem": f"Os seguintes tópicos obrigatórios não foram identificados: {', '.join(faltantes)}.",
            "gravidade": "média"
        })

    # Exemplo de análise com IA (mock para ambiente offline)
    try:
        # Se houver client configurado, realiza uma chamada real
        if client:
            prompt = (
                "Analise o edital abaixo e aponte inconsistências, incoerências ou omissões "
                "relevantes. Forneça um score de coerência (0-100) e recomendações práticas.\n\n"
                f"Texto:\n{texto}"
            )

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um avaliador técnico especializado em licitações públicas."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
            )

            content = response.choices[0].message.content
            match = re.search(r"(\d{1,3})", content)
            score = float(match.group(1)) if match else 75.0

            alertas.append({
                "tipo": "ia",
                "mensagem": "Análise semântica concluída com sucesso pelo modelo de linguagem.",
                "gravidade": "informativa"
            })

        else:
            score = 70.0
            alertas.append({
                "tipo": "simulado",
                "mensagem": "Validação realizada em modo offline (sem client ativo).",
                "gravidade": "baixa"
            })

    except Exception as e:
        score = 60.0
        alertas.append({
            "tipo": "erro",
            "mensagem": f"Falha ao executar análise semântica: {e}",
            "gravidade": "alta"
        })

    return score, alertas


# ==========================================================
# 🧩 Compatibilidade retroativa – SynapseNext vNext
# ==========================================================
# Este alias mantém compatibilidade com versões anteriores
# do sistema que chamavam esta função como "validar_semantica_edital".
# No padrão atual (vNext), o nome oficial é semantic_validate_edital.
# ==========================================================

validar_semantica_edital = semantic_validate_edital
