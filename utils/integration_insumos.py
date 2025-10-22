# ==========================================================
# 📁 integration_insumos.py
# SynapseNext – Módulo de Upload e Controle de Insumos Institucionais
# Secretaria de Administração e Abastecimento – SAAB 5.0
# ==========================================================

from datetime import datetime
from pathlib import Path
import json

def salvar_insumo(artefato: str, arquivo, usuario: str = "anônimo", descricao: str = "") -> dict:
    """
    Salva um arquivo de insumo dentro da pasta 'uploads/<artefato>/'
    e registra o evento no log de integrações.
    
    Parâmetros:
        artefato (str): Nome do artefato (ex.: DFD, ETP, TR, Edital, Contrato)
        arquivo (UploadedFile): Arquivo carregado via Streamlit
        usuario (str): Nome do usuário remetente
        descricao (str): Descrição ou contexto do envio
    
    Retorna:
        dict: Mensagem e caminho do arquivo salvo
    """
    base = Path(__file__).resolve().parents[1]
    destino_dir = base / "uploads" / artefato
    destino_dir.mkdir(parents=True, exist_ok=True)

    # Salvar o arquivo no diretório correspondente
    save_path = destino_dir / arquivo.name
    with open(save_path, "wb") as f:
        f.write(arquivo.getbuffer())

    # Gerar log do envio
    log_entry = {
        "artefato": artefato,
        "arquivo": arquivo.name,
        "usuario": usuario,
        "descricao": descricao,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "path": str(save_path)
    }

    log_dir = base / "exports" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"insumos_{datetime.now().strftime('%Y%m%d')}.json"

    if log_path.exists():
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
    else:
        logs = []

    logs.append(log_entry)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)

    return {
        "mensagem": f"Arquivo '{arquivo.name}' salvo com sucesso em '{destino_dir}'.",
        "path": str(save_path)
    }


def listar_insumos(artefato: str) -> list:
    """
    Retorna uma lista de arquivos armazenados para o artefato informado.
    """
    base = Path(__file__).resolve().parents[1]
    destino_dir = base / "uploads" / artefato
    if not destino_dir.exists():
        return []
    return [f.name for f in destino_dir.iterdir() if f.is_file()]
