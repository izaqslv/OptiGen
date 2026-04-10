# ============================================================
#  MODEL CONFIG — OPTIGEN
# ============================================================
# Autor: NewGen / OptiGen
# Descrição:
# Este módulo centraliza TODAS as configurações estruturais
# relacionadas aos modelos de Machine Learning utilizados
# no OptiGen.
#
# Ele garante:
# - Consistência entre treino e predição
# - Desacoplamento de caminhos e features
# - Facilidade de manutenção e versionamento
#
#  REGRA CRÍTICA:
# Nenhum outro arquivo do sistema deve definir manualmente:
# - lista de features
# - nome do target
# - caminhos de modelos
#
# Tudo deve ser importado daqui.
# ============================================================


# ============================================================
#  FEATURES DO MODELO
# ============================================================
# Lista oficial de variáveis de entrada utilizadas pelo modelo.
#
#  IMPORTANTE:
# - A ordem deve ser mantida (impacta diretamente o modelo)
# - Deve ser IDENTICA entre treino e inferência
# - Alterações exigem re-treinamento do modelo
#
# Origem:
# Geradas após pipeline de feature engineering
# ============================================================

FEATURE_COLUMNS = [
    "tempo",
    "altura",
    "concentracao",
    "c_lag1",
    "c_lag2",
    "roa",
    "dens_susp",
    "dens_solids",
    "teor_solids",
    "dp_medio",
    "m",
    "n",
    "dc_dt",
    "regime"
]


# ============================================================
#  TARGET DO MODELO
# ============================================================
# Variável alvo que o modelo aprende a prever
#
# Neste caso:
# target = concentração futura (t+1)
# ============================================================

TARGET_COLUMN = "target"


# ============================================================
#  PATHS DOS MODELOS
# ============================================================
# Estrutura padronizada de armazenamento dos modelos treinados.
#
# Organização:
# - Modelo global → fallback / baseline
# - Modelos por regime → especializados
#
# Isso permite:
# - Maior precisão por regime
# - Robustez com fallback global
# - Escalabilidade futura (novos regimes)
#
#  IMPORTANTE:
# - Caminhos devem existir no ambiente de execução
# - Devem ser consistentes com o treinamento
# ============================================================

MODEL_PATHS = {

    #  Modelo global (usado como fallback)
    "global": "model_layer/artifacts/models/model_v1.pkl",

    #  Modelos especializados por regime
    "regime": {
        0: "model_layer/models/specialized/model_regime_0.pkl",
        1: "model_layer/models/specialized/model_regime_1.pkl",
        2: "model_layer/models/specialized/model_regime_2.pkl",
    }
}


# ============================================================
#  OBSERVAÇÕES DE ARQUITETURA
# ============================================================
#  Este arquivo é o "single source of truth" dos modelos
#
#  Qualquer alteração aqui impacta:
#   - train_model_core.py
#   - predictor_core.py
#   - simulator_core.py (futuro)
#
#  Boas práticas:
#   - Versionar modelos (model_v1, model_v2, ...)
#   - Nunca sobrescrever modelos antigos
#   - Manter rastreabilidade (experimentos)
#
#  Futuras expansões:
#   - inclusão de hiperparâmetros
#   - configuração de thresholds por regime
#   - metadata do modelo (data, dataset, etc.)
# ============================================================
