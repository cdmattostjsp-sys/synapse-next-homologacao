# ==========================================
# utils/next_pipeline.py
# SynapseNext – Pipeline Consolidado (Fase Brasília + Passo 9)
# Atualizado em: 19/10/2025
# ==========================================

from datetime import datetime
import os
import json

# =========================================================
# 1️⃣ – DOCUMENTO DE FORMALIZAÇÃO DA DEMANDA (DFD)
# =========================================================
def build_dfd_markdown(respostas: dict) -> str:
    """Gera o conteúdo do Documento de Formalização da Demanda (DFD)."""
    texto = f"""# 📄 DOCUMENTO DE FORMALIZAÇÃO DA DEMANDA (DFD)

**Data de geração:** {respostas.get("timestamp", datetime.now().strftime("%d/%m/%Y %H:%M"))}

---

## 1️⃣ UNIDADE SOLICITANTE
{respostas.get("unidade", "—")}

## 2️⃣ RESPONSÁVEL PELO PEDIDO
{respostas.get("responsavel", "—")}

## 3️⃣ OBJETO DA DEMANDA
{respostas.get("objeto", "—")}

## 4️⃣ QUANTIDADE / ESCOPO
{respostas.get("quantidade_escopo", "—")}

## 5️⃣ JUSTIFICATIVA
{respostas.get("justificativa", "—")}

## 6️⃣ URGÊNCIA
{respostas.get("urgencia", "—")}

## 7️⃣ RISCOS IDENTIFICADOS
{respostas.get("riscos", "—")}

## 8️⃣ ALINHAMENTO INSTITUCIONAL
{respostas.get("alinhamento", "—")}

---

**Observação:**  
Rascunho gerado automaticamente pelo SynapseNext (Fase Brasília) – TJSP / SAAB.
"""
    return texto


# =========================================================
# 2️⃣ – ESTUDO TÉCNICO PRELIMINAR (ETP)
# =========================================================
def build_etp_markdown(respostas: dict) -> str:
    """Gera o conteúdo do Estudo Técnico Preliminar (ETP)."""
    texto = f"""# 📘 ESTUDO TÉCNICO PRELIMINAR (ETP)

**Data de geração:** {respostas.get("data", datetime.now().strftime("%d/%m/%Y"))}

---

## 1️⃣ DESCRIÇÃO DA NECESSIDADE
{respostas.get("descricao", "—")}

## 2️⃣ MOTIVAÇÃO DA CONTRATAÇÃO
{respostas.get("motivacao", "—")}

## 3️⃣ ESTIMATIVA DE CUSTOS
{respostas.get("custos", "—")}

## 4️⃣ SOLUÇÕES AVALIADAS
{respostas.get("solucoes", "—")}

## 5️⃣ RESULTADO DA ANÁLISE
{respostas.get("analise", "—")}

---

**Observação:**  
Gerado automaticamente pelo SynapseNext – conforme a IN nº 12/2025 e Lei nº 14.133/2021.
"""
    return texto


# =========================================================
# 3️⃣ – TERMO DE REFERÊNCIA (TR)
# =========================================================
def build_tr_markdown(respostas: dict) -> str:
    """Gera o conteúdo do Termo de Referência (TR)."""
    texto = f"""# 📙 TERMO DE REFERÊNCIA (TR)

**Data de geração:** {respostas.get("data", datetime.now().strftime("%d/%m/%Y"))}

---

## 1️⃣ OBJETO
{respostas.get("objeto", "—")}

## 2️⃣ JUSTIFICATIVA
{respostas.get("justificativa", "—")}

## 3️⃣ FUNDAMENTAÇÃO LEGAL
{respostas.get("fundamentacao", "—")}

## 4️⃣ DESCRIÇÃO DO OBJETO
{respostas.get("descricao", "—")}

## 5️⃣ OBRIGAÇÕES DAS PARTES
{respostas.get("obrigacoes", "—")}

## 6️⃣ PRAZOS E CONDIÇÕES
{respostas.get("prazos", "—")}

## 7️⃣ CRITÉRIOS DE ACEITAÇÃO
{respostas.get("criterios", "—")}

## 8️⃣ ESTIMATIVA DE CUSTOS
{respostas.get("custos", "—")}

---

**Observação:**  
Documento gerado automaticamente pelo SynapseNext, em conformidade com a Lei nº 14.133/2021.
"""
    return texto


