# Authorized PDF Password Tester (using pikepdf)

> **Purpose:** a small, *authorized* utility that attempts all CPF combinations as passwords against a PDF.  
> **Important:** This tool **must only** be used on PDFs you own or have explicit permission to test. Do **not** use it to attempt unauthorized access.

---

## Legal & Ethical notice

By using this tool you confirm that:
- You are the owner of the PDF **or**
- You have explicit, written permission from the owner to test passwords on the PDF.

Unauthorized access to computer systems, files, or data is illegal in many jurisdictions. The author of this script is not responsible for misuse.

---

## Requirements

- Python 3.8+
- `pikepdf` installed in a virtual environment (recommended)

Install dependencies (recommended inside a `venv`):

```bash
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install --upgrade pip
pip install pikepdf
```

- Save the file as invoice.pdf or if you prefer, change the filename in code
- Run the script