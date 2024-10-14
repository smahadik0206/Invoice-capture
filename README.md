# Invoice-capture
Overview
The Invoice Capture project is designed to automate the process of extracting and processing key data from invoices. It uses various data extraction techniques (like OCR or PDF parsing) and organizes the captured information into structured formats for further use or analysis. This project simplifies the tedious task of manually handling invoices, making it faster and more efficient.

Features
Extract invoice data (such as invoice number, date, total amount, line items, etc.)
Supports multiple file formats (PDF, image files)
Data validation and error handling
Export captured data to CSV or Excel formats
User-friendly interface for uploading and managing invoices

Technologies Used
Programming Language: Python
Mindee API: For OCR and financial document processing
Flask: For building the web interface
Werkzeug: For secure file uploads and handling
SQLite3: For storing and managing the extracted invoice data
Pandas: For data manipulation and exporting
PyMuPDF (Fitz): For PDF reading and processing
Custom Python Modules: For parsing results and database interaction

invoice-capture/
│
├── app.py                    # Flask web app
├── main.py                   # Main processing functions
├── create_db.py              # Script to create and manage SQLite database
├── parse_result.py           # Module to parse extracted results
├── pdf_to_img.py             # Module to convert PDF to image for OCR
├── templates/                # HTML templates for Flask
│   └── upload.html           # Upload page
├── static/                   # Static files (CSS, JS)
├── invoices/                 # Directory to store uploaded invoices
├── output/                   # Directory for exported results (CSV, Excel)
└── requirements.txt          # Python dependencies
