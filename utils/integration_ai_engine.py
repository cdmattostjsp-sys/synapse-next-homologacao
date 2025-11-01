# utils/integration_ai_engine.py

```python
# ==============================
# utils/integration_ai_engine.py
# SynapseNext – SAAB / TJSP – IA Ativa v3
# ==============================
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Dict, Any, Optional

import streamlit as st
from openai import OpenAI

# Preferir bibliotecas já presentes no projeto
try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

try:
    import docx2txt
except Exception:
    docx2txt = None

# ----------------------------
# ⚙️ Configuração do cliente
# ----------------------------
_client: Optional[OpenAI] = None

def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # não logar
    return _client

# ----------------------------
# 🧰 Utilidades de extração
# ----------------------------

def _extract_txt_from_pdf(file) -> str:
    """Extrai texto de PDF usando PyMuPDF; fallback para bytes vazios."""
    if fitz is None:
        return ""
    try:
        data = file.read() if hasattr(file, "read") else file
        if isinstance(data, bytes):
            doc = fitz.open(stream=data, filetype="pdf")
        else:
            doc = fitz.open(stream=data.getvalue(), filetype="pdf")
        texts = []
        for page in doc:
            texts.append(page.get_text())
        return "\n".join(texts)
    except Exception:
        return ""


def _extract_txt_from_docx(file) -> str:
    if docx2txt is None:
        return ""
    try:
        data = file.read() if hasattr(file, "read") else file
        if isinstance(data, bytes):
            import io
            bio = io.BytesIO(data)
            return docx2txt.process(bio)
        return docx2txt.process(file)
    except Exception:
        return ""


def _extract_txt_from_plain(file) -> str:
    try:
        data = file.read() if hasattr(file, "read") else file
        if isinstance(data, bytes):
            return data.decode("utf-8", errors="ignore")
        return str(data)
    except Exception:
        return ""


def extrair_texto(uploaded_file) -> str:
    """Detecta tipo e extrai o texto bruto do arquivo enviado."""
    if uploaded_file is None:
        return ""
    name = getattr(uploaded_file, "name", "")
    lower = name.lower()
    if lower.endswith(".pdf"):
        return _extract_txt_from_pdf(uploaded_file)
    if lower.endswith(".docx"):
        return _extract_txt_from_docx(uploaded_file)
    if lower.endswith(".txt"):
        return _extract_txt_from_plain(uploaded_file)
    # tentativa genérica
    return _extract_txt_from_plain(uploaded_file)

# ----------------------------
# 📦 Modelo de retorno
# ----------------------------

@dataclass
class IAResultado:
    modulo: str
    campos: Dict[str, Any]
    lacunas: list[str]
    inferido_de: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "modulo": self.modulo,
            "campos": self.campos,
            "lacunas": self.lacunas,
            "inferido_de": self.inferido_de,
        }

# ----------------------------
# 🧠 Prompt institucional
# ----------------------------

def _montar_prompt(modulo: str, texto: str, metadados: Dict[str, Any]) -> list[Dict[str, str]]:
    schema_comum = {
        "DFD": [
            "objeto",
            "justificativa",
            "resultados_esperados",
            "requisitos_minimos",
            "criterio_julgamento",
            "prazo_execucao",
            "base_legal",
        ],
        "ETP": [
            "objeto",
            "motivacao",
            "alternativas",
            "vantagem_da_soluçao",
            "riscos",
            "estimativa_custos",
            "criterios_aceitacao",
            "base_legal",
        ],
        "TR": [
            "objeto",
            "escopo_detalhado",
            "requisitos_tecnicos",
            "condicoes_entrega",
            "indicadores_de_desempenho",
            "criterio_julgamento",
            "prazos",
            "garantias",
            "base_legal",
        ],
    }

    chaves = schema_comum.get(modulo.upper(), [])

    system = (
        "Você é redator técnico do SAAB/TJSP, especialista na Lei 14.133/2021. "
        "Seu trabalho é inferir campos administrativos a partir de insumos fornecidos. "
        "Responda ESTRITAMENTE em JSON válido (um único objeto) no schema solicitado. "
        "Se um campo não puder ser inferido com segurança, deixe-o vazio e liste em 'lacunas'. "
        "Não adicione comentários fora do JSON."
    )

    user = (
        f"MÓDULO ALVO: {modulo}\n"
        f"METADADOS DO FORMULÁRIO (preferência sobre o texto):\n{json.dumps(metadados, ensure_ascii=False)}\n\n"
        f"EXTRATO DO INSUMO (texto extraído):\n{texto[:12000]}\n\n"
        f"RETORNE JSON COM AS CHAVES: {chaves}. "
        "Inclua também 'lacunas' (lista de pendências) e 'evidencias' (trechos do texto que suportam as inferências)."
    )

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

# ----------------------------
# 🔄 Pós-processamento / validação
# ----------------------------

def _coagir_json(conteudo: str) -> Dict[str, Any]:
    """Extrai o primeiro objeto JSON válido do conteúdo retornado."""
    # Tentativa direta
    try:
        return json.loads(conteudo)
    except Exception:
        pass

    # Regex ampla (lenta porém segura para respostas curtas)
    m = re.search(r"\{[\s\S]*\}", conteudo)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    # Fallback
    return {"raw": conteudo}

# ----------------------------
# 🧩 Função pública principal
# ----------------------------

def processar_insumo(
    uploaded_file,
    tipo_artefato: str,
    metadados_form: Optional[Dict[str, Any]] = None,
    filename: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Processa um insumo e retorna um dicionário JSON com campos inferidos.
    Side-effect: preenche st.session_state["<modulo>_campos_ai"].
    """
    modulo = (tipo_artefato or "").upper()
    metadados_form = metadados_form or {}

    # 1) Extração de texto
    texto = extrair_texto(uploaded_file)

    # 2) Chamada à OpenAI com response_format JSON
    try:
        client = _get_client()
        messages = _montar_prompt(modulo, texto, metadados_form)

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.2,
            response_format={"type": "json_object"},
            max_tokens=2000,
        )
        conteudo = resp.choices[0].message.content
    except Exception as e:
        # Fallback: JSON mínimo indicando falha
        conteudo = json.dumps({
            "modulo": modulo,
            "campos": {},
            "lacunas": [f"Falha na chamada de IA: {str(e)}"],
            "evidencias": [],
        }, ensure_ascii=False)

    # 3) Validação/parse
    parsed = _coagir_json(conteudo)
    if "campos" not in parsed:
        parsed["campos"] = {}
    if "lacunas" not in parsed:
        parsed["lacunas"] = []

    # 4) Montagem do objeto padrão
    resultado = IAResultado(
        modulo=modulo,
        campos=parsed.get("campos", {}),
        lacunas=parsed.get("lacunas", []),
        inferido_de={
            "arquivo": filename or getattr(uploaded_file, "name", None),
            "bytes": True,
        },
    ).to_dict()

    # 5) Side-effect seguro no session_state
    try:
        key_map = {
            "DFD": "dfd_campos_ai",
            "ETP": "etp_campos_ai",
            "TR": "tr_campos_ai",
        }
        target_key = key_map.get(modulo)
        if target_key:
            st.session_state[target_key] = resultado.get("campos", {})
    except Exception:
        # Nunca interromper o fluxo por falha de estado
        pass

    return resultado
```

