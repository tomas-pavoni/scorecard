import os
from utils.PDF_generator import create_combined_pdf
import pandas as pd

def test_create_combined_pdf():
    data = {
        "Alexandre": {"Calculateur réno": pd.DataFrame({"Category": ["A", "B"], "Score": [3, 5]})}
    }
    filename = "test_results.pdf"
    create_combined_pdf(data, filename)

    assert os.path.exists(filename)
    os.remove(filename)  # Nettoyer après test
