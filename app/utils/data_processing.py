# 📌 data_processing.py – Fonctions de traitement des données
import pandas as pd
import numpy as np


def prepare_data_for_chart(user, session_data, business_list, mapping_strategiques, mapping_implementation):
    all_data = []
    if user == "Tomas":
        aggregated_data = {}
        user_count = 0

        for usr, usr_data in session_data['data_store'].items():
            if usr != "Tomas":
                user_count += 1
                for business in business_list:
                    if business in usr_data:
                        data = usr_data[business]

                        mean_strategic = np.mean([mapping_strategiques.get(val, 0) for val in data.values() if val in mapping_strategiques])
                        mean_implementation = np.mean([mapping_implementation[key].get(val, 0) for key, val in data.items() if key in mapping_implementation and val in mapping_implementation[key]])
                        mean_score = session_data['scorecard_data'].get(usr, {}).get(business, pd.DataFrame()).get("Score", pd.Series(dtype=float)).mean()


                        if business not in aggregated_data:
                            aggregated_data[business] = {"Moyenne Contribution Stratégique": mean_strategic, "Moyenne Implémentation": mean_implementation, "Score moyen Scorecard": mean_score}
                        else:
                            aggregated_data[business]["Moyenne Contribution Stratégique"] += mean_strategic
                            aggregated_data[business]["Moyenne Implémentation"] += mean_implementation
                            aggregated_data[business]["Score moyen Scorecard"] += mean_score

        if user_count > 0:
            for business in aggregated_data:
                aggregated_data[business] = {key: val / user_count for key, val in aggregated_data[business].items()}

        all_data = [{"Business": business, **values} for business, values in aggregated_data.items()]
    else:
        for business in business_list:
            if business in session_data['data_store'].get(user, {}):
                data = session_data['data_store'][user][business]
                mean_strategic = np.mean([mapping_strategiques.get(val, 0) for val in data.values() if val in mapping_strategiques])
                mean_implementation = np.mean([mapping_implementation[key].get(val, 0) for key, val in data.items() if key in mapping_implementation and val in mapping_implementation[key]])
                mean_score = session_data['scorecard_data'].get(user, {}).get(business, pd.DataFrame()).get("Score", pd.Series()).mean()
                all_data.append({"Business": business, "Moyenne Contribution Stratégique": mean_strategic, "Moyenne Implémentation": mean_implementation, "Score moyen Scorecard": mean_score})

    return pd.DataFrame(all_data)


def calculate_average_scorecard(results_dict):
    """Calcule la moyenne des scorecards des utilisateurs (exclut Tomas)."""
    scorecard_moyenne = None
    utilisateurs_remplis = 0

    for user, user_data in results_dict.items():
        if user != "Tomas":
            for business, data in user_data.items():
                if not data.empty:
                    if scorecard_moyenne is None:
                        scorecard_moyenne = data.copy()
                    else:
                        scorecard_moyenne["Score"] += data["Score"]
                    utilisateurs_remplis += 1

    if scorecard_moyenne is not None and utilisateurs_remplis > 0:
        scorecard_moyenne["Score"] /= utilisateurs_remplis
        scorecard_moyenne["Score"] = scorecard_moyenne["Score"].round(2)
        return scorecard_moyenne
    return None
