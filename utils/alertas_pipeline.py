# -*- coding: utf-8 -*-
"""
alertas_pipeline.py – Módulo institucional SAAB/TJSP v2025.1
==============================================================
Sistema de alertas e monitoramento automático para documentos
da jornada de contratação pública (DFD, ETP, TR, Edital, Contrato).

FUNCIONALIDADES:
- Coleta estado real dos documentos em exports/
- Detecta campos obrigatórios vazios
- Valida consistência entre documentos
- Gera alertas contextualizados por severidade
- Mantém histórico de alertas

Versão: v2025.1 (REFATORADO COMPLETO)
==============================================================
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# ======================================================
# 🔧 Configurações e Paths
# ======================================================
EXPORTS_DIR = Path(__file__).resolve().parents[1] / "exports"
ALERTAS_HISTORICO_DIR = EXPORTS_DIR / "analises" / "historico_alertas"
ALERTAS_HISTORICO_DIR.mkdir(parents=True, exist_ok=True)

# Campos obrigatórios por módulo
CAMPOS_OBRIGATORIOS = {
    "DFD": ["objeto", "justificativa", "valor_estimado", "responsavel"],
    "ETP": ["objeto", "justificativa_contratacao", "prazo_estimado", "orcamento_previsto"],
    "TR": ["objeto", "especificacao_tecnica", "prazo_execucao", "criterio_aceitacao"],
    "EDITAL": ["numero_edital", "tipo_licitacao", "objeto", "valor_estimado"],
    "CONTRATO": ["numero_contrato", "objeto", "valor_global", "vigencia", "partes_contratada"],
}

# Limites de validação
LIMITES = {
    "min_tamanho_objeto": 100,  # caracteres
    "max_divergencia_valor": 0.20,  # 20% de diferença aceitável
    "min_tamanho_justificativa": 150,
    "min_obrigacoes": 5,  # número mínimo de obrigações listadas
}


# ======================================================
# 📂 Funções de Coleta de Estado do Sistema
# ======================================================

def coletar_estado_sistema() -> Dict[str, Any]:
    """
    Varre exports/ e coleta estado atual de todos os documentos.
    
    Returns:
        Dict com estado de cada módulo (DFD, ETP, TR, EDITAL, CONTRATO)
    """
    estado = {
        "timestamp": datetime.now().isoformat(),
        "documentos": {},
        "arquivos_ausentes": [],
    }
    
    # Verificar cada módulo
    modulos = {
        "DFD": EXPORTS_DIR / "dfd_data.json",
        "ETP": EXPORTS_DIR / "etp_data.json",
        "TR": EXPORTS_DIR / "tr_data.json",
        "EDITAL": EXPORTS_DIR / "edital_data.json",
        "CONTRATO": EXPORTS_DIR / "contrato_data.json",
    }
    
    for modulo, caminho in modulos.items():
        if caminho.exists():
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    
                # Extrair campos do módulo (pode estar em diferentes estruturas)
                campos = dados.get(modulo, dados.get("campos_ai", dados))
                
                estado["documentos"][modulo] = {
                    "existe": True,
                    "caminho": str(caminho),
                    "timestamp": dados.get("timestamp", "N/A"),
                    "campos": campos,
                    "total_campos": len(campos) if isinstance(campos, dict) else 0,
                }
            except Exception as e:
                estado["documentos"][modulo] = {
                    "existe": True,
                    "erro": f"Erro ao ler arquivo: {e}",
                }
        else:
            estado["arquivos_ausentes"].append(str(caminho))
            estado["documentos"][modulo] = {
                "existe": False,
                "caminho": str(caminho),
            }
    
    return estado


def analisar_documento(modulo: str, campos: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    Analisa um documento específico e retorna lista de alertas.
    
    Args:
        modulo: Nome do módulo (DFD, ETP, TR, EDITAL, CONTRATO)
        campos: Dicionário com campos do documento
        
    Returns:
        Lista de alertas encontrados
    """
    alertas = []
    
    if not campos:
        return alertas
    
    # Verificar campos obrigatórios
    campos_obrigatorios = CAMPOS_OBRIGATORIOS.get(modulo, [])
    for campo in campos_obrigatorios:
        valor = campos.get(campo, "")
        
        if not valor or (isinstance(valor, str) and len(valor.strip()) < 10):
            alertas.append({
                "id": f"{modulo.lower()}_{campo}_vazio",
                "modulo": modulo,
                "campo": campo,
                "tipo": "Crítico",
                "severidade": "alto",
                "categoria": "Campo Obrigatório",
                "mensagem": f"Campo obrigatório '{campo}' está vazio ou muito curto no {modulo}",
                "recomendacao": f"Preencher o campo '{campo}' com informações completas e detalhadas",
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            })
    
    # Validações específicas por módulo
    if modulo == "DFD":
        alertas.extend(_validar_dfd(campos))
    elif modulo == "ETP":
        alertas.extend(_validar_etp(campos))
    elif modulo == "TR":
        alertas.extend(_validar_tr(campos))
    elif modulo == "EDITAL":
        alertas.extend(_validar_edital(campos))
    elif modulo == "CONTRATO":
        alertas.extend(_validar_contrato(campos))
    
    return alertas


