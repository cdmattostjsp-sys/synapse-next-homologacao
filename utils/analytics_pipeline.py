# -*- coding: utf-8 -*-
"""
utils/analytics_pipeline.py
---------------------------
Sistema de Análise de Desempenho v2025.1 – SynapseNext
Coleta métricas REAIS dos documentos processados e gera análises temporais.

FUNCIONALIDADES:
- Coleta dados de auditoria (word_count, timestamps, char_count)
- Extrai métricas de coerência entre documentos
- Calcula conformidade legal e status dos artefatos
- Gera séries temporais de evolução
- Persiste histórico para análise de tendências

DADOS COLETADOS:
- Auditoria: exports/auditoria/audit_*.jsonl
- Coerência: exports/analises/relatorio_coerencia_*.json
- Conformidade: exports/analises/insights_metrics_*.json
- Documentos: exports/*_data.json

AUTOR: Sistema SynapseNext TJSP
DATA: Dezembro/2025
VERSÃO: v2025.1
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import re
from collections import defaultdict

# ======================================================
# 📁 Configuração de Diretórios
# ======================================================
EXPORTS_DIR = Path("exports")
AUDITORIA_DIR = EXPORTS_DIR / "auditoria"
ANALISES_DIR = EXPORTS_DIR / "analises"
HISTORICO_DESEMPENHO_DIR = ANALISES_DIR / "historico_desempenho"

# Criar diretórios se não existirem
HISTORICO_DESEMPENHO_DIR.mkdir(parents=True, exist_ok=True)

# ======================================================
# 📊 Constantes
# ======================================================
MODULOS = ["DFD", "ETP", "TR", "EDITAL", "CONTRATO"]


# ======================================================
# 🔍 Função: Coletar Métricas de Auditoria
# ======================================================
def coletar_metricas_auditoria() -> Dict[str, Any]:
    """
    Coleta métricas de auditoria dos arquivos JSONL.
    
    Lê todos os arquivos audit_*.jsonl e extrai:
    - word_count por artefato
    - char_count por artefato
    - timestamps de processamento
    - evolução temporal
    
    Returns:
        Dict com histórico de eventos por artefato e série temporal
    """
    print("[analytics_pipeline] Coletando métricas de auditoria...")
    
    eventos_por_artefato = defaultdict(list)
    eventos_temporais = []
    
    # Listar todos os arquivos de auditoria
    if not AUDITORIA_DIR.exists():
        print(f"[analytics_pipeline] ⚠️  Diretório de auditoria não existe: {AUDITORIA_DIR}")
        return {"eventos_por_artefato": {}, "eventos_temporais": [], "total_eventos": 0}
    
    arquivos_audit = sorted(AUDITORIA_DIR.glob("audit_*.jsonl"))
    
    for arquivo in arquivos_audit:
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha:
                        continue
                    
                    try:
                        evento = json.loads(linha)
                        artefato = evento.get("artefato", "DESCONHECIDO")
                        
                        # Adicionar ao histórico do artefato
                        eventos_por_artefato[artefato].append({
                            "timestamp": evento.get("timestamp"),
                            "word_count": evento.get("word_count", 0),
                            "char_count": evento.get("char_count", 0),
                            "etapa": evento.get("etapa", "processamento"),
                            "sha256": evento.get("sha256", "")[:10],
                        })
                        
                        # Adicionar ao histórico temporal geral
                        eventos_temporais.append({
                            "timestamp": evento.get("timestamp"),
                            "artefato": artefato,
                            "word_count": evento.get("word_count", 0),
                            "char_count": evento.get("char_count", 0),
                        })
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"[analytics_pipeline] Erro ao ler {arquivo.name}: {e}")
    
    # Ordenar eventos temporais por timestamp
    eventos_temporais.sort(key=lambda x: x.get("timestamp", ""))
    
    resultado = {
        "eventos_por_artefato": dict(eventos_por_artefato),
        "eventos_temporais": eventos_temporais,
        "total_eventos": len(eventos_temporais),
    }
    
    print(f"[analytics_pipeline] ✅ {len(eventos_temporais)} eventos coletados de auditoria")
    return resultado


# ======================================================
# 📈 Função: Calcular Evolução Temporal
# ======================================================
def calcular_evolucao_temporal(eventos_temporais: List[Dict], dias: int = 30) -> Dict[str, Any]:
    """
    Calcula evolução temporal de métricas agregadas por dia.
    
    Args:
        eventos_temporais: Lista de eventos com timestamp, word_count, artefato
        dias: Número de dias para análise (padrão 30)
        
    Returns:
        Dict com séries temporais agregadas por dia
    """
    print(f"[analytics_pipeline] Calculando evolução temporal ({dias} dias)...")
    
    if not eventos_temporais:
        return {
            "volume_por_dia": [],
            "word_count_por_dia": [],
            "distribuicao_artefatos_por_dia": [],
        }
    
    # Agrupar eventos por dia
    eventos_por_dia = defaultdict(lambda: {"volume": 0, "word_count_total": 0, "artefatos": defaultdict(int)})
    
    for evento in eventos_temporais:
        timestamp_str = evento.get("timestamp", "")
        if not timestamp_str:
            continue
        
        try:
            # Extrair data (YYYY-MM-DD)
            data = timestamp_str.split("T")[0] if "T" in timestamp_str else timestamp_str.split(" ")[0]
            
            eventos_por_dia[data]["volume"] += 1
            eventos_por_dia[data]["word_count_total"] += evento.get("word_count", 0)
            eventos_por_dia[data]["artefatos"][evento.get("artefato", "DESCONHECIDO")] += 1
        except:
            continue
    
    # Ordenar por data
    datas_ordenadas = sorted(eventos_por_dia.keys())
    
    # Limitar aos últimos N dias
    if len(datas_ordenadas) > dias:
        datas_ordenadas = datas_ordenadas[-dias:]
    
    # Construir séries temporais
    volume_por_dia = [{"data": data, "valor": eventos_por_dia[data]["volume"]} for data in datas_ordenadas]
    
    word_count_por_dia = [
        {"data": data, "valor": eventos_por_dia[data]["word_count_total"]}
        for data in datas_ordenadas
    ]
    
    # Distribuição de artefatos por dia (para gráfico de linhas múltiplas)
    distribuicao_artefatos = defaultdict(list)
    for data in datas_ordenadas:
        for modulo in MODULOS:
            distribuicao_artefatos[modulo].append({
                "data": data,
                "valor": eventos_por_dia[data]["artefatos"].get(modulo, 0)
            })
    
    resultado = {
        "volume_por_dia": volume_por_dia,
        "word_count_por_dia": word_count_por_dia,
        "distribuicao_artefatos": dict(distribuicao_artefatos),
    }
    
    print(f"[analytics_pipeline] ✅ Evolução temporal calculada para {len(datas_ordenadas)} dias")
    return resultado


# ======================================================
# 🧩 Função: Coletar Métricas de Coerência
# ======================================================
def coletar_metricas_coerencia() -> Dict[str, Any]:
    """
    Coleta métricas de coerência entre documentos.
    
    Lê arquivos relatorio_coerencia_*.json e extrai:
    - coerencia_global
    - comparações par-a-par
    - timestamps
    
    Returns:
        Dict com histórico de coerência e última medição
    """
    print("[analytics_pipeline] Coletando métricas de coerência...")
    
    if not ANALISES_DIR.exists():
        return {"historico_coerencia": [], "ultima_coerencia": None}
    
    arquivos_coerencia = sorted(ANALISES_DIR.glob("relatorio_coerencia_*.json"))
    
    historico = []
    for arquivo in arquivos_coerencia:
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                
                # Extrair timestamp do nome do arquivo (formato: relatorio_coerencia_YYYYMMDD_HHMMSS.json)
                match = re.search(r'(\d{8})_(\d{6})', arquivo.stem)
                if match:
                    data_str = match.group(1)
                    hora_str = match.group(2)
                    timestamp = f"{data_str[:4]}-{data_str[4:6]}-{data_str[6:8]}T{hora_str[:2]}:{hora_str[2:4]}:{hora_str[4:6]}"
                else:
                    timestamp = datetime.now().isoformat()
                
                historico.append({
                    "timestamp": timestamp,
                    "coerencia_global": dados.get("coerencia_global", 0),
                    "comparacoes": dados.get("comparacoes", {}),
                })
        except Exception as e:
            print(f"[analytics_pipeline] Erro ao ler {arquivo.name}: {e}")
    
    # Ordenar por timestamp
    historico.sort(key=lambda x: x["timestamp"])
    
    ultima_coerencia = historico[-1] if historico else None
    
    print(f"[analytics_pipeline] ✅ {len(historico)} registros de coerência coletados")
    return {
        "historico_coerencia": historico,
        "ultima_coerencia": ultima_coerencia,
    }


# ======================================================
# 📋 Função: Coletar Métricas de Conformidade
# ======================================================
def coletar_metricas_conformidade() -> Dict[str, Any]:
    """
    Coleta métricas de conformidade legal dos artefatos.
    
    Lê arquivos insights_metrics_*.json gerados pelo analytics_engine_vNext
    
    Returns:
        Dict com métricas de conformidade e artefatos
    """
    print("[analytics_pipeline] Coletando métricas de conformidade...")
    
    if not ANALISES_DIR.exists():
        return {"conformidade_percentual": 0, "artefatos_completos": 0, "artefatos_incompletos": 0}
    
    arquivos_metrics = sorted(ANALISES_DIR.glob("insights_metrics_*.json"))
    
    if not arquivos_metrics:
        return {"conformidade_percentual": 0, "artefatos_completos": 0, "artefatos_incompletos": 0}
    
    # Usar o arquivo mais recente
    arquivo_recente = arquivos_metrics[-1]
    
    try:
        with open(arquivo_recente, "r", encoding="utf-8") as f:
            dados = json.load(f)
            
            indicadores = dados.get("indicadores", [])
            
            resultado = {}
            for indicador in indicadores:
                nome = indicador.get("Indicador", "")
                valor = indicador.get("Valor", 0)
                
                if "Conformidade Legal" in nome:
                    resultado["conformidade_percentual"] = valor
                elif "Artefatos Completos" in nome:
                    resultado["artefatos_completos"] = valor
                elif "Artefatos Incompletos" in nome:
                    resultado["artefatos_incompletos"] = valor
                elif "Artefatos Ausentes" in nome:
                    resultado["artefatos_ausentes"] = valor
                elif "Total de Artefatos" in nome:
                    resultado["total_artefatos"] = valor
            
            print(f"[analytics_pipeline] ✅ Métricas de conformidade coletadas de {arquivo_recente.name}")
            return resultado
    except Exception as e:
        print(f"[analytics_pipeline] Erro ao ler {arquivo_recente.name}: {e}")
        return {"conformidade_percentual": 0, "artefatos_completos": 0, "artefatos_incompletos": 0}


# ======================================================
# 📄 Função: Coletar Estatísticas de Documentos
# ======================================================
def coletar_estatisticas_documentos() -> Dict[str, Any]:
    """
    Coleta estatísticas dos documentos processados em exports/.
    
    Lê arquivos *_data.json e extrai informações básicas
    
    Returns:
        Dict com estatísticas dos documentos existentes
    """
    print("[analytics_pipeline] Coletando estatísticas de documentos...")
    
    documentos_encontrados = []
    total_campos = 0
    
    for modulo in MODULOS:
        arquivo = EXPORTS_DIR / f"{modulo.lower()}_data.json"
        if arquivo.exists():
            try:
                with open(arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    
                    # Extrair campos (pode estar em diferentes estruturas)
                    campos = None
                    if modulo.upper() in dados:
                        campos = dados[modulo.upper()]
                    elif "campos_ai" in dados:
                        campos = dados["campos_ai"]
                    else:
                        campos = dados
                    
                    num_campos = len(campos) if isinstance(campos, dict) else 0
                    total_campos += num_campos
                    
                    documentos_encontrados.append({
                        "modulo": modulo,
                        "arquivo": arquivo.name,
                        "num_campos": num_campos,
                        "timestamp": datetime.fromtimestamp(arquivo.stat().st_mtime).isoformat(),
                    })
            except Exception as e:
                print(f"[analytics_pipeline] Erro ao ler {arquivo.name}: {e}")
    
    resultado = {
        "documentos_processados": len(documentos_encontrados),
        "total_campos_extraidos": total_campos,
        "documentos": documentos_encontrados,
    }
    
    print(f"[analytics_pipeline] ✅ {len(documentos_encontrados)} documentos encontrados")
    return resultado


# ======================================================
# 🚀 Função Principal: Gerar Métricas de Desempenho
# ======================================================
def gerar_metricas_desempenho(dias: int = 30, salvar_historico: bool = True) -> Dict[str, Any]:
    """
    Função PRINCIPAL que gera métricas completas de desempenho do sistema.
    
    Args:
        dias: Número de dias para análise temporal (padrão 30)
        salvar_historico: Se True, salva resultado no histórico
        
    Returns:
        Dict completo com todas as métricas de desempenho
    """
    print("[analytics_pipeline] ========================================")
    print("[analytics_pipeline] 📊 Iniciando análise de desempenho...")
    print("[analytics_pipeline] ========================================")
    
    # 1. Coletar métricas de auditoria
    metricas_auditoria = coletar_metricas_auditoria()
    
    # 2. Calcular evolução temporal
    evolucao_temporal = calcular_evolucao_temporal(
        metricas_auditoria["eventos_temporais"],
        dias=dias
    )
    
    # 3. Coletar métricas de coerência
    metricas_coerencia = coletar_metricas_coerencia()
    
    # 4. Coletar métricas de conformidade
    metricas_conformidade = coletar_metricas_conformidade()
    
    # 5. Coletar estatísticas de documentos
    estatisticas_docs = coletar_estatisticas_documentos()
    
    # 6. Calcular métricas agregadas atuais
    total_word_count = sum(
        e.get("word_count", 0) 
        for e in metricas_auditoria["eventos_temporais"]
    )
    
    word_count_medio = (
        total_word_count / metricas_auditoria["total_eventos"]
        if metricas_auditoria["total_eventos"] > 0
        else 0
    )
    
    # 7. Distribuição de eventos por artefato
    distribuicao_artefatos = {}
    for modulo in MODULOS:
        eventos_modulo = metricas_auditoria["eventos_por_artefato"].get(modulo, [])
        
        if eventos_modulo:
            word_counts = [e.get("word_count", 0) for e in eventos_modulo]
            distribuicao_artefatos[modulo] = {
                "total_eventos": len(eventos_modulo),
                "word_count_total": sum(word_counts),
                "word_count_medio": sum(word_counts) / len(word_counts) if word_counts else 0,
                "ultimo_processamento": eventos_modulo[-1].get("timestamp") if eventos_modulo else None,
            }
        else:
            distribuicao_artefatos[modulo] = {
                "total_eventos": 0,
                "word_count_total": 0,
                "word_count_medio": 0,
                "ultimo_processamento": None,
            }
    
    # 8. Construir resultado consolidado
    resultado = {
        "gerado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "timestamp": datetime.now().isoformat(),
        "periodo_analise_dias": dias,
        
        "resumo": {
            "total_eventos": metricas_auditoria["total_eventos"],
            "total_word_count": total_word_count,
            "word_count_medio": round(word_count_medio, 2),
            "documentos_processados": estatisticas_docs["documentos_processados"],
            "conformidade_percentual": metricas_conformidade.get("conformidade_percentual", 0),
            "coerencia_global_atual": (
                metricas_coerencia["ultima_coerencia"]["coerencia_global"]
                if metricas_coerencia["ultima_coerencia"]
                else 0
            ),
        },
        
        "evolucao_temporal": {
            "volume_eventos": evolucao_temporal.get("volume_por_dia", []),
            "word_count_total": evolucao_temporal.get("word_count_por_dia", []),
            "distribuicao_modulos": evolucao_temporal.get("distribuicao_artefatos", {}),
        },
        
        "coerencia": {
            "historico": metricas_coerencia["historico_coerencia"],
            "ultima_medicao": metricas_coerencia["ultima_coerencia"],
        },
        
        "conformidade": metricas_conformidade,
        
        "distribuicao_artefatos": distribuicao_artefatos,
        
        "documentos": estatisticas_docs,
    }
    
    # 9. Salvar no histórico
    if salvar_historico:
        try:
            caminho_historico = salvar_metricas_historico(resultado)
            resultado["historico_salvo"] = str(caminho_historico)
            print(f"[analytics_pipeline] ✅ Histórico salvo: {caminho_historico}")
        except Exception as e:
            print(f"[analytics_pipeline] ⚠️  Erro ao salvar histórico: {e}")
    
    print("[analytics_pipeline] ========================================")
    print(f"[analytics_pipeline] ✅ Análise concluída: {metricas_auditoria['total_eventos']} eventos processados")
    print("[analytics_pipeline] ========================================")
    
    return resultado


# ======================================================
# 💾 Função: Salvar Métricas no Histórico
# ======================================================
def salvar_metricas_historico(metricas: Dict[str, Any]) -> Path:
    """
    Salva métricas de desempenho no histórico.
    
    Args:
        metricas: Dict retornado por gerar_metricas_desempenho()
        
    Returns:
        Path do arquivo salvo
    """
    timestamp_arquivo = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = HISTORICO_DESEMPENHO_DIR / f"metricas_desempenho_{timestamp_arquivo}.json"
    
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(metricas, f, ensure_ascii=False, indent=2)
    
    return caminho


# ======================================================
# 📜 Função: Carregar Histórico de Desempenho
# ======================================================
def carregar_historico_desempenho(limit: int = 30) -> List[Dict[str, Any]]:
    """
    Carrega últimos N registros do histórico de métricas.
    
    Args:
        limit: Número máximo de registros a carregar
        
    Returns:
        Lista de registros do histórico (mais recentes primeiro)
    """
    arquivos = sorted(HISTORICO_DESEMPENHO_DIR.glob("metricas_desempenho_*.json"), reverse=True)
    
    historico = []
    for arquivo in arquivos[:limit]:
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                historico.append({
                    "arquivo": arquivo.name,
                    "timestamp": dados.get("gerado_em", "N/A"),
                    "total_eventos": dados.get("resumo", {}).get("total_eventos", 0),
                    "conformidade": dados.get("resumo", {}).get("conformidade_percentual", 0),
                    "coerencia": dados.get("resumo", {}).get("coerencia_global_atual", 0),
                })
        except Exception as e:
            print(f"[analytics_pipeline] Erro ao ler {arquivo.name}: {e}")
    
    return historico


# ======================================================
# 📊 Função: Obter Estatísticas do Histórico
# ======================================================
def obter_estatisticas_historico() -> Dict[str, Any]:
    """
    Calcula estatísticas agregadas do histórico de métricas.
    
    Returns:
        Dict com estatísticas agregadas
    """
    arquivos = sorted(HISTORICO_DESEMPENHO_DIR.glob("metricas_desempenho_*.json"))
    
    stats = {
        "total_execucoes": len(arquivos),
        "primeira_execucao": None,
        "ultima_execucao": None,
        "media_eventos": 0,
        "media_conformidade": 0,
        "media_coerencia": 0,
        "tendencia_eventos": [],
    }
    
    if not arquivos:
        return stats
    
    # Primeira e última execução
    stats["primeira_execucao"] = arquivos[0].stem.replace("metricas_desempenho_", "")
    stats["ultima_execucao"] = arquivos[-1].stem.replace("metricas_desempenho_", "")
    
    # Calcular médias
    total_eventos = 0
    total_conformidade = 0
    total_coerencia = 0
    
    for arquivo in arquivos:
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                resumo = dados.get("resumo", {})
                
                eventos = resumo.get("total_eventos", 0)
                conformidade = resumo.get("conformidade_percentual", 0)
                coerencia = resumo.get("coerencia_global_atual", 0)
                
                total_eventos += eventos
                total_conformidade += conformidade
                total_coerencia += coerencia
                
                stats["tendencia_eventos"].append({
                    "timestamp": arquivo.stem.replace("metricas_desempenho_", ""),
                    "eventos": eventos,
                    "conformidade": conformidade,
                    "coerencia": coerencia,
                })
        except:
            pass
    
    if len(arquivos) > 0:
        stats["media_eventos"] = round(total_eventos / len(arquivos), 2)
        stats["media_conformidade"] = round(total_conformidade / len(arquivos), 2)
        stats["media_coerencia"] = round(total_coerencia / len(arquivos), 2)
    
    return stats


# ======================================================
# 🧪 Execução isolada de teste
# ======================================================
if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTE DO SISTEMA DE ANÁLISE DE DESEMPENHO")
    print("=" * 60)
    
    metricas = gerar_metricas_desempenho(dias=30, salvar_historico=True)
    
    print("\n📊 RESUMO DAS MÉTRICAS:")
    print(f"  - Total de eventos: {metricas['resumo']['total_eventos']}")
    print(f"  - Word count total: {metricas['resumo']['total_word_count']}")
    print(f"  - Word count médio: {metricas['resumo']['word_count_medio']}")
    print(f"  - Documentos processados: {metricas['resumo']['documentos_processados']}")
    print(f"  - Conformidade: {metricas['resumo']['conformidade_percentual']}%")
    print(f"  - Coerência global: {metricas['resumo']['coerencia_global_atual']}%")
    
    print("\n✅ Teste concluído!")
