import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from typing import List, Dict, Any
from app.logic.models import Transaction

def export_to_csv(filepath: str, transactions: List[Transaction]):
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Tipo", "Título", "Descripción", "Monto", "Categoría", "Fecha", "Método de Pago"])
        for t in transactions:
            writer.writerow([t.id, t.type, t.title, t.description, t.amount, t.category, t.date, t.payment_method])

def export_to_pdf(filepath: str, transactions: List[Transaction], summary: Dict[str, Any]):
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Reporte Financiero")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Total Ingresos: ${summary.get('total_income', 0):.2f}")
    c.drawString(50, height - 100, f"Total Gastos: ${summary.get('total_expense', 0):.2f}")
    c.drawString(50, height - 120, f"Balance Total: ${summary.get('balance', 0):.2f}")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 150, "Transacciones")
    
    c.setFont("Helvetica", 10)
    y = height - 170
    for t in transactions:
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 50
        text = f"{t.date} | {t.type.upper()} | {t.title} | {t.category} | ${t.amount:.2f}"
        c.drawString(50, y, text)
        y -= 20
        
    c.save()