def _validar_dfd(campos: Dict[str, str]) -> List[Dict[str, Any]]:
    """Validações específicas do DFD."""
    alertas = []
    
    # Validar tamanho do objeto
    objeto = campos.get("objeto", "")
    if objeto and len(objeto) < LIMITES["min_tamanho_objeto"]:
        alertas.append({
            "id": "dfd_objeto_curto",
            "modulo": "DFD",
            "campo": "objeto",
            "tipo": "Médio",
            "severidade": "medio",
            "categoria": "Qualidade do Conteúdo",
            "mensagem": f"Campo 'objeto' muito curto no DFD ({len(objeto)} caracteres, mínimo {LIMITES['min_tamanho_objeto']})",
            "recomendacao": "Detalhar melhor o objeto da contratação com especificações completas",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
    
    # Validar justificativa
    justificativa = campos.get("justificativa", "")
    if justificativa and len(justificativa) < LIMITES["min_tamanho_justificativa"]:
        alertas.append({
            "id": "dfd_justificativa_curta",
            "modulo": "DFD",
            "campo": "justificativa",
            "tipo": "Médio",
            "severidade": "medio",
            "categoria": "Qualidade do Conteúdo",
            "mensagem": f"Justificativa muito curta no DFD ({len(justificativa)} caracteres)",
            "recomendacao": "Expandir justificativa com fundamentação técnica e legal detalhada",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
    
    # Validar valor estimado
    valor = campos.get("valor_estimado", "")
    if valor and "R$" not in valor and not any(c.isdigit() for c in valor):
        alertas.append({
            "id": "dfd_valor_invalido",
            "modulo": "DFD",
            "campo": "valor_estimado",
            "tipo": "Crítico",
            "severidade": "alto",
            "categoria": "Dados Financeiros",
            "mensagem": "Valor estimado sem formatação monetária adequada no DFD",
            "recomendacao": "Informar valor no formato 'R$ XXX.XXX,XX'",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
    
    return alertas


def _validar_etp(campos: Dict[str, str]) -> List[Dict[str, Any]]:
    """Validações específicas do ETP."""
    alertas = []
    
    # Validar prazo estimado
    prazo = campos.get("prazo_estimado", "")
    if not prazo or prazo.lower() in ["a definir", "n/a", "não informado"]:
        alertas.append({
            "id": "etp_prazo_indefinido",
            "modulo": "ETP",
            "campo": "prazo_estimado",
            "tipo": "Crítico",
            "severidade": "alto",
            "categoria": "Planejamento",
            "mensagem": "Prazo estimado não definido no ETP",
            "recomendacao": "Definir prazo específico em dias, meses ou anos",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
    
    # Validar orçamento
    orcamento = campos.get("orcamento_previsto", "")
    if not orcamento or "definir" in orcamento.lower():
        alertas.append({
            "id": "etp_orcamento_indefinido",
            "modulo": "ETP",
            "campo": "orcamento_previsto",
            "tipo": "Crítico",
            "severidade": "alto",
            "categoria": "Dados Financeiros",
            "mensagem": "Orçamento previsto não definido no ETP",
            "recomendacao": "Informar valor orçamentário com base em pesquisa de preços",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
    
    return alertas


def _validar_tr(campos: Dict[str, str]) -> List[Dict[str, Any]]:
    """Validações específicas do TR."""
    alertas = []
    
    # Validar especificação técnica
    especificacao = campos.get("especificacao_tecnica", "")
    if especificacao and len(especificacao) < 200:
        alertas.append({
            "id": "tr_especificacao_curta",
            "modulo": "TR",
            "campo": "especificacao_tecnica",
            "tipo": "Médio",
            "severidade": "medio",
            "categoria": "Qualidade Técnica",
            "mensagem": f"Especificação técnica muito curta no TR ({len(especificacao)} caracteres)",
            "recomendacao": "Detalhar especificações técnicas com requisitos, quantitativos e padrões",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
    
    # Validar critério de aceitação
    criterio = campos.get("criterio_aceitacao", "")
    if not criterio or len(criterio) < 50:
        alertas.append({
            "id": "tr_criterio_ausente",
            "modulo": "TR",
            "campo": "criterio_aceitacao",
            "tipo": "Crítico",
            "severidade": "alto",
            "categoria": "Fiscalização",
            "mensagem": "Critério de aceitação ausente ou incompleto no TR",
            "recomendacao": "Definir critérios objetivos e mensuráveis para aceitação dos serviços/produtos",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
    
    return alertas


def _validar_edital(campos: Dict[str, str]) -> List[Dict[str, Any]]:
    """Validações específicas do Edital."""
    alertas = []
    
    # Validar número do edital
    numero = campos.get("numero_edital", "")
    if not numero or numero in ["N/A", "XXX/YYYY"]:
        alertas.append({
            "id": "edital_numero_invalido",
            "modulo": "EDITAL",
            "campo": "numero_edital",
            "tipo": "Crítico",
            "severidade": "alto",
            "categoria": "Identificação",
            "mensagem": "Número do edital não definido ou placeholder",
            "recomendacao": "Informar número oficial do edital no formato XXX/AAAA",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
    
    # Validar obrigações
    obrigacoes = campos.get("obrigacoes_contratada", "")
    if obrigacoes:
        num_obrigacoes = len([x for x in obrigacoes.split(";") if x.strip()])
        if num_obrigacoes < LIMITES["min_obrigacoes"]:
            alertas.append({
                "id": "edital_poucas_obrigacoes",
                "modulo": "EDITAL",
                "campo": "obrigacoes_contratada",
                "tipo": "Médio",
                "severidade": "medio",
                "categoria": "Qualidade Contratual",
                "mensagem": f"Poucas obrigações da contratada listadas ({num_obrigacoes}, mínimo {LIMITES['min_obrigacoes']})",
                "recomendacao": "Listar detalhadamente todas as obrigações e responsabilidades da contratada",
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            })
    
    return alertas


def _validar_contrato(campos: Dict[str, str]) -> List[Dict[str, Any]]:
    """Validações específicas do Contrato."""
    alertas = []
    
    # Validar número do contrato
    numero = campos.get("numero_contrato", "")
    if not numero or "XXX" in numero:
        alertas.append({
            "id": "contrato_numero_invalido",
            "modulo": "CONTRATO",
            "campo": "numero_contrato",
            "tipo": "Crítico",
            "severidade": "alto",
            "categoria": "Identificação",
            "mensagem": "Número do contrato não definido ou placeholder",
            "recomendacao": "Informar número oficial do contrato no formato XXX/AAAA",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
    
    # Validar partes
    contratada = campos.get("partes_contratada", "")
    if not contratada or len(contratada) < 50:
        alertas.append({
            "id": "contrato_contratada_incompleta",
            "modulo": "CONTRATO",
            "campo": "partes_contratada",
            "tipo": "Crítico",
            "severidade": "alto",
            "categoria": "Partes Contratuais",
            "mensagem": "Identificação da contratada incompleta no contrato",
            "recomendacao": "Incluir razão social completa, CNPJ, endereço e representante legal",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
    
    # Validar obrigações (campo crítico)
    obrigacoes = campos.get("obrigacoes_contratada", "")
    if obrigacoes and len(obrigacoes) < 500:
        alertas.append({
            "id": "contrato_obrigacoes_curtas",
            "modulo": "CONTRATO",
            "campo": "obrigacoes_contratada",
            "tipo": "Médio",
            "severidade": "medio",
            "categoria": "Qualidade Contratual",
            "mensagem": f"Obrigações da contratada muito curtas ({len(obrigacoes)} caracteres, recomendado mínimo 500)",
            "recomendacao": "Detalhar todas as obrigações com no mínimo 10-15 itens numerados",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
    
    return alertas


def validar_consistencia_entre_documentos(estado: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Valida consistência de valores, prazos e objetos entre documentos.
    
    Args:
        estado: Estado do sistema retornado por coletar_estado_sistema()
        
    Returns:
        Lista de alertas de inconsistência
    """
    alertas = []
    docs = estado.get("documentos", {})
    
    # Extrair valores de cada documento
    valores = {}
    objetos = {}
    prazos = {}
    
    for modulo, info in docs.items():
        if not info.get("existe"):
            continue
        
        campos = info.get("campos", {})
        if not campos:
            continue
        
        # Coletar valores
        for campo_valor in ["valor_estimado", "valor_global", "orcamento_previsto"]:
            if campo_valor in campos:
                val = campos[campo_valor]
                if val and isinstance(val, str):
                    # Tentar extrair número
                    import re
                    match = re.search(r'[\d.,]+', val.replace(".", "").replace(",", "."))
                    if match:
                        try:
                            valores[modulo] = float(match.group().replace(",", "."))
                        except:
                            pass
        
        # Coletar objetos
        if "objeto" in campos:
            objetos[modulo] = campos["objeto"]
        
        # Coletar prazos
        for campo_prazo in ["prazo_estimado", "prazo_execucao", "vigencia"]:
            if campo_prazo in campos:
                prazos[modulo] = campos[campo_prazo]
                break
    
    # Validar valores (DFD vs ETP vs Edital vs Contrato)
    if len(valores) >= 2:
        valores_lista = list(valores.values())
        max_val = max(valores_lista)
        min_val = min(valores_lista)
        
        if max_val > 0:
            divergencia = (max_val - min_val) / max_val
            
            if divergencia > LIMITES["max_divergencia_valor"]:
                modulos_str = ", ".join(valores.keys())
                alertas.append({
                    "id": "consistencia_valores_divergentes",
                    "modulo": "SISTEMA",
                    "tipo": "Crítico",
                    "severidade": "alto",
                    "categoria": "Consistência Entre Documentos",
                    "mensagem": f"Valores divergentes entre documentos ({modulos_str}): diferença de {divergencia*100:.1f}%",
                    "recomendacao": f"Revisar valores nos documentos. Maior: R$ {max_val:,.2f} | Menor: R$ {min_val:,.2f}",
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                })
    
    # Validar similaridade de objetos
    if len(objetos) >= 2:
        objetos_lista = list(objetos.values())
        # Comparar primeiro objeto com os demais
        obj_base = objetos_lista[0]
        for i, obj_comp in enumerate(objetos_lista[1:], 1):
            # Similaridade simples por palavras comuns
            palavras_base = set(obj_base.lower().split())
            palavras_comp = set(obj_comp.lower().split())
            
            if len(palavras_base) > 5 and len(palavras_comp) > 5:
                intersecao = len(palavras_base & palavras_comp)
                uniao = len(palavras_base | palavras_comp)
                similaridade = intersecao / uniao if uniao > 0 else 0
                
                if similaridade < 0.3:  # Menos de 30% de palavras comuns
                    modulos_str = f"{list(objetos.keys())[0]} vs {list(objetos.keys())[i]}"
                    alertas.append({
                        "id": f"consistencia_objetos_diferentes_{i}",
                        "modulo": "SISTEMA",
                        "tipo": "Médio",
                        "severidade": "medio",
                        "categoria": "Consistência Entre Documentos",
                        "mensagem": f"Objetos muito diferentes entre {modulos_str} (similaridade {similaridade*100:.0f}%)",
                        "recomendacao": "Verificar se o objeto da contratação está sendo descrito consistentemente",
                        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    })
    
    return alertas


# ======================================================
# 🚀 Função Principal: Gerar Alertas Reais
# ======================================================

def gerar_alertas_reais(salvar_historico: bool = True) -> Dict[str, Any]:
    """
    Função PRINCIPAL que gera alertas reais do sistema.
    
    Args:
        salvar_historico: Se True, salva alertas no histórico
        
    Returns:
        Dict com alertas, totais e timestamp
    """
    print("[alertas_pipeline] Iniciando geração de alertas reais...")
    
    # 1. Coletar estado do sistema
    estado = coletar_estado_sistema()
    
    # 2. Gerar alertas por documento
    todos_alertas = []
    
    for modulo, info in estado["documentos"].items():
        if info.get("existe") and info.get("campos"):
            alertas_doc = analisar_documento(modulo, info["campos"])
            todos_alertas.extend(alertas_doc)
            print(f"[alertas_pipeline] {modulo}: {len(alertas_doc)} alertas")
    
    # 3. Validar consistência entre documentos
    alertas_consistencia = validar_consistencia_entre_documentos(estado)
    todos_alertas.extend(alertas_consistencia)
    print(f"[alertas_pipeline] Consistência: {len(alertas_consistencia)} alertas")
    
    # 4. Adicionar alertas de arquivos ausentes
    for arquivo_ausente in estado["arquivos_ausentes"]:
        modulo_nome = Path(arquivo_ausente).stem.split("_")[0].upper()
        todos_alertas.append({
            "id": f"arquivo_ausente_{modulo_nome.lower()}",
            "modulo": modulo_nome,
            "tipo": "Informativo",
            "severidade": "baixo",
            "categoria": "Arquivos",
            "mensagem": f"Arquivo {Path(arquivo_ausente).name} não encontrado",
            "recomendacao": f"Processar documento {modulo_nome} para gerar o arquivo",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
    
    # 5. Calcular totais
    totais = {
        "total": len(todos_alertas),
        "critico": len([a for a in todos_alertas if a.get("tipo") == "Crítico"]),
        "medio": len([a for a in todos_alertas if a.get("tipo") == "Médio"]),
        "informativo": len([a for a in todos_alertas if a.get("tipo") == "Informativo"]),
        "alto": len([a for a in todos_alertas if a.get("severidade") == "alto"]),
        "medio_sev": len([a for a in todos_alertas if a.get("severidade") == "medio"]),
        "baixo": len([a for a in todos_alertas if a.get("severidade") == "baixo"]),
    }
    
    resultado = {
        "gerado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "timestamp": datetime.now().isoformat(),
        "totais": totais,
        "alerts": todos_alertas,
        "resumo": f"{totais['total']} alertas – {totais['critico']} críticos, {totais['medio']} médios, {totais['informativo']} informativos",
        "estado_sistema": estado,
    }
    
    # 6. Salvar no histórico
    if salvar_historico:
        try:
            caminho_historico = salvar_no_historico(resultado)
            resultado["historico_salvo"] = str(caminho_historico)
            print(f"[alertas_pipeline] ✅ Histórico salvo: {caminho_historico}")
        except Exception as e:
            print(f"[alertas_pipeline] ⚠️ Erro ao salvar histórico: {e}")
    
    print(f"[alertas_pipeline] ✅ Total: {totais['total']} alertas gerados")
    return resultado


def salvar_no_historico(resultado: Dict[str, Any]) -> Path:
    """
    Salva resultado de alertas no histórico.
    
    Args:
        resultado: Dict retornado por gerar_alertas_reais()
        
    Returns:
        Path do arquivo salvo
    """
    timestamp_arquivo = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = ALERTAS_HISTORICO_DIR / f"alertas_{timestamp_arquivo}.json"
    
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    return caminho


def carregar_historico(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Carrega últimos N registros do histórico de alertas.
    
    Args:
        limit: Número máximo de registros a carregar
        
    Returns:
        Lista de registros do histórico (mais recentes primeiro)
    """
    arquivos = sorted(ALERTAS_HISTORICO_DIR.glob("alertas_*.json"), reverse=True)
    
    historico = []
    for arquivo in arquivos[:limit]:
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                historico.append({
                    "arquivo": arquivo.name,
                    "timestamp": dados.get("gerado_em", "N/A"),
                    "totais": dados.get("totais", {}),
                    "resumo": dados.get("resumo", ""),
                })
        except Exception as e:
            print(f"[alertas_pipeline] Erro ao ler {arquivo.name}: {e}")
    
    return historico


def obter_estatisticas_historico() -> Dict[str, Any]:
    """
    Calcula estatísticas do histórico de alertas.
    
    Returns:
        Dict com estatísticas agregadas
    """
    arquivos = sorted(ALERTAS_HISTORICO_DIR.glob("alertas_*.json"))
    
    stats = {
        "total_execucoes": len(arquivos),
        "primeira_execucao": None,
        "ultima_execucao": None,
        "media_alertas_criticos": 0,
        "media_alertas_total": 0,
        "evolucao": [],
    }
    
    if not arquivos:
        return stats
    
    # Primeira e última execução
    stats["primeira_execucao"] = arquivos[0].stem.replace("alertas_", "")
    stats["ultima_execucao"] = arquivos[-1].stem.replace("alertas_", "")
    
    # Calcular médias
    total_criticos = 0
    total_geral = 0
    
    for arquivo in arquivos:
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                totais = dados.get("totais", {})
                
                total_criticos += totais.get("critico", 0)
                total_geral += totais.get("total", 0)
                
                stats["evolucao"].append({
                    "timestamp": arquivo.stem.replace("alertas_", ""),
                    "criticos": totais.get("critico", 0),
                    "total": totais.get("total", 0),
                })
        except:
            pass
    
    if len(arquivos) > 0:
        stats["media_alertas_criticos"] = total_criticos / len(arquivos)
        stats["media_alertas_total"] = total_geral / len(arquivos)
    
    return stats


# ======================================================
# 💾 Função: exportar alertas para JSON (compatibilidade)
# ======================================================
def export_alerts_json(alertas, export_path="exports/analises"):
    """
    Exporta alertas para JSON (mantida para compatibilidade).
    Use gerar_alertas_reais() para nova funcionalidade.
    """
    os.makedirs(export_path, exist_ok=True)
    file_path = os.path.join(
        export_path, f"alertas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(alertas, f, ensure_ascii=False, indent=2)
    return file_path


# ======================================================
# 🧩 Wrapper compatível: gerar_alertas(snapshot)
# ======================================================
def gerar_alertas(snapshot=None):
    """
    Wrapper para compatibilidade com Painel de Governança.
    Usa gerar_alertas_reais() internamente.
    """
    print("[alertas_pipeline] gerar_alertas() chamado (modo compatibilidade)")
    
    resultado = gerar_alertas_reais(salvar_historico=False)
    
    # Retornar apenas lista de alertas para compatibilidade
    return resultado.get("alerts", [])


