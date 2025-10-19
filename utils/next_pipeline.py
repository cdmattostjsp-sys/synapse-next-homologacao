# ==========================================
# utils/next_pipeline.py
# SynapseNext – Pipeline Consolidado (Fase Brasília)
# Atualizado em: 19/10/2025
# ==========================================

from datetime import datetime

# =========================================================
# 1️⃣ – DOCUMENTO DE FORMALIZAÇÃO DA DEMANDA (DFD)
# =========================================================
def build_dfd_markdown(respostas: dict) -> str:
    """Gera o conteúdo do Documento de Formalização da Demanda (DFD)."""
    texto = f"""# 📄 DOCUMENTO DE FORMALIZAÇÃO DA DEMANDA (DFD)

**Data de geração:** {respostas.get("data", datetime.now().strftime("%d/%m/%Y"))}

---

## 1️⃣ UNIDADE SOLICITANTE
{respostas.get("unidade", "—")}

## 2️⃣ RESPONSÁVEL PELO PEDIDO
{respostas.get("responsavel", "—")}

## 3️⃣ OBJETO DA DEMANDA
{respostas.get("objeto", "—")}

## 4️⃣ JUSTIFICATIVA
{respostas.get("justificativa", "—")}

## 5️⃣ RESULTADOS ESPERADOS
{respostas.get("resultados", "—")}

## 6️⃣ PRAZO ESTIMADO
{respostas.get("prazo", "—")}

---

**Observação:**  
Este rascunho é gerado automaticamente pelo SynapseNext (Fase Brasília)  
e segue o modelo padrão definido pela Secretaria de Administração e Abastecimento – TJSP.
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
Rascunho gerado automaticamente pelo SynapseNext (Fase Brasília)  
com base nas diretrizes da Instrução Normativa nº 12/2025.
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
Documento gerado automaticamente pelo SynapseNext,  
em conformidade com a Lei nº 14.133/2021 e a IN nº 12/2025 – TJSP.
"""
    return texto


# =========================================================
# 4️⃣ – EDITAL DE LICITAÇÃO (NOVO)
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
Este rascunho é gerado automaticamente pelo SynapseNext (Fase Brasília)  
e serve de base para elaboração do edital final, conforme diretrizes do TJSP e da IN nº 12/2025.
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

## 7️⃣ ASSINATURAS
{respostas.get("assinaturas", "—")}

---

**Observação:**  
Modelo de contrato gerado pelo SynapseNext, compatível com a Lei nº 14.133/2021  
e a IN nº 12/2025 – TJSP (fase externa do processo licitatório).
"""
    return texto


# =========================================================
# 6️⃣ – CONTROLE DE EXPORTAÇÃO E LOG
# =========================================================
def exportar_arquivo(markdown_text: str, nome_arquivo: str) -> str:
    """
    Exporta o texto em Markdown para o diretório /exports/rascunhos/
    Retorna o caminho completo do arquivo salvo.
    """
    import os

    pasta = os.path.join("exports", "rascunhos")
    os.makedirs(pasta, exist_ok=True)

    caminho_arquivo = os.path.join(pasta, f"{nome_arquivo}.md")

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(markdown_text)

    return caminho_arquivo


def registrar_log(artefato: str, usuario: str = "Sistema") -> None:
    """
    Cria ou atualiza um arquivo de log para registrar o histórico
    de geração de artefatos no SynapseNext.
    """
    import os

    pasta = os.path.join("exports", "logs")
    os.makedirs(pasta, exist_ok=True)

    log_path = os.path.join(pasta, "log_geracao.txt")

    with open(log_path, "a", encoding="utf-8") as log:
        log.write(
            f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] "
            f"Artefato gerado: {artefato} | Usuário: {usuario}\n"
        )
