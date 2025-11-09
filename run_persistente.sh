#!/bin/bash
# ==========================================================
# run_persistente.sh – SynapseNext Homologação (TJSP)
# ==========================================================
# Script de inicialização persistente do Streamlit
# Garante execução dentro do workspace real (Codespaces)
# ==========================================================

echo "🚀 Iniciando ambiente SynapseNext (persistente)..."

# Garante que estamos no diretório raiz do projeto
cd /workspaces/synapse-next-homologacao || exit 1
echo "📂 Diretório de execução: $(pwd)"

# Desativa coleta de estatísticas (limpa o log)
export STREAMLIT_BROWSER_GATHERUSAGESTATS=false
export PYTHONUNBUFFERED=1

# Carrega variáveis do .env, se existir
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
  echo "✅ Variáveis de ambiente carregadas do .env"
else
  echo "⚠️  Arquivo .env não encontrado — IA institucional pode não funcionar."
fi

# Garante diretórios necessários
mkdir -p exports/insumos/json exports/logs

# Sobe o Streamlit com o caminho correto do Codespaces
echo "🌐 Subindo Streamlit na porta 8501..."
/home/vscode/.local/bin/streamlit run streamlit_app/Home.py \
  --server.port 8501 \
  --server.enableCORS false \
  --server.enableXsrfProtection false
