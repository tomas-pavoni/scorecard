# 📌 pdf_generator.py – Gestion des exports PDF
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from matplotlib.backends.backend_pdf import PdfPages

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

                c.setFont("Helvetica", 12)
                y_position = height - 100

                for _, row in data.iterrows():
                    c.drawString(100, y_position, row['Category'])
                    c.drawString(300, y_position, str(row['Score']))
                    y_position -= 20
                    if y_position < 100:
                        c.showPage()
                        y_position = height - 60
                c.showPage()

    c.save()

def save_bubble_chart_to_pdf(fig, filename):
    """Enregistre un graphique en bulles dans un PDF."""
    with PdfPages(filename) as pdf:
        pdf.savefig(fig)
        plt.close(fig)
