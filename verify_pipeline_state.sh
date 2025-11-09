#!/bin/bash
# ==========================================================
# SynapseNext – Script de Verificação de Estado do Pipeline IA/DFD
# Autor: Diagnostic Synapse
# Data: 09.NOV.2025
# ==========================================================
# Este script realiza verificações automáticas para confirmar:
# 1️⃣ Presença e integridade dos logs do cliente IA
# 2️⃣ Existência de JSONs gerados em exports/insumos/json
# 3️⃣ Existência do comando fitz.open() no módulo integration_insumos.py
# 4️⃣ Estrutura e conteúdo básico do JSON DFD_ultimo.json
# ==========================================================

echo ""
echo "🧠 Iniciando verificação do estado atual do pipeline IA/DFD..."
echo "=========================================================="

# ----------------------------------------------------------
# 1️⃣ Verificar logs recentes do cliente IA
# ----------------------------------------------------------
echo ""
echo "📂 [1/5] Verificando logs de execução do cliente IA..."
LOG_PATH="exports/logs/"
if ls -lh "$LOG_PATH" | grep -q "ai_client"; then
    echo "✅ Logs encontrados:"
    ls -lh "$LOG_PATH" | grep "ai_client"
else
    echo "⚠️ Nenhum log recente de cliente IA encontrado em $LOG_PATH"
fi

# ----------------------------------------------------------
# 2️⃣ Verificar JSONs gerados
# ----------------------------------------------------------
echo ""
echo "📂 [2/5] Verificando arquivos JSON de insumos..."
INSUMOS_PATH="exports/insumos/json/"
if [ -d "$INSUMOS_PATH" ]; then
    ls -lh "$INSUMOS_PATH"
else
    echo "⚠️ Diretório $INSUMOS_PATH não encontrado — verificar persistência."
fi

# ----------------------------------------------------------
# 3️⃣ Procurar chamada fitz.open() no integration_insumos.py
# ----------------------------------------------------------
echo ""
echo "🔍 [3/5] Verificando se o método fitz.open está implementado..."
if grep -q "fitz.open" utils/integration_insumos.py; then
    echo "✅ Chamada fitz.open() detectada no módulo integration_insumos.py"
else
    echo "❌ Nenhuma chamada fitz.open() detectada — leitura de PDF ainda não corrigida."
fi

# ----------------------------------------------------------
# 4️⃣ Verificar JSON do DFD
# ----------------------------------------------------------
echo ""
echo "📄 [4/5] Verificando estrutura do DFD_ultimo.json..."
DFD_JSON="$INSUMOS_PATH/DFD_ultimo.json"
if [ -f "$DFD_JSON" ]; then
    echo "✅ Arquivo encontrado. Mostrando primeiras linhas:"
    head -n 30 "$DFD_JSON"
else
    echo "⚠️ Nenhum arquivo DFD_ultimo.json encontrado — pipeline interrompido antes da persistência."
fi

# ----------------------------------------------------------
# 5️⃣ Testar permissões de gravação no diretório exports/
# ----------------------------------------------------------
echo ""
echo "🔐 [5/5] Testando permissões de gravação no diretório exports/..."
touch exports/_test_write.txt 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Permissão de gravação confirmada em exports/"
    rm -f exports/_test_write.txt
else
    echo "❌ Falha de permissão — sistema está em modo volátil (/tmp/)"
fi

# ----------------------------------------------------------
# Resumo final
# ----------------------------------------------------------
echo ""
echo "=========================================================="
echo "🧾 Resumo da verificação:"
echo "----------------------------------------------------------"

if grep -q "fitz.open" utils/integration_insumos.py; then
    echo "📘 Leitura PDF: ✅ Implementada"
else
    echo "📘 Leitura PDF: ❌ Ausente — aplicar correção recomendada"
fi

if [ -f "$DFD_JSON" ]; then
    echo "📄 JSON DFD: ✅ Detectado"
else
    echo "📄 JSON DFD: ⚠️ Não encontrado"
fi

if ls "$LOG_PATH" | grep -q "ai_client"; then
    echo "🧠 Logs IA: ✅ Encontrados"
else
    echo "🧠 Logs IA: ⚠️ Ausentes"
fi

echo "=========================================================="
echo "🔍 Fim da verificação – consulte o relatório acima."
echo "Se houver ❌ em Leitura PDF, prossiga com a correção do integration_insumos.py."
echo "=========================================================="
echo ""
