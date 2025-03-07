# 📌 charts.py – Gestion des graphiques avec Matplotlib
import pandas as pd
import matplotlib.pyplot as plt

def generate_bubble_chart(data, title="Priorisation des nouveaux business"):
    """Génère un graphique en bulles basé sur les données."""
    if data.empty or data.isnull().all().all():
        return None  # Évite les erreurs si les données sont vides

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.get_cmap("tab10", len(data))

    for i, row in data.iterrows():
        x, y, size, label = row["Moyenne Contribution Stratégique"], row["Moyenne Implémentation"], row["Score moyen Scorecard"] * 100, row["Business"]
        if pd.isna(x) or pd.isna(y) or pd.isna(size):
            continue  # Ignore les valeurs NaN
        ax.scatter(x, y, s=size, color=colors(i), alpha=0.6, edgecolors='k')
        ax.annotate(label, (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    ax.set_xlabel("Contribution stratégique (vision)")
    ax.set_ylabel("Facilité d'implémentation (réalisation)")
    ax.set_title(title, fontsize=14, fontweight='bold')
    plt.grid(True, linestyle="--", alpha=0.6)
    return fig
