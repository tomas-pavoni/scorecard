import pandas as pd
from utils.data_processing import prepare_data_for_chart

def test_prepare_data_for_chart():
    session_data = {
        'data_store': {
            'Alexandre': {'Calculateur réno': {'Expertise': 'Moyenne', 'Projet pilote': 'En cours'}},
            'Aline': {'Calculateur réno': {'Expertise': 'Faible', 'Projet pilote': 'À définir'}}
        },
        'scorecard_data': {
            'Alexandre': {'Calculateur réno': pd.DataFrame({'Score': [7, 8, 9]})},
            'Aline': {'Calculateur réno': pd.DataFrame({'Score': [5, 6]})}
        }
    }
    business_list = ["Calculateur réno"]
    mapping_strategiques = {"Faible": 1, "Moyenne": 2, "Élevée": 3}
    mapping_implementation = {"Projet pilote": {"À définir": 1, "En cours": 2}}

    df_results = prepare_data_for_chart("Tomas", session_data, business_list, mapping_strategiques, mapping_implementation)

    assert not df_results.empty
    assert df_results["Moyenne Contribution Stratégique"].iloc[0] == 1.5  # (1 + 2) / 2
    assert df_results["Moyenne Implémentation"].iloc[0] == 1.5  # (2 + 1) / 2
    assert round(df_results["Score moyen Scorecard"].iloc[0], 2) == 6.75  # Arrondi au centième
