import json
import os
from jinja2 import Template
from weasyprint import HTML, CSS

OUTPUT_DIR = "output"
INPUT_FILE = os.path.join(OUTPUT_DIR, "content.json")
OUTPUT_PDF = os.path.join(OUTPUT_DIR, "strategic_report.pdf")


CSS_STYLES = """
@page {
    size: A4;
    margin: 2.5cm;
    @top-right {
        content: "CONFIDENTIAL | Inuvaira";
        font-family: 'Helvetica', sans-serif;
        font-size: 8pt;
        color: #7f8c8d;
    }
    @bottom-center {
        content: "Page " counter(page);
        font-family: 'Helvetica', sans-serif;
        font-size: 9pt;
        color: #7f8c8d;
    }
}

body {
    font-family: 'Helvetica', sans-serif;
    color: #333;
    line-height: 1.6;
    font-size: 11pt;
}

/* Cover Page Styling */
.cover-page {
    text-align: center;
    padding-top: 35%;
    break-after: page;
}

h1.title {
    font-size: 36pt;
    color: #2c3e50;
    margin-bottom: 20px;
    font-weight: bold;
}

.subtitle {
    font-size: 16pt;
    color: #7f8c8d;
    margin-bottom: 15px; /* Reduced margin to fit Author line */
}

.author-line {
    font-size: 14pt;
    color: #2980b9; /* Professional Blue for Author */
    margin-bottom: 60px;
    font-weight: bold;
}

/* Section Styling */
h2 {
    color: #2980b9;
    border-bottom: 2px solid #eee;
    padding-bottom: 10px;
    margin-top: 35px;
}

/* Table Styling */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 25px 0;
    font-size: 10pt;
    border: 1px solid #eee;
}

thead tr {
    background-color: #2c3e50;
    color: #ffffff;
    text-align: left;
}

th, td {
    padding: 12px 15px;
    border-bottom: 1px solid #ddd;
}

tbody tr:nth-of-type(even) {
    background-color: #f8f9fa;
}

tbody tr:last-of-type {
    border-bottom: 2px solid #2c3e50;
}
"""

def generate_pdf():
    # A. Load the JSON Content
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run the content generator first.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"--> Loaded data for report: {data['meta']['title']}")

    # B. Define the HTML Template
    # UPDATED: Added the author-line div
    html_template_string = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ data.meta.title }}</title>
        <meta charset="utf-8">
    </head>
    <body>
        <div class="cover-page">
            <h1 class="title">{{ data.meta.title }}</h1>
            
            <div class="subtitle">Prepared for: {{ data.meta.client }}</div>
            
            <div class="author-line">Report Author: {{ data.meta.author }}</div>
            
            <p><strong>Date:</strong> {{ data.meta.date }}</p>
        </div>

        {% for section in data.sections %}
            <div class="section">
                <h2>{{ section.heading }}</h2>
                <p>{{ section.content }}</p>

                {% if section.table_data %}
                <table>
                    <thead>
                        <tr>
                            {% for col in section.table_data.columns %}
                                <th>{{ col }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in section.table_data.rows %}
                            <tr>
                                {% for cell in row %}
                                    <td>{{ cell }}</td>
                                {% endfor %}
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% endif %}
            </div>
        {% endfor %}
    </body>
    </html>
    """

    # C. Render HTML
    template = Template(html_template_string)
    rendered_html = template.render(data=data)

    # D. Convert to PDF
    print("--> Rendering PDF...")
    try:
        html = HTML(string=rendered_html)
        css = CSS(string=CSS_STYLES)
        html.write_pdf(OUTPUT_PDF, stylesheets=[css])
        print(f"--> Success! Report generated at: {OUTPUT_PDF}")
        
        if os.name == 'nt': # Windows
            os.startfile(OUTPUT_PDF)
        elif os.name == 'posix': # Mac/Linux
            try: os.system(f"open '{OUTPUT_PDF}'") 
            except: pass

    except Exception as e:
        print(f"Error generating PDF: {e}")

if __name__ == "__main__":
    generate_pdf()