---

## 📌 Patch 1 – pages/01_🔧 Insumos.py (adição do botão “Pré-preencher com IA (engine v3)”)

```python
# Topo do arquivo – novas importações
from utils.integration_ai_engine import processar_insumo as processar_insumo_ia

# ... Dentro do layout, após upload e seleção do artefato ...
if arquivo and st.button("⚙️ Pré-preencher com IA (engine v3)"):
    with st.spinner("Processando insumo com IA institucional..."):
        try:
            metadados_form = {
                "usuario": usuario,
                "descricao": descricao,
                "artefato": artefato,
            }
            doc_json = processar_insumo_ia(
                arquivo,
                artefato,
                metadados_form=metadados_form,
                filename=getattr(arquivo, "name", None),
            )
            st.success("Campos pré-preenchidos (session_state atualizado).")
            with st.expander("📄 Prévia JSON (IA v3)", expanded=False):
                st.json(doc_json)
        except Exception as e:
            st.warning(f"Falha no pré-preenchimento por IA: {e}")
            st.info("Mantendo valores atuais do formulário (fallback).")
```

---

## 📌 Patch 2 – páginas de DFD / ETP / TR (carregar session_state no formulário)

> Inserir após a construção do formulário, antes de exibir os campos (exemplo DFD; repetir com as chaves de cada módulo):

```python
# DFD – leitura do estado
valores_ai = st.session_state.get("dfd_campos_ai", {})

# Aplicar valores nos widgets mantendo edição do usuário
objeto = st.text_area("Objeto", value=valores_ai.get("objeto", ""))
justificativa = st.text_area("Justificativa", value=valores_ai.get("justificativa", ""))
criterio = st.selectbox(
    "Critério de julgamento",
    ["Menor preço", "Técnica e preço", "Maior desconto", "Maior retorno"],
    index=0,
)
if valores_ai.get("criterio_julgamento"):
    try:
        idx = ["Menor preço", "Técnica e preço", "Maior desconto", "Maior retorno"].index(valores_ai["criterio_julgamento"])
        st.session_state["_dfd_idx_criterio"] = idx
    except ValueError:
        pass
```

---

## 🧪 Patch 3 – teste rápido (dev)

```python
# pages/99_DEV_Teste_IA_Engine.py (opcional para homologação)
import streamlit as st
from utils.integration_ai_engine import processar_insumo

st.title("Teste rápido – IA Engine v3")
up = st.file_uploader("Suba PDF/DOCX/TXT")
mod = st.selectbox("Módulo", ["DFD", "ETP", "TR"])
if st.button("Testar") and up:
    out = processar_insumo(up, mod, metadados_form={"ambiente":"DEV"}, filename=up.name)
    st.json(out)
```

---

## 🔒 Observações de segurança

* Uso exclusivo de `st.secrets["OPENAI_API_KEY"]`.
* `response_format={"type": "json_object"}` força JSON estrito.
* `try/except` em toda etapa crítica + nunca quebrar UI por falha de sessão.
* Sem logging de conteúdo sensível.

## ✅ Critérios de aceite (fase 1)

* Botão em **Insumos** popula `st.session_state["dfd_campos_ai"|"etp_campos_ai"|"tr_campos_ai"]`.
* Formulários passam a abrir com os valores sugeridos pelo engine.
* JSON exibe `lacunas` e `evidencias` quando faltarem dados.
* Falhas de IA não interrompem o fluxo (mensagens amigáveis + fallback).