# =========================================================
# 4️⃣ – EDITAL DE LICITAÇÃO
# =========================================================
def build_edital_markdown(respostas: dict) -> str:
    """Gera o conteúdo do Edital em formato Markdown."""
    texto = f"""# 🧾 EDITAL DE LICITAÇÃO

**Data de geração:** {respostas.get("data", datetime.now().strftime("%d/%m/%Y"))}

---

## 1️⃣ OBJETO
{respostas.get("objeto", "—")}

## 2️⃣ FUNDAMENTO LEGAL
{respostas.get("fundamento", "—")}

## 3️⃣ CRITÉRIOS DE JULGAMENTO
{respostas.get("criterios", "—")}

## 4️⃣ CLÁUSULAS ESSENCIAIS
{respostas.get("clausulas", "—")}

---

**Observação:**  
Rascunho institucional do Edital, conforme diretrizes do TJSP e da IN nº 12/2025.
"""
    return texto


# =========================================================
# 5️⃣ – CONTRATO (fase externa – modelo base)
# =========================================================
def build_contrato_markdown(respostas: dict) -> str:
    """Gera o conteúdo do Contrato Administrativo (fase externa)."""
    texto = f"""# 📑 CONTRATO ADMINISTRATIVO

**Data de geração:** {respostas.get("data", datetime.now().strftime("%d/%m/%Y"))}

---

## 1️⃣ PARTES CONTRATANTES
{respostas.get("partes", "—")}

## 2️⃣ OBJETO
{respostas.get("objeto", "—")}

## 3️⃣ VIGÊNCIA
{respostas.get("vigencia", "—")}

## 4️⃣ VALOR E DOTAÇÃO ORÇAMENTÁRIA
{respostas.get("valor", "—")}

## 5️⃣ OBRIGAÇÕES DAS PARTES
{respostas.get("obrigacoes", "—")}

## 6️⃣ SANÇÕES E PENALIDADES
{respostas.get("sancoes", "—")}

---

**Observação:**  
Modelo gerado automaticamente pelo SynapseNext – Fase Externa da Licitação.
"""
    return texto


# =========================================================
# 6️⃣ – CONTROLE DE EXPORTAÇÃO E LOG
# =========================================================
def exportar_arquivo(markdown_text: str, nome_arquivo: str) -> str:
    """Exporta o texto em Markdown para o diretório /exports/rascunhos/"""
    pasta = os.path.join("exports", "rascunhos")
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, f"{nome_arquivo}.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    return caminho


def registrar_log(artefato: str, usuario: str = "Sistema") -> None:
    """Registra logs simples em /exports/logs/"""
    pasta = os.path.join("exports", "logs")
    os.makedirs(pasta, exist_ok=True)
    log_path = os.path.join(pasta, "log_geracao.txt")
    with open(log_path, "a", encoding="utf-8") as log:
        log.write(
            f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] "
            f"Artefato: {artefato} | Usuário: {usuario}\n"
        )


# =========================================================
# 7️⃣ – VALIDAÇÃO SEMÂNTICA (IA TJSP)
# =========================================================
import openai
import streamlit as st

def run_semantic_validation(markdown_text: str) -> dict:
    """
    Executa uma validação semântica do conteúdo textual gerado (Markdown),
    retornando um dicionário com resumo, pontuação e sugestões.
    """

    openai.api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

    if not openai.api_key:
        return {
            "erro": "Chave da OpenAI não configurada. Verifique o arquivo secrets.toml.",
            "resumo": "",
            "pontuacao": 0,
            "sugestoes": [],
        }

    prompt = f"""
    Você é um assistente técnico do Tribunal de Justiça de São Paulo (TJSP).
    Avalie criticamente o seguinte documento administrativo (em formato Markdown):

    {markdown_text}

    Retorne um JSON com:
    - resumo: síntese objetiva (3 a 5 linhas)
    - pontuacao: grau de completude (0–100)
    - sugestoes: lista de recomendações textuais e técnicas (3 a 7 itens)
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um revisor técnico especializado em documentos administrativos do TJSP."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        raw_text = response["choices"][0]["message"]["content"]

        try:
            data = json.loads(raw_text)
        except Exception:
            data = {
                "resumo": raw_text[:400],
                "pontuacao": 50,
                "sugestoes": ["Não foi possível decodificar o JSON retornado pela IA."]
            }

        return data

    except Exception as e:
        return {
            "erro": str(e),
            "resumo": "",
            "pontuacao": 0,
            "sugestoes": [],
        }
