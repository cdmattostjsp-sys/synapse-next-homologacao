#!/bin/bash
# ==========================================================
# SynapseNext - Verificação Pós-Patch IA -> DFD (versão ASCII)
# ==========================================================

echo ""
echo "Iniciando verificação pós-patch IA -> DFD"
echo "=========================================================="

LOGFILE="exports/logs/diagnostic_post_patch.txt"
JSON_PATH="exports/insumos/json/DFD_ultimo.json"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[1/5] Verificando existência do arquivo DFD_ultimo.json..."
if [ -f "$JSON_PATH" ]; then
    echo "OK: Arquivo encontrado em $JSON_PATH"
else
    echo "ERRO: Arquivo DFD_ultimo.json não encontrado."
    exit 1
fi

echo ""
echo "[2/5] Validando estrutura principal do JSON..."
if grep -q '"DFD"' "$JSON_PATH" && grep -q '"objeto"' "$JSON_PATH" && grep -q '"necessidadeContratacao"' "$JSON_PATH"; then
    echo "OK: Estrutura principal detectada."
else
    echo "ALERTA: Estrutura parcial ou inesperada."
fi

echo ""
echo "[3/5] Verificando presença da resposta IA..."
if grep -q '"resultado_ia"' "$JSON_PATH" && grep -q '"resposta_texto"' "$JSON_PATH"; then
    echo "OK: Resposta IA presente."
else
    echo "ERRO: Campo resultado_ia ou resposta_texto ausente."
fi

echo ""
echo "[4/5] Testando leitura simulada pelo módulo DFD..."
if grep -q '"DFD"' "$JSON_PATH"; then
    echo "OK: Módulo DFD deve conseguir carregar os dados."
else
    echo "ALERTA: Bloco DFD não localizado no JSON."
fi

echo ""
echo "[5/5] Gerando relatório de diagnóstico..."
{
    echo "=========================================================="
    echo "SynapseNext - Diagnóstico Pós-Patch IA -> DFD"
    echo "Data/Hora: $TIMESTAMP"
    echo "----------------------------------------------------------"
    echo "Arquivo JSON: $JSON_PATH"
    echo ""
    grep -E '"artefato"|"arquivo_origem"|"gerado_em"' "$JSON_PATH" | head -n 3
    echo ""
    if grep -q '"DFD"' "$JSON_PATH"; then
        echo "Estrutura DFD: OK"
    else
        echo "Estrutura DFD: AUSENTE"
    fi
    if grep -q '"resposta_texto"' "$JSON_PATH"; then
        echo "Resposta IA: OK"
    else
        echo "Resposta IA: AUSENTE"
    fi
    echo "=========================================================="
} > "$LOGFILE"

cat "$LOGFILE"
echo ""
echo "Fim da verificação pós-patch."
echo "=========================================================="
