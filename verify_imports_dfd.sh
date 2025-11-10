#!/bin/bash
# ==========================================================
# verify_imports_dfd.sh
# SynapseNext – Auditoria de Importações DFD
# ==========================================================
# Este script verifica se há importações do módulo integration_dfd
# fora do caminho oficial (utils.integration_dfd).
# Gera relatório detalhado em exports/logs/verify_imports_dfd.txt
# ==========================================================

echo "🧠 Verificando importações de integration_dfd em todo o repositório..."
echo "==========================================================" 

# Cria diretório de logs, se não existir
mkdir -p exports/logs

LOGFILE="exports/logs/verify_imports_dfd.txt"
> "$LOGFILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Início da auditoria de importações DFD" >> "$LOGFILE"
echo "----------------------------------------------------------" >> "$LOGFILE"

# 1️⃣ Busca todas as importações do módulo integration_dfd
grep -RIn "integration_dfd" --exclude-dir={.git,__pycache__,exports} . >> "$LOGFILE"

# 2️⃣ Destaca importações incorretas (fora de utils/)
INCORRETAS=$(grep -RIn "streamlit_app.utils.integration_dfd" --exclude-dir={.git,__pycache__,exports} .)

# 3️⃣ Resumo visual no terminal
if [ -z "$INCORRETAS" ]; then
  echo "✅ Todas as importações do módulo DFD apontam corretamente para utils.integration_dfd"
  echo "✅ Nenhuma referência incorreta encontrada" >> "$LOGFILE"
else
  echo "⚠️ Importações incorretas detectadas:"
  echo "$INCORRETAS"
  echo "----------------------------------------------------------" >> "$LOGFILE"
  echo "⚠️ Importações incorretas detectadas:" >> "$LOGFILE"
  echo "$INCORRETAS" >> "$LOGFILE"
  echo "----------------------------------------------------------" >> "$LOGFILE"
  echo "🧩 Aponte todas as importações para: from utils.integration_dfd import ..." >> "$LOGFILE"
fi

echo "==========================================================" 
echo "📄 Relatório completo salvo em: $LOGFILE"
echo "=========================================================="
