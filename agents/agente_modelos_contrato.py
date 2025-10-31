# ==========================================================
# 🤖 Agente_ModelosContrato
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================
# Responsável por criar, revisar e validar os modelos contratuais
# armazenados em knowledge/contrato_models/, com base no
# Manual de Contratos TJSP 2025 e Lei nº 14.133/2021.
# ==========================================================

import os
import json
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# ==========================================================
# ⚙️ Configuração do cliente OpenAI
# ==========================================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("openai_api_key")
client = OpenAI(api_key=OPENAI_API_KEY)

# ==========================================================
# 📚 Caminhos institucionais
# ==========================================================
BASE_PATH = Path(__file__).resolve().parents[1]
MODELOS_PATH = BASE_PATH / "knowledge" / "contrato_models"
MANUALS_PATH = BASE_PATH / "knowledge" / "manuals"
LOGS_PATH = BASE_PATH / "data" / "logs"
LOGS_PATH.mkdir(parents=True, exist_ok=True)

# ==========================================================
# 🧾 Funções utilitárias
# ==========================================================
def registrar_log(mensagem: str):
    """Registra evento no log institucional do agente."""
    log_file = LOGS_PATH / "modelos_contrato.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensagem}\n")


def ler_modelos_existentes():
    """Lê todos os modelos da pasta knowledge/contrato_models/"""
    modelos = {}
    if MODELOS_PATH.exists():
        for arq in MODELOS_PATH.glob("*.txt"):
            modelos[arq.name] = arq.read_text(encoding="utf-8")
    return modelos


def ler_manual_contratos():
    """Localiza o Manual TJSP 2025, se presente."""
    for arquivo in MANUALS_PATH.glob("Manual_Contratos_TJSP_*.pdf"):
        return arquivo
    return None


# ==========================================================
# 🧠 Função principal – Validação e Criação de Modelos
# ==========================================================
def analisar_modelos_existentes():
    """
    Avalia todos os modelos da pasta contrato_models,
    verificando completude, linguagem institucional e aderência
    às cláusulas obrigatórias previstas no Manual TJSP 2025.
    """
    modelos = ler_modelos_existentes()
    if not modelos:
        registrar_log("Nenhum modelo encontrado em contrato_models/.")
        return "Nenhum modelo encontrado."

    resultados = []

    for nome, conteudo in modelos.items():
        prompt = f"""
Você é o Agente de Governança Contratual do TJSP.
Analise o modelo a seguir e verifique:
1. Se contém as cláusulas obrigatórias do art. 92 da Lei 14.133/2021;
2. Se utiliza linguagem institucional compatível com o Manual de Contratos TJSP 2025;
3. Se apresenta conformidade estrutural com os modelos SAAB;
4. Sugira, se necessário, ajustes pontuais de redação, mas sem alterar o sentido jurídico.

Modelo:
\"\"\"{conteudo}\"\"\"

Retorne um JSON no formato:
{{
  "modelo": "{nome}",
  "status": "conforme" ou "ajustes necessários",
  "clausulas_identificadas": [...],
  "observacoes": "...",
  "sugestoes": "..."
}}
"""
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é o Agente de Governança Contratual da SAAB/TJSP."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            resultado = response.choices[0].message.content.strip()
            resultados.append(json.loads(resultado))
        except Exception as e:
            registrar_log(f"Erro ao analisar {nome}: {e}")
            resultados.append({"modelo": nome, "erro": str(e)})

    registrar_log("Análise de conformidade concluída.")
    return resultados


# ==========================================================
# 🧩 Função – Criar novo modelo de contrato
# ==========================================================
def criar_novo_modelo(tipo: str, descricao: str = ""):
    """
    Gera um novo modelo de contrato conforme o tipo especificado,
    com base no Manual TJSP 2025 e boas práticas do TCE-SP.
    """
    tipo = tipo.lower().replace(" ", "_")
    nome_arquivo = f"modelo_contrato_{tipo}.txt"
    destino = MODELOS_PATH / nome_arquivo

    manual = ler_manual_contratos()
    referencia_manual = f"O manual institucional está disponível em: {manual}" if manual else "Manual não localizado."

    prompt = f"""
Crie um modelo textual completo de contrato administrativo do TJSP
para o tipo: {tipo.upper()}.

O texto deve seguir o padrão do Manual de Contratos TJSP 2025,
incluir as cláusulas essenciais (objeto, vigência, valor, fiscalização,
sanções, rescisão e foro) e adotar a redação formal SAAB/TJSP.

Descrição adicional: {descricao}

{referencia_manual}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é especialista em contratos administrativos do TJSP."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        conteudo = response.choices[0].message.content.strip()
        destino.write_text(conteudo, encoding="utf-8")
        registrar_log(f"Novo modelo criado: {nome_arquivo}")
        return f"✅ Novo modelo criado: {nome_arquivo}"
    except Exception as e:
        registrar_log(f"Erro ao criar modelo {tipo}: {e}")
        return f"❌ Erro ao criar modelo {tipo}: {e}"


# ==========================================================
# 🧾 Execução direta (CLI opcional)
# ==========================================================
if __name__ == "__main__":
    print("🔍 Executando análise de modelos contratuais...")
    resultado = analisar_modelos_existentes()
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
