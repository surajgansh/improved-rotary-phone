import base64
from io import BytesIO
from flask import Flask, render_template_string, request
import qrcode

app = Flask(__name__)

# HTML Template with Embedded Styling & QR Generator
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PathLab Report System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f7f6; }
        .container { max-width: 800px; background: #fff; padding: 20px; margin: auto; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1, h2 { text-align: center; color: #0056b3; }
        .form-group { margin-bottom: 15px; }
        label { font-weight: bold; display: block; margin-bottom: 5px; }
        input, select { width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        button { width: 100%; background: #28a745; color: white; padding: 12px; border: none; font-size: 16px; border-radius: 4px; cursor: pointer; }
        button:hover { background: #218838; }
        .report-box { border: 2px solid #0056b3; padding: 20px; margin-top: 20px; border-radius: 8px; background: #fff; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #0056b3; color: white; }
        .qr-code { text-align: center; margin-top: 15px; }
    </style>
</head>
<body>
<div class="container">
    <h1>PathLab Management System</h1>
    <form method="POST">
        <h2>Patient Info</h2>
        <div class="grid">
            <div class="form-group">
                <label>Patient Name:</label>
                <input type="text" name="name" required>
            </div>
            <div class="form-group">
                <label>Age / Gender:</label>
                <input type="text" name="age_gender" placeholder="25 / Male" required>
            </div>
        </div>

        <h2>1. Complete Blood Count (CBC)</h2>
        <div class="grid">
            <div><label>Hemoglobin (g/dL):</label><input type="text" name="hb"></div>
            <div><label>TLC (cells/cu.mm):</label><input type="text" name="tlc"></div>
            <div><label>RBC Count (millions/cu.mm):</label><input type="text" name="rbc"></div>
            <div><label>Platelet Count (lakhs/cu.mm):</label><input type="text" name="platelet"></div>
        </div>

        <h2>2. Liver Function Test (LFT)</h2>
        <div class="grid">
            <div><label>Bilirubin Total (mg/dL):</label><input type="text" name="bili_total"></div>
            <div><label>SGOT / AST (U/L):</label><input type="text" name="sgot"></div>
            <div><label>SGPT / ALT (U/L):</label><input type="text" name="sgpt"></div>
            <div><label>Alkaline Phosphatase (U/L):</label><input type="text" name="alp"></div>
        </div>

        <h2>3. Kidney Function Test (KFT)</h2>
        <div class="grid">
            <div><label>Serum Creatinine (mg/dL):</label><input type="text" name="creatinine"></div>
            <div><label>Blood Urea (mg/dL):</label><input type="text" name="urea"></div>
            <div><label>Uric Acid (mg/dL):</label><input type="text" name="uric_acid"></div>
        </div>

        <h2>4. Lipid Profile Test (LPT)</h2>
        <div class="grid">
            <div><label>Total Cholesterol (mg/dL):</label><input type="text" name="cholesterol"></div>
            <div><label>Triglycerides (mg/dL):</label><input type="text" name="triglycerides"></div>
            <div><label>HDL Cholesterol (mg/dL):</label><input type="text" name="hdl"></div>
            <div><label>LDL Cholesterol (mg/dL):</label><input type="text" name="ldl"></div>
        </div>

        <br>
        <button type="submit">Generate Report & QR</button>
    </form>

    {% if data %}
    <div class="report-box" id="report">
        <h2>CITY PATHOLOGY LAB</h2>
        <p><strong>Patient Name:</strong> {{ data.name }} | <strong>Age/Gender:</strong> {{ data.age_gender }}</p>
        <hr>
        <table>
            <tr><th>Test Name</th><th>Observed Value</th></tr>
            {% for key, val in data.items() %}
            {% if key not in ['name', 'age_gender'] and val %}
            <tr><td>{{ key|upper }}</td><td>{{ val }}</td></tr>
            {% endif %}
            {% endfor %}
        </table>
        
        <div class="qr-code">
            <h3>Report QR Code</h3>
            <img src="data:image/png;base64,{{ qr_img }}" alt="QR Code">
        </div>
    </div>
    {% endif %}
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form.to_dict()

        # QR Code Generator logic
        qr_text = f"PathLab Report\nName: {data.get('name')}\nHb: {data.get('hb')}\nCreatinine: {data.get('creatinine')}\nSGPT: {data.get('sgpt')}"
        qr = qrcode.make(qr_text)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_img = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return render_template_string(HTML_TEMPLATE, data=data, qr_img=qr_img)

    return render_template_string(HTML_TEMPLATE, data=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
