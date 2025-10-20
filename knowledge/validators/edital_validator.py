# ==========================================================
# 📋 SynapseNext – Validador de Editais
# Secretaria de Administração e Abastecimento (SAAB 5.0)
# ==========================================================
# Este módulo executa a validação de editais de licitação com base
# nos padrões definidos em:
#   - knowledge/edital_checklist.yml
#   - knowledge/EDITAL.json
#   - utils/edital_loader.py
# ==========================================================

from pathlib import Path
import json
import datetime
from utils.edital_loader import carregar_checklist

# ==========================================================
# 🧭 Função principal
# ==========================================================
def validar_edital(tipo: str = "servicos", dados_edital: dict = None) -> dict:
    """
    Valida o conteúdo de um edital conforme o tipo de contratação.
    Retorna um dicionário com o resumo da validação e recomendações.

    Args:
        tipo (str): tipo de contratação (ex: servicos, obras, materiais, ti, consultoria)
        dados_edital (dict): conteúdo do edital para validação semântica (opcional)

    Returns:
        dict: estrutura consolidada com resultados de validação
    """

    # Caminhos de referência
    base_dir = Path(__file__).resolve().parents[1]
    json_path = base_dir / "knowledge" / "EDITAL.json"

    # ======================================================
    # 🔍 Verificação de existência
    # ======================================================
    if not json_path.exists():
        return {"erro": f"Arquivo EDITAL.json não encontrado em {json_path}"}

    with open(json_path, "r", encoding="utf-8") as f:
        modelo = json.load(f)

    checklist_itens = carregar_checklist(tipo)
    resultados = []

    # ======================================================
    # 🧠 Validação básica (estrutura textual)
    # ======================================================
    for item in checklist_itens:
        # Lógica simplificada: verifica se o item está no conteúdo fornecido
        if dados_edital and any(item.lower() in v.lower() for v in dados_edital.values()):
            status = "Atendido"
        else:
            status = "Pendente"

        resultados.append({
            "item": item,
            "status": status,
            "comentario": "",
            "fonte": tipo
        })

    # ======================================================
    # 📊 Geração de resumo
    # ======================================================
    total = len(resultados)
    atendidos = sum(1 for r in resultados if r["status"] == "Atendido")
    pendentes = sum(1 for r in resultados if r["status"] == "Pendente")

    resumo = {
        "tipo": tipo,
        "total_itens": total,
        "atendidos": atendidos,
        "pendentes": pendentes,
        "percentual_conformidade": round((atendidos / total) * 100, 2) if total else 0
    }

    # ======================================================
    # 🧾 Estrutura final
    # ======================================================
    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "modelo_usado": modelo["metadata"]["description"],
        "resumo": resumo,
        "resultados": resultados
    }


# ==========================================================
# 🧪 Teste rápido (CLI)
# ==========================================================
if __name__ == "__main__":
    # Exemplo de teste simples
    exemplo_edital = {
        "objeto": "Contratação de empresa especializada em serviços de limpeza e conservação",
        "justificativa": "Necessidade de manutenção predial contínua",
        "fundamentação_legal": "Lei nº 14.133/2021, art. 6º, inciso IX"
    }

    resultado = validar_edital("servicos", exemplo_edital)

    print("\n📋 RESULTADO DA VALIDAÇÃO – EDITAL")
    print("=" * 70)
    print(f"Tipo: {resultado['resumo']['tipo']}")
    print(f"Itens atendidos: {resultado['resumo']['atendidos']}/{resultado['resumo']['total_itens']}")
    print(f"Percentual de conformidade: {resultado['resumo']['percentual_conformidade']}%")
    print("\nExemplo de item validado:")
    print(resultado["resultados"][0])
