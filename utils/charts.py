import matplotlib.pyplot as plt
import os

CHART_DIR = "charts"
os.makedirs(CHART_DIR, exist_ok=True)

def generate_chart(score, matched, missing, file_id):

    labels = [
        "Matched Skills",
        "Missing Skills"
    ]

    values = [matched, missing]

    plt.figure(figsize=(5, 5))
    plt.pie(
        values,
        labels=labels,
        autopct='%1.1f%%'
    )

    chart_path = f"{CHART_DIR}/{file_id}.png"

    plt.savefig(chart_path)
    plt.close()

    return chart_path