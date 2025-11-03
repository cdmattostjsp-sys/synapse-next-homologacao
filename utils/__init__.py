# -*- coding: utf-8 -*-
"""
Compatibilidade retroativa – SynapseNext v3
Permite que imports do tipo `from utils.*` continuem funcionando
mesmo quando os módulos estão dentro de `streamlit_app/utils/`.
"""

import sys
from pathlib import Path

# Caminho absoluto para o diretório streamlit_app/utils
base_path = Path(__file__).resolve().parent
internal_utils = base_path / "streamlit_app" / "utils"

# Se existir, adiciona ao sys.path (prioridade alta)
if internal_utils.exists() and str(internal_utils) not in sys.path:
    sys.path.insert(0, str(internal_utils))
# torna /utils um pacote Python
