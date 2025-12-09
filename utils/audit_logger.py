# -*- coding: utf-8 -*-
"""
utils/audit_logger.py
---------------------
Sistema de Auditoria Automática v2025.1 – SynapseNext

Registra eventos de processamento de documentos para análise de desempenho.

ESTRUTURA DE EVENTOS:
- timestamp: ISO 8601 (YYYY-MM-DDTHH:MM:SS)
- artefato: DFD, ETP, TR, EDITAL, CONTRATO
- word_count: número de palavras do documento
- char_count: número de caracteres do documento
- etapa: processamento, validacao, exportacao
- sha256: hash do conteúdo (para rastreabilidade)

ARMAZENAMENTO:
- exports/auditoria/audit_YYYYMMDD.jsonl (1 evento por linha)

AUTOR: Sistema SynapseNext TJSP
DATA: Dezembro/2025
VERSÃO: v2025.1
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional

# Diretório de auditoria
WORKSPACE_ROOT = Path(__file__).parent.parent
AUDITORIA_DIR = WORKSPACE_ROOT / "exports" / "auditoria"


def registrar_evento_auditoria(
    artefato: str,
    word_count: int,
    char_count: int,
    etapa: str = "processamento",
    conteudo_textual: Optional[str] = None
) -> bool:
    """
    Registra evento de auditoria no arquivo JSONL.
    
    Args:
        artefato: Nome do artefato (DFD, ETP, TR, EDITAL, CONTRATO)
        word_count: Número de palavras do documento
        char_count: Número de caracteres do documento
        etapa: Etapa do processamento (processamento, validacao, exportacao)
        conteudo_textual: Texto completo (opcional, para gerar hash)
    
    Returns:
        bool: True se registrado com sucesso, False caso contrário
    """
    try:
        # Criar diretório se não existir
        AUDITORIA_DIR.mkdir(parents=True, exist_ok=True)
        
        # Nome do arquivo baseado na data atual
        hoje = datetime.now().strftime("%Y%m%d")
        arquivo_audit = AUDITORIA_DIR / f"audit_{hoje}.jsonl"
        
        # Gerar hash SHA256 (se conteúdo fornecido)
        sha256_hash = "não-disponível"
        if conteudo_textual:
            sha256_hash = hashlib.sha256(conteudo_textual.encode('utf-8')).hexdigest()[:16]
        
        # Criar evento
        evento = {
            "timestamp": datetime.now().isoformat(),
            "artefato": artefato.upper(),
            "word_count": word_count,
            "char_count": char_count,
            "etapa": etapa,
            "sha256": sha256_hash
        }
        
        # Anexar ao arquivo JSONL (append mode)
        with open(arquivo_audit, "a", encoding="utf-8") as f:
            f.write(json.dumps(evento, ensure_ascii=False) + "\n")
        
        print(f"[audit_logger] ✅ Evento registrado: {artefato} ({word_count} palavras)")
        return True
        
    except Exception as e:
        print(f"[audit_logger] ⚠️ Erro ao registrar auditoria: {e}")
        return False


def obter_estatisticas_auditoria(dias: int = 30) -> dict:
    """
    Retorna estatísticas dos eventos de auditoria dos últimos N dias.
    
    Args:
        dias: Número de dias para análise
    
    Returns:
        dict com total_eventos, por_artefato, por_etapa
    """
    try:
        if not AUDITORIA_DIR.exists():
            return {
                "total_eventos": 0,
                "por_artefato": {},
                "por_etapa": {},
                "periodo_dias": dias
            }
        
        from collections import defaultdict
        stats = {
            "total_eventos": 0,
            "por_artefato": defaultdict(int),
            "por_etapa": defaultdict(int),
            "periodo_dias": dias
        }
        
        # Ler todos os arquivos audit_*.jsonl
        for arquivo in sorted(AUDITORIA_DIR.glob("audit_*.jsonl")):
            with open(arquivo, "r", encoding="utf-8") as f:
                for linha in f:
                    try:
                        evento = json.loads(linha.strip())
                        stats["total_eventos"] += 1
                        stats["por_artefato"][evento["artefato"]] += 1
                        stats["por_etapa"][evento["etapa"]] += 1
                    except:
                        continue
        
        # Converter defaultdict para dict normal
        stats["por_artefato"] = dict(stats["por_artefato"])
        stats["por_etapa"] = dict(stats["por_etapa"])
        
        return stats
        
    except Exception as e:
        print(f"[audit_logger] ⚠️ Erro ao obter estatísticas: {e}")
        return {
            "total_eventos": 0,
            "por_artefato": {},
            "por_etapa": {},
            "periodo_dias": dias
        }


def limpar_auditoria_antiga(dias_retencao: int = 90) -> int:
    """
    Remove arquivos de auditoria mais antigos que N dias.
    
    Args:
        dias_retencao: Número de dias para manter
    
    Returns:
        int: Número de arquivos removidos
    """
    try:
        if not AUDITORIA_DIR.exists():
            return 0
        
        from datetime import timedelta
        data_limite = datetime.now() - timedelta(days=dias_retencao)
        removidos = 0
        
        for arquivo in AUDITORIA_DIR.glob("audit_*.jsonl"):
            # Extrair data do nome do arquivo (audit_YYYYMMDD.jsonl)
            try:
                data_str = arquivo.stem.replace("audit_", "")
                data_arquivo = datetime.strptime(data_str, "%Y%m%d")
                
                if data_arquivo < data_limite:
                    arquivo.unlink()
                    removidos += 1
                    print(f"[audit_logger] 🗑️ Removido: {arquivo.name}")
            except:
                continue
        
        if removidos > 0:
            print(f"[audit_logger] ✅ {removidos} arquivo(s) antigo(s) removido(s)")
        
        return removidos
        
    except Exception as e:
        print(f"[audit_logger] ⚠️ Erro ao limpar auditoria antiga: {e}")
        return 0
