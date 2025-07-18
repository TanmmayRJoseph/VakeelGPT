from fpdf import FPDF
import os

def generate_summary_pdf(qa_history: list, output_path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.multi_cell(0, 10, "Legal Clause Q&A Summary\n\n")

    for idx, qa in enumerate(qa_history, 1):
        q = f"\nQ{idx}: {qa['question']}"
        clause = f"Matched Clause:\n{qa['clause']}"
        ans = f"Explanation:\n{qa['answer']}\n" + "-" * 80

        for content in [q, clause, ans]:
            pdf.multi_cell(0, 10, content.encode('latin-1', 'replace').decode('latin-1'))

    pdf.output(output_path)
    return output_path
