import pandas as pd
from utils.charts import generate_bubble_chart

def test_generate_bubble_chart():
    # Données valides
    df = pd.DataFrame({
        "Business": ["Projet 1", "Projet 2"],
        "Moyenne Contribution Stratégique": [2, 3],
        "Moyenne Implémentation": [3, 1],
        "Score moyen Scorecard": [7, 9]
    })
    fig = generate_bubble_chart(df)
    assert fig is not None  # Vérifie que le graphique est bien généré

    # Données vides
    df_empty = pd.DataFrame()
    fig_empty = generate_bubble_chart(df_empty)
    assert fig_empty is None  # Vérifie qu'on ne plante pas

    # Données NaN : on vérifie si un graphique est généré sans erreur
    df_nan = pd.DataFrame({
        "Business": ["Projet 1"],
        "Moyenne Contribution Stratégique": [None],
        "Moyenne Implémentation": [3],
        "Score moyen Scorecard": [7]
    })
    fig_nan = generate_bubble_chart(df_nan)
    assert fig_nan is not None  # Vérifie que le graphe est généré même avec NaN
