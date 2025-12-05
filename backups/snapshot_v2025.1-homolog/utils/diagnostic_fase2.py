# ==========================================================
# 🧪 Synapse Diagnostic CLI – Fase 2 (DFD → ETP)
# SAAB/TJSP – SynapseNext
# Gera: exports/diagnostic_fase2.txt
# ==========================================================

from __future__ import annotations
import os, sys, json, platform
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STREAMLIT_APP = os.path.join(ROOT, "streamlit_app")
EXPORTS = os.path.join(ROOT, "exports")
KB = os.path.join(ROOT, "knowledge_base")
PROMPTS = os.path.join(ROOT, "prompts")
VALIDATORS = os.path.join(ROOT, "validators")

# Tornar pacotes importáveis
for p in {ROOT, STREAMLIT_APP}:
    if p not in sys.path:
        sys.path.insert(0, p)

# Imports “best-effort”
def try_import(path_desc: str, import_fn):
    try:
        return import_fn(), None
    except Exception as e:
        return None, f"{path_desc}: {e}"

def check_exists(path: str) -> bool:
    return os.path.exists(path)

def verdict(flag: bool) -> str:
    return "OK" if flag else "❌"

def safe(obj):
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    if isinstance(obj, dict):
        return {k: safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [safe(x) for x in obj]
    return str(obj)

def read_file_head(path: str, n=800) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()[:n]
    except Exception:
        return ""

def line():
    return "-" * 72

def main():
    os.makedirs(EXPORTS, exist_ok=True)
    report_path = os.path.join(EXPORTS, "diagnostic_fase2.txt")

    rows = []
    add = rows.append

    # Cabeçalho
    add("SYNAPSE DIAGNOSTIC CLI – Fase 2 (DFD → ETP)")
    add(line())
    add(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    add(f"Python: {platform.python_version()}")
    add(f"ROOT: {ROOT}")
    add("")

    # 1) Estrutura de pastas
    add("[1] Estrutura de Pastas")
    for label, path in [
        ("utils", os.path.join(ROOT, "utils")),
        ("agents", os.path.join(ROOT, "agents")),
        ("knowledge_base", KB),
        ("prompts", PROMPTS),
        ("validators", VALIDATORS),
        ("streamlit_app/pages", os.path.join(STREAMLIT_APP, "pages")),
        ("exports", EXPORTS),
    ]:
        add(f" - {label:<22} {verdict(check_exists(path))}  {path}")
    add("")

    # 2) Exports existentes
    add("[2] Arquivos de Export (JSON/DOCX)")
    insumos_json = os.path.join(EXPORTS, "insumos_data.json")
    dfd_json     = os.path.join(EXPORTS, "dfd_data.json")
    etp_json     = os.path.join(EXPORTS, "ETP_teste.json")
    for label, path in [
        ("insumos_data.json", insumos_json),
        ("dfd_data.json", dfd_json),
        ("ETP_teste.json", etp_json),
    ]:
        add(f" - {label:<22} {verdict(check_exists(path))}  {path}")
    add("")

    # 3) Carregamento da Knowledge Base (ETP/legislacao)
    add("[3] Knowledge Base (leitura ETP/legislacao)")
    def _import_knowledge_loader():
        from utils.knowledge_loader import read_txt_files
        return read_txt_files
    read_txt_files, err_kb_import = try_import("utils.knowledge_loader", _import_knowledge_loader)
    if err_kb_import:
        add(f" - Import loader KB: ❌ {err_kb_import}")
    else:
        try:
            kb_preview = read_txt_files(["ETP","legislacao"], max_chars=800)
            kb_ok = bool(kb_preview.strip())
            add(f" - Leitura KB (ETP+legislacao): {verdict(kb_ok)}")
            if kb_ok:
                add("   Prévia:\n" + kb_preview[:400].replace("\n", " ") + " ...")
        except Exception as e:
            add(f" - Leitura KB: ❌ {e}")
    add("")

    # 4) Geração “seca” via agentes (DFD e ETP)
    add("[4] Agentes – geração de rascunhos (DFD, ETP)")
    def _import_agents_bridge():
        from utils.agents_bridge import AgentsBridge
        return AgentsBridge
    AgentsBridge, err_ab = try_import("utils.agents_bridge", _import_agents_bridge)
    if err_ab:
        add(f" - AgentsBridge: ❌ {err_ab}")
    else:
        # DFD
        try:
            dfd_md = {
                "unidade": "SAAB/TJSP",
                "descricao": "Aquisição de notebooks",
                "motivacao": "Renovação do parque computacional",
                "responsavel": "Eng. Carlos Mattos",
            }
            dfd_agent = AgentsBridge("DFD")
            dfd_doc = dfd_agent.generate(dfd_md)
            add(f" - DFD.generate(): {verdict(bool(dfd_doc))}")
        except Exception as e:
            add(f" - DFD.generate(): ❌ {e}")

        # ETP
        try:
            etp_md = {
                "unidade": "SAAB/TJSP",
                "objeto": "Aquisição de notebooks",
                "justificativa": "Manter a continuidade operacional",
                "responsavel": "Eng. Carlos Mattos",
            }
            # Acrescenta conhecimento, se loader OK
            if read_txt_files and not err_kb_import:
                etp_md["contexto_institucional"] = read_txt_files(["ETP","legislacao"], max_chars=5000)
            etp_agent = AgentsBridge("ETP")
            etp_doc = etp_agent.generate(etp_md)
            add(f" - ETP.generate(): {verdict(bool(etp_doc))}")
        except Exception as e:
            add(f" - ETP.generate(): ❌ {e}")

    add("")

    # 5) PROMPTS e VALIDATORS
    add("[5] PROMPTS e VALIDATORS")
    def list_dir_safe(p):
        try:
            if os.path.isdir(p):
                items = sorted(os.listdir(p))
                return items[:10], len(items)
            return [], 0
        except Exception:
            return [], 0

    prompts_items, prompts_count = list_dir_safe(PROMPTS)
    validators_items, validators_count = list_dir_safe(VALIDATORS)
    add(f" - prompts/: {verdict(prompts_count>0)}  (itens: {prompts_count})  {PROMPTS}")
    if prompts_items:
        add("   Amostra: " + ", ".join(prompts_items))
    add(f" - validators/: {verdict(validators_count>0)}  (itens: {validators_count})  {VALIDATORS}")
    if validators_items:
        add("   Amostra: " + ", ".join(validators_items))
    add("")

    # 6) Recomendações rápidas (geradas a partir do estado)
    add("[6] Recomendações")
    if not check_exists(dfd_json):
        add(" - Exporte o DFD em `exports/dfd_data.json` na página DFD para habilitar integração automática DFD→ETP.")
    if not check_exists(KB):
        add(" - Crie/alinhe a pasta knowledge_base/ com textos de apoio (ETP, DFD, TR, legislação).")
    if not check_exists(PROMPTS):
        add(" - Configure prompts/{DFD,ETP}.json para ganhos de precisão editorial.")
    add("")

    # Escreve relatório
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rows))

    print(f"✅ Relatório gerado em: {report_path}")

if __name__ == "__main__":
    main()
