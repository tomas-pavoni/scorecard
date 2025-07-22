import matplotlib.pyplot as plt
import datetime
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from utils.data_processing import calculate_average_scorecard


def create_combined_pdf(results_dict, filename):
    """Crée un PDF contenant tous les résultats des utilisateurs, y compris la moyenne."""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y_position = height - 40

    # 🟢 **Utilisation de la fonction calculate_average_scorecard()**
    df_moyenne = calculate_average_scorecard(results_dict)

    # 📌 **Ajout de la Scorecard Moyenne au PDF**
    if df_moyenne is not None and not df_moyenne.empty:
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, y_position, "📊 Scorecard Moyenne des Utilisateurs")
        y_position -= 30

        # 📅 Ajout de la date sous le titre
        c.setFont("Helvetica", 12)
        c.drawString(100, y_position, f"Date : {datetime.datetime.now().strftime('%Y-%m-%d')}")
        y_position -= 30

        # Affichage des scores moyens
        for _, row in df_moyenne.iterrows():
            c.drawString(100, y_position, f"{row['Section']} - {row['Category']} : {row['Score']}")
            y_position -= 20
            if y_position < 100:
                c.showPage()
                y_position = height - 40

        c.showPage()  # Nouvelle page pour la suite des résultats

    # 📌 **Ajout des Scorecards Individuelles**
    for user, user_data in results_dict.items():
        if user != "Tomas":
            for business, data in user_data.items():
                if not data.empty:
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(100, height - 40, f"📄 Scorecard pour {business} ({user})")
                    c.drawString(100, height - 60, f"Date : {datetime.datetime.now().strftime('%Y-%m-%d')}")
                    y_position = height - 100

                    c.setFont("Helvetica", 12)
                    for _, row in data.iterrows():
                        c.drawString(100, y_position, f"{row['Section']} - {row['Category']} : {row['Score']}")
                        y_position -= 20
                        if y_position < 100:
                            c.showPage()
                            y_position = height - 40

                    c.showPage()

    c.save()


def save_bubble_chart_to_pdf(fig, filename):
    """Enregistre un graphique en bulles dans un PDF."""
    with PdfPages(filename) as pdf:
        pdf.savefig(fig)
        plt.close(fig)
