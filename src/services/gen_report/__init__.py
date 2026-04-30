import io
from src.database import db
from .fetch_data import fetch_report_data
from .normalize_data import process_rows_into_questions
from .gen_excel import create_excel_structure, write_questions_to_excel, write_summary_section
from openpyxl import Workbook

async def generate_test_report(attempt_id: int) -> io.BytesIO:
    """
    Generates a detailed Excel report for a specific test attempt.
    """
    
    async with db.pool.acquire() as conn:
        metadata, rows = await fetch_report_data(conn, attempt_id)
    
    if not metadata or not rows:
        return None

    questions = process_rows_into_questions(rows)

    wb = Workbook()
    ws = wb.active
    ws.title = "Test Result"

    create_excel_structure(ws)
    last_row, correct_count = write_questions_to_excel(ws, questions)
    write_summary_section(ws, last_row, metadata, len(questions), correct_count)

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    return output