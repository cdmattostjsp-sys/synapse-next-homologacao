#!/bin/bash

# ============================================================================
# FULL FLOW TEST — DFD → ETP → TR
# Homologação integrada do SynapseNext vNext (TJSP)
# ============================================================================

WORKSPACE="/workspaces/synapse-next-homologacao"
REPORT_FILE="/tmp/relatorio_full_flow_homologacao.txt"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  FULL FLOW HOMOLOGATION TEST — SynapseNext vNext (TJSP)     ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"

# Inicia relatório
echo "=========================================================" > "$REPORT_FILE"
echo "RELATÓRIO DE HOMOLOGAÇÃO INTEGRADA - SYNAPSE NEXT vNext" >> "$REPORT_FILE"
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')" >> "$REPORT_FILE"
echo "Workspace: $WORKSPACE" >> "$REPORT_FILE"
echo "=========================================================" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# -------------------------------------------------------------------
# Função genérica de teste com timeout e leitura NÃO bloqueante
# -------------------------------------------------------------------
test_page() {
    local PAGE_NAME="$1"
    local PAGE_FILE="$2"
    local PORT="$3"
    local DURATION="$4"

    echo -e "\n${YELLOW}[$(date '+%H:%M:%S')]${NC} Testando: $PAGE_NAME"
    echo "" >> "$REPORT_FILE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE"
    echo "TESTE: $PAGE_NAME" >> "$REPORT_FILE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$REPORT_FILE"
    echo "Arquivo: $PAGE_FILE" >> "$REPORT_FILE"
    echo "Porta: $PORT" >> "$REPORT_FILE"
    echo "Janela de observação: ${DURATION}s" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"

    local LOG_FILE="/tmp/streamlit_${PORT}.log"

    python3 - << EOF_PY
import subprocess, time, sys, select

cmd = [
    "streamlit", "run",
    "$PAGE_FILE",
    "--server.headless", "true",
    "--server.port", "$PORT",
    "--server.enableCORS", "false",
    "--server.enableXsrfProtection", "false",
]

print("Processo iniciado. Observando por ${DURATION}s...")

logs = []
warnings = []
errors = []
endpoints = []
initialized = False
init_time = None

start = time.time()

proc = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
)

# Loop com timeout + leitura não bloqueante
while True:
    now = time.time()
    if now - start > $DURATION:
        print("⏱ Timeout atingido (${DURATION}s). Encerrando observação.")
        break

    rlist, _, _ = select.select([proc.stdout], [], [], 0.5)
    if not rlist:
        # Nada novo para ler, volta para checar timeout
        continue

    line = proc.stdout.readline()
    if not line:
        if proc.poll() is not None:
            # Processo terminou
            break
        continue

    line = line.rstrip("\n")
    logs.append(line)
    low = line.lower()

    if "you can now view your streamlit app" in low:
        if not initialized:
            initialized = True
            init_time = now - start
            print(f"✅ Aplicação iniciada em {init_time:.2f}s")

    if "warning" in low and "usage statistics" not in low:
        warnings.append(line)

    if any(k in low for k in ["error", "exception", "traceback", "failed", "could not"]):
        errors.append(line)

    if "local url:" in low or "network url:" in low or "external url:" in low:
        endpoints.append(line)

# Finaliza processo
try:
    proc.terminate()
    proc.wait(timeout=5)
except Exception:
    try:
        proc.kill()
        proc.wait(timeout=5)
    except Exception:
        pass

# Salvar logs em arquivo dedicado
with open("$LOG_FILE", "w", encoding="utf-8") as f:
    f.write("\n".join(logs))

print("LOGS_COUNT=", len(logs))
print("WARNINGS_COUNT=", len(warnings))
print("ERRORS_COUNT=", len(errors))
print("ENDPOINTS_COUNT=", len(endpoints))
print("INITIALIZED=", initialized)
print("INIT_TIME=", init_time)

if errors:
    print("CRITICAL_ERRORS_FOUND=YES")
else:
    print("CRITICAL_ERRORS_FOUND=NO")

if endpoints:
    for ep in endpoints:
        print("ENDPOINT: " + ep)

# Critério de sucesso: iniciou + sem erros críticos
ok = bool(initialized) and not errors
sys.exit(0 if ok else 1)
EOF_PY

    EXIT_CODE=${PIPESTATUS[0]}

    echo "" >> "$REPORT_FILE"
    echo "Código de Saída: $EXIT_CODE" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"

    # Anexa primeiros 60 logs para auditoria
    if [ -f "$LOG_FILE" ]; then
        echo "--- LOGS (trecho inicial) ---" >> "$REPORT_FILE"
        head -n 60 "$LOG_FILE" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
    fi

    if [ $EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✅ $PAGE_NAME: HOMOLOGADO${NC}"
        echo "STATUS: ✅ HOMOLOGADO" >> "$REPORT_FILE"
    else
        echo -e "${RED}❌ $PAGE_NAME: NÃO HOMOLOGADO${NC}"
        echo "STATUS: ❌ NÃO HOMOLOGADO" >> "$REPORT_FILE"
    fi

    return $EXIT_CODE
}

cd "$WORKSPACE" || exit 1

STATUS_DFD=0
STATUS_ETP=0
STATUS_TR=0

# DFD
test_page "DFD - Formalização da Demanda" \
          "streamlit_app/pages/02_📄 DFD - Formalização da Demanda.py" \
          8503 \
          20
STATUS_DFD=$?

# ETP
test_page "ETP – Estudo Técnico Preliminar" \
          "streamlit_app/pages/03_📘 ETP – Estudo Técnico Preliminar.py" \
          8504 \
          20
STATUS_ETP=$?

# TR
test_page "TR – Termo de Referência" \
          "streamlit_app/pages/05_📑 TR – Termo de Referência.py" \
          8505 \
          20
STATUS_TR=$?

echo "" >> "$REPORT_FILE"
echo "=========================================================" >> "$REPORT_FILE"
echo "SUMÁRIO EXECUTIVO" >> "$REPORT_FILE"
echo "=========================================================" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

TOTAL_PASSED=0
[ $STATUS_DFD -eq 0 ] && ((TOTAL_PASSED++))
[ $STATUS_ETP -eq 0 ] && ((TOTAL_PASSED++))
[ $STATUS_TR -eq 0 ] && ((TOTAL_PASSED++))

echo "DFD: $([ $STATUS_DFD -eq 0 ] && echo 'HOMOLOGADO' || echo 'NÃO HOMOLOGADO')" >> "$REPORT_FILE"
echo "ETP: $([ $STATUS_ETP -eq 0 ] && echo 'HOMOLOGADO' || echo 'NÃO HOMOLOGADO')" >> "$REPORT_FILE"
echo "TR:  $([ $STATUS_TR -eq 0 ] && echo 'HOMOLOGADO' || echo 'NÃO HOMOLOGADO')" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "Total aprovado: $TOTAL_PASSED/3" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

if [ $TOTAL_PASSED -eq 3 ]; then
    echo "RESULTADO FINAL: ✅ FLUXO COMPLETO HOMOLOGADO" >> "$REPORT_FILE"
else
    echo "RESULTADO FINAL: ⚠️ FLUXO REQUER AJUSTES" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"
echo "Relatório gerado em: $(date '+%Y-%m-%d %H:%M:%S')" >> "$REPORT_FILE"
echo "=========================================================" >> "$REPORT_FILE"

echo ""
echo -e "${GREEN}Relatório completo em: $REPORT_FILE${NC}"
echo ""
cat "$REPORT_FILE"

exit $([ $TOTAL_PASSED -eq 3 ] && echo 0 || echo 1)
