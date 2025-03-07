# utils.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime


description = """
### 🚀 Bienvenue sur la plateforme de priorisation des initiatives stratégiques 📊

Cette application vous permet **d’évaluer et comparer différents projets** en fonction de leur **pertinence stratégique**, de leur **faisabilité** et de leur **impact potentiel**.  

Grâce aux **scorecards et aux graphiques interactifs**, vous pouvez analyser les résultats et **faciliter la prise de décision**. 📈  

---

## 🎯 Objectif de l’application  
Cette plateforme vous aide à :  
✔ **Évaluer** la pertinence et la faisabilité des projets.  
✔ **Prioriser** les initiatives selon des critères stratégiques.  
✔ **Visualiser** les résultats sous forme de graphes interactifs.  
✔ **Faciliter** le suivi des projets à fort impact.  

---

## 📝 Fonctionnement des Scorecards  
Chaque projet est évalué selon plusieurs dimensions :  

### **1️⃣ Contribution Stratégique (Vision) 🌍**  
➡️ Évalue **l’alignement du projet avec les objectifs stratégiques**.  
➡️ Notation basée sur **son impact sur la digitalisation, la décarbonation, la croissance, etc.**  

### **2️⃣ Faisabilité & Implémentation 🛠**  
➡️ Analyse de la **facilité de mise en œuvre** du projet.  
➡️ Critères : **expertise requise, état du projet pilote, compétences internes disponibles**.  

### **3️⃣ Scorecard détaillée 🎯**  
➡️ Notation de **0 à 10** sur : potentiel financier, valeur client, faisabilité technique, viabilité économique, etc.  

---

## 📊 Visualisation et Priorisation des Business  
Les résultats sont représentés sous forme de **graphique en bulles** :  

🔵 **Chaque bulle représente un projet**.  
🔵 **La taille** de la bulle correspond au **score moyen** du projet.  
🔵 **L’axe X** = **Alignement stratégique (vision)**.  
🔵 **L’axe Y** = **Facilité d’implémentation (réalisation)**.  

### **📌 Interprétation des résultats :**  
✅ **En haut à droite (💎 Prioritaires)** : Projets à fort impact stratégique et faciles à implémenter.  
🔄 **Au centre (⚖ Zone d’arbitrage)** : Projets nécessitant une discussion approfondie.  
❌ **En bas à gauche (📉 Risqués)** : Projets difficiles à mettre en œuvre avec un faible impact stratégique.  

---

## 📄 Exportation et Partage des Résultats  
Les résultats peuvent être **générés en PDF** pour partage et analyse ultérieure.  

📥 **Options disponibles** :  
- Télécharger **les résultats des scorecards** pour chaque projet.  
- Exporter **le graphe global des projets**.  
- Générer **un PDF unique contenant toutes les analyses**.  

---

## 🚀 Conclusion  
Cette plateforme vous aide à **structurer, analyser et prioriser vos projets d’innovation** pour maximiser leur succès.  

🔍 **À vous de jouer !** 💡  

---

💬 **En cas de question, contactez Tomas Pavoni ou Philippe Chollet.**
"""


# 📌 Calcul de la moyenne des colonnes sélectionnées
def calculate_means(data, column_list):
    if isinstance(data, dict):
        df = pd.DataFrame([data])  # Convertir en DataFrame si c'est un dictionnaire
    else:
        df = data

    valid_columns = [col for col in column_list if col in df.columns]
    return df[valid_columns].mean().mean() if valid_columns else 0


# 📌 Création d'un PDF avec les résultats des utilisateurs
def create_combined_pdf(results_dict, filename):
    """Crée un PDF contenant tous les résultats des utilisateurs."""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    for user, user_data in results_dict.items():
        for business, data in user_data.items():
            if not data.empty:
                c.setFont("Helvetica-Bold", 14)
                c.drawString(100, height - 40, f"Scorecard pour {business}")
                c.drawString(100, height - 60, f"Utilisateur : {user}")
                c.drawString(100, height - 80, f"Date : {datetime.now().strftime('%Y-%m-%d')}")

                c.setFont("Helvetica-Bold", 12)
                c.drawString(100, height - 120, "Catégorie")
                c.drawString(300, height - 120, "Score")
                y_position = height - 140

                c.setFont("Helvetica", 12)
                for _, row in data.iterrows():
                    c.drawString(100, y_position, row['Category'])
                    c.drawString(300, y_position, str(row['Score']))
                    y_position -= 20
                    if y_position < 100:
                        c.showPage()
                        y_position = height - 60
                c.showPage()

    c.save()


# 📌 Génération d'un graphique en bulles
def generate_bubble_chart(data, title="Priorisation des nouveaux business"):
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


# 📌 Sauvegarde d'un graphique en PDF
def save_bubble_chart_to_pdf(fig, filename):
    """Enregistre un graphique matplotlib dans un fichier PDF."""
    with PdfPages(filename) as pdf:
        pdf.savefig(fig)
        plt.close(fig)


# 📌 Préparation des données pour le graphique
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
                        mean_score = session_data['scorecard_data'].get(usr, {}).get(business, pd.DataFrame()).get("Score", pd.Series()).mean()

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