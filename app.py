import os, secrets, datetime, subprocess
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads"))
INVOICE_FOLDER = os.environ.get("INVOICE_FOLDER", os.path.join(BASE_DIR, "invoices"))
MAX_MB = float(os.environ.get("MAX_CONTENT_LENGTH_MB", "25"))
ALLOWED_EXTS = {"pdf","txt","doc","docx","png","jpg","jpeg"}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", secrets.token_hex(16))
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["INVOICE_FOLDER"] = INVOICE_FOLDER
app.config["MAX_CONTENT_LENGTH"] = int(MAX_MB * 1024 * 1024)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["INVOICE_FOLDER"], exist_ok=True)

# --- Service catalog (per-unit prices) ---
SERVICES = {
    "bw_pages": {"label": "B/W Printing (per page)", "price": 1.0},
    "color_pages": {"label": "Color Printing (per page)", "price": 3.0},
    "scan_pages": {"label": "Scanning (per page)", "price": 2.0},
    "lamination_sheets": {"label": "Lamination (per sheet)", "price": 20.0},
    "binding_count": {"label": "Binding (per book)", "price": 30.0},
}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTS

# --- Routes ---
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", services=SERVICES)

@app.route("/checkout", methods=["POST"])
def checkout():
    customer_name = request.form.get("customer_name","").strip()
    contact = request.form.get("contact","").strip()
    file = request.files.get("file")

    if not customer_name:
        flash("Customer name is required.", "error")
        return redirect(url_for("index"))

    saved_filename = None
    if file and file.filename:
        if not allowed_file(file.filename):
            flash("File type not allowed.", "error")
            return redirect(url_for("index"))
        ext = file.filename.rsplit(".",1)[1].lower()
        saved_filename = f"{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}-{secrets.token_hex(4)}.{ext}"
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], saved_filename)
        file.save(save_path)
    else:
        flash("Please attach a file to print.", "error")
        return redirect(url_for("index"))

    # Build line items
    items = []
    subtotal = 0.0
    for key, meta in SERVICES.items():
        qty_str = request.form.get(key, "0").strip()
        try:
            qty = int(qty_str) if qty_str else 0
        except ValueError:
            qty = 0
        if qty > 0:
            line_total = qty * meta["price"]
            items.append({
                "label": meta["label"],
                "qty": qty,
                "price": meta["price"],
                "total": line_total
            })
            subtotal += line_total

    tax_rate = 0.18  # 18% GST example
    tax = round(subtotal * tax_rate, 2)
    total = round(subtotal + tax, 2)

    order_id = secrets.token_hex(6).upper()
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Render invoice HTML to file
    invoice_filename = f"invoice-{order_id}.html"
    invoice_path = os.path.join(app.config["INVOICE_FOLDER"], invoice_filename)
    from flask import render_template_string
    html = render_template("invoice.html",
                           order_id=order_id, ts=ts,
                           customer_name=customer_name, contact=contact,
                           uploaded_filename=saved_filename, items=items,
                           subtotal=subtotal, tax=tax, total=total)
    with open(invoice_path, "w", encoding="utf-8") as f:
        f.write(html)

    return render_template("invoice.html",
                           order_id=order_id, ts=ts,
                           customer_name=customer_name, contact=contact,
                           uploaded_filename=saved_filename, items=items,
                           subtotal=subtotal, tax=tax, total=total,
                           invoice_download=url_for("get_invoice", filename=invoice_filename))

@app.route("/invoices/<path:filename>")
def get_invoice(filename):
    return send_from_directory(app.config["INVOICE_FOLDER"], filename, as_attachment=True)

@app.route("/uploads/<path:filename>")
def get_upload(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

# Optional: stub route to attempt server-side print (won't work in Codespaces printers)
@app.route("/api/print-upload/<path:filename>", methods=["POST"])
def print_upload(filename):
    # This would work only on a Linux host with CUPS and lp installed
    try:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        if not os.path.exists(file_path):
            return {"ok": False, "error": "File not found"}, 404
        # WARNING: Disabled by default in Codespaces
        # result = subprocess.run(["lp", file_path], capture_output=True, text=True, check=False)
        # return {"ok": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr}, 200
        return {"ok": False, "error": "Server-side printing disabled in Codespaces. Download and print locally."}, 501
    except Exception as e:
        return {"ok": False, "error": str(e)}, 500


# --- Main ---
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))  # fallback to 8000 instead of 5000
    app.run(host="0.0.0.0", port=port, debug=True)

# To run locally: set FLASK_APP=app.py and flask run


