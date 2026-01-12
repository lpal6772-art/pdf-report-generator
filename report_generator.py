"""
===========================================================
Employee Performance Analysis Report Generator
-----------------------------------------------------------
Reads employee data from CSV file,
performs analysis, and generates a PDF report.
===========================================================
"""

# ---------------------- IMPORTS ---------------------------
from fpdf import FPDF
import csv
from datetime import datetime
import statistics
import os

# ------------------- CONSTANTS ----------------------------
DATA_FILE = "data.csv"
OUTPUT_FILE = "employee_performance_report.pdf"
PAGE_MARGIN = 15

# ------------------- UTILITY FUNCTIONS --------------------


def check_file_exists(filename):
    """Check if required file exists"""
    if not os.path.exists(filename):
        print(f"ERROR: {filename} not found!")
        exit()
    else:
        print(f"{filename} found successfully.")


def read_csv_data(filename):
    """Read employee data from CSV file"""
    employees = []

    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            employees.append({
                "name": row["Name"],
                "department": row["Department"],
                "score": int(row["Score"])
            })

    print("CSV data read successfully.")
    return employees


# ------------------- DATA ANALYSIS ------------------------


def calculate_statistics(employees):
    """Calculate performance statistics"""
    scores = [emp["score"] for emp in employees]

    stats = {
        "total_employees": len(employees),
        "average_score": round(statistics.mean(scores), 2),
        "highest_score": max(scores),
        "lowest_score": min(scores)
    }

    print("Statistics calculated successfully.")
    return stats


def department_wise_average(employees):
    """Calculate department-wise average scores"""
    dept_data = {}

    for emp in employees:
        dept = emp["department"]
        score = emp["score"]

        if dept not in dept_data:
            dept_data[dept] = []
        dept_data[dept].append(score)

    dept_avg = {}
    for dept, scores in dept_data.items():
        dept_avg[dept] = round(statistics.mean(scores), 2)

    print("Department-wise averages calculated.")
    return dept_avg


# ------------------- PDF CLASS ----------------------------


class ReportPDF(FPDF):
    """Custom PDF class"""

    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Employee Performance Analysis Report", align="C")
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", size=9)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


# ------------------- PDF CONTENT FUNCTIONS ----------------


def add_report_metadata(pdf):
    """Add report generation date"""
    pdf.set_font("Arial", size=11)
    date_str = datetime.now().strftime("%B %d, %Y")
    pdf.cell(0, 8, f"Report Generated On: {date_str}", ln=True)
    pdf.ln(5)


def add_summary_section(pdf, stats):
    """Add summary statistics section"""
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. Summary Statistics", ln=True)

    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"Total Employees: {stats['total_employees']}", ln=True)
    pdf.cell(0, 8, f"Average Score: {stats['average_score']}", ln=True)
    pdf.cell(0, 8, f"Highest Score: {stats['highest_score']}", ln=True)
    pdf.cell(0, 8, f"Lowest Score: {stats['lowest_score']}", ln=True)
    pdf.ln(5)


def add_department_analysis(pdf, dept_avg):
    """Add department-wise performance analysis"""
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. Department-wise Performance", ln=True)

    pdf.set_font("Arial", size=11)
    for dept, avg in dept_avg.items():
        pdf.cell(0, 8, f"{dept}: Average Score = {avg}", ln=True)

    pdf.ln(5)


def add_employee_table(pdf, employees):
    """Add detailed employee table"""
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "3. Employee-wise Detailed Scores", ln=True)

    pdf.set_font("Arial", "B", 11)
    col_widths = [60, 60, 30]

    headers = ["Name", "Department", "Score"]
    for i in range(len(headers)):
        pdf.cell(col_widths[i], 10, headers[i], border=1, align="C")
    pdf.ln()

    pdf.set_font("Arial", size=11)
    for emp in employees:
        pdf.cell(col_widths[0], 10, emp["name"], border=1)
        pdf.cell(col_widths[1], 10, emp["department"], border=1)
        pdf.cell(col_widths[2], 10, str(emp["score"]), border=1, align="C")
        pdf.ln()

    pdf.ln(5)


def add_conclusion(pdf, stats):
    """Add concluding remarks"""
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "4. Conclusion", ln=True)

    pdf.set_font("Arial", size=11)
    pdf.multi_cell(
        0,
        8,
        f"The overall average performance score of employees is "
        f"{stats['average_score']}. Continuous monitoring and "
        f"targeted improvements can help increase overall productivity."
    )


# ------------------- MAIN CONTROLLER ----------------------


def generate_report():
    """Main function to generate PDF report"""

    check_file_exists(DATA_FILE)

    employees = read_csv_data(DATA_FILE)

    stats = calculate_statistics(employees)

    dept_avg = department_wise_average(employees)

    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=PAGE_MARGIN)
    pdf.add_page()

    add_report_metadata(pdf)
    add_summary_section(pdf, stats)
    add_department_analysis(pdf, dept_avg)
    add_employee_table(pdf, employees)
    add_conclusion(pdf, stats)

    pdf.output(OUTPUT_FILE)
    print("PDF report generated successfully!")


# ------------------- SCRIPT ENTRY POINT -------------------

if __name__ == "__main__":
    generate_report()