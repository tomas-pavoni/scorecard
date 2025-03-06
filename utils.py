# utils.py
import pandas as pd
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



def create_combined_pdf(results_dict, filename):
    """Crée un PDF unique contenant tous les résultats des utilisateurs."""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    for user, user_data in results_dict.items():
        for business, data in user_data.items():
            if not data.empty:
                # Ajout d'un en-tête
                c.setFont("Helvetica-Bold", 14)
                c.drawString(100, height - 40, f"Scorecard pour {business}")
                c.drawString(100, height - 60, f"Utilisateur : {user}")
                c.drawString(100, height - 80, f"Date : {datetime.now().strftime('%Y-%m-%d')}")

                # Ajout des scores
                c.setFont("Helvetica-Bold", 12)
                c.drawString(100, height - 120, "Catégorie")
                c.drawString(300, height - 120, "Score")
                y_position = height - 140

                c.setFont("Helvetica", 12)
                for index, row in data.iterrows():
                    text_category = f"{row['Category']}"
                    text_score = f"{row['Score']}"
                    c.drawString(100, y_position, text_category)
                    c.drawString(300, y_position, str(text_score))
                    y_position -= 20

                    # Vérification pour ajouter une nouvelle page si nécessaire
                    if y_position < 100:
                        c.showPage()
                        y_position = height - 60

                c.showPage()  # Nouvelle page pour le prochain utilisateur

    c.save()


def calculate_means(data, column_list):
    if isinstance(data, dict):
        # Convertir le dictionnaire en DataFrame si nécessaire
        df = pd.DataFrame([data])
    else:
        df = data

    valid_columns = [col for col in column_list if col in df.columns]
    if valid_columns:
        return df[valid_columns].mean().mean()
    else:
        return 0  # Retourne 0 si aucune des colonnes n'est valide

def generate_bubble_chart(df, user_name):
    fig, ax = plt.subplots()
    colors = plt.cm.get_cmap('tab10', len(df))

    for i, row in df.iterrows():
        x = row['Mean Strategic']
        y = row['Mean Implementation']
        size = row['Mean Score'] * 100  # Adjust bubble size
        label = row['Business']

        bubble = ax.scatter(x, y, s=size, color=colors(i), alpha=0.6, edgecolors='w')
        ax.annotate(label, (x, y), textcoords="offset points", xytext=(0,10), ha='center')

    ax.set_xlabel('Contribution aux objectifs de RES24')
    ax.set_ylabel('Facilité d\'implémentation')
    ax.set_title(f'Priorisation des business pour {user_name}')
    return fig

def save_bubble_chart_to_pdf(fig, filename):
    """Enregistre un graphique matplotlib dans un fichier PDF."""
    with PdfPages(filename) as pdf:
        pdf.savefig(fig)
        plt.close(fig)
