# utils.py
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime


description = """
    ### Bienvenue sur la plateforme
    Veuillez entrer vos identifiants pour accéder aux fonctionnalités.  
    Si vous avez des problèmes de connexion, contactez l'administrateur.
    """


def create_pdf(data, filename, user_name, business_name):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Headers
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 40, f"Scorecard for {business_name}")
    c.drawString(100, height - 60, f"Prepared by: {user_name}")
    c.drawString(100, height - 80, f"Date: {datetime.now().strftime('%Y-%m-%d')}")

    # Adding column headers before data entries
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 120, "Category")
    c.drawString(300, height - 120, "Score")
    y_position = height - 140

    # Data Iteration and Display
    c.setFont("Helvetica", 12)
    for index, row in data.iterrows():
        text_category = f"{row['Category']}"
        text_score = f"{row['Score']}"
        c.drawString(100, y_position, text_category)
        c.drawString(300, y_position, str(text_score))
        y_position -= 20

        # Page control
        if y_position < 100:
            c.showPage()
            c.setFont("Helvetica-Bold", 14)
            c.drawString(100, height - 40, f"Continued: Scorecard for {business_name}")
            y_position = height - 60

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