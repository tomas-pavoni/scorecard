import matplotlib.pyplot as plt
import pandas as pd


def generate_bubble_chart(data, title="Priorisation des nouveaux business"):
    if data.empty or data.isnull().all().all():
        return None  # Évite les erreurs si les données sont vides

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.colormaps.get_cmap("tab10")

    for i, row in data.iterrows():
        x, y, size, label = row["Moyenne Contribution Stratégique"], row["Moyenne Implémentation"], row[
                                                                                                        "Score moyen Scorecard"] * 100, \
        row["Business"]
        if pd.isna(x) or pd.isna(y) or pd.isna(size):
            continue  # Ignore les valeurs NaN

        ax.scatter(x, y, s=size, color=colors(i), alpha=0.6, edgecolors='k')
        ax.annotate(label, (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    # Fixer les limites des axes X et Y
    ax.set_xlim(0, 3)  # Axe X (Contribution stratégique)
    ax.set_ylim(0, 3)  # Axe Y (Facilité d'implémentation)

    ax.set_xlabel("Contribution stratégique (vision)")
    ax.set_ylabel("Facilité d'implémentation (réalisation)")
    ax.set_title(title, fontsize=14, fontweight='bold')

    plt.grid(True, linestyle="--", alpha=0.6)
    return fig
