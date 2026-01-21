# 📨 Logistics Email Automation Agent

**Status:** ✅ Active / Production Ready
**Tech Stack:** Python, imap-tools, Secure Environment

## 💼 The Business Case
Logistics operations face a critical bottleneck: the "Inbox Flood." Dispatch teams spend hours daily manually monitoring emails to download Invoices, Bills of Lading (BOLs), and Rate Sheets. This manual process causes payment delays, data entry errors, and operational drag.

## ✅ The Solution
This agent provides **autonomous document ingestion**. It acts as a dedicated 24/7 digital worker that securely connects to your logistics email, identifies critical documents based on your criteria, and routes them to a local folder for processing.

## 🚀 Key Capabilities
* **🔒 Enterprise-Grade Security:** Connects via standard IMAP protocols using App Passwords. Your primary login credentials are never exposed or stored in the code.
* **📂 Smart Filtering:** Unlike basic auto-downloaders, this agent uses precise server-side filtering (e.g., `Subject="Invoice"`, `Status="Unread"`) to ensure only relevant business documents are processed.
* **⚡ Zero Latency:** Captures PDF documents the moment they arrive, faster than any human operator.
* **🛡 Data Sovereignty:** Designed for privacy. Unlike cloud-based automation platforms (Zapier/Make) that process your data on third-party servers, this agent runs entirely on your local machine or private VPS. Financial data never leaves your control.

---

## 🛠 Installation

### 1. Clone the repository
```bash
git clone https://github.com/SamSanchezFlores/logistics-email-agent.git
cd logistics-email-agent

```

### 2. Configure the Environment

We use a virtual environment to ensure stability and isolate dependencies.

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Secure Your Credentials

Create a `.env` file in the root directory to store your keys securely. **Do not share this file.**

```ini
EMAIL_ADDRESS="your_target_email@gmail.com"
EMAIL_PASSWORD="xxxx xxxx xxxx xxxx" 
# NOTE: Requires a Google App Password for security.

```

---

## ⚙ Usage

1. **Test Connection**
Verifies the secure handshake with the mail server and lists available folders.

```bash
python src/connect_test.py

```

2. **Run the Ingestor**
Scans for unread emails matching your criteria (e.g., "Invoice"), downloads the PDF attachments, and marks the email as processed.

```bash
python src/fetch_invoices.py

```

3. **View Output**

* **Logs:** Real-time status updates are printed to the console in structured JSON.
* **Files:** Retrieved documents are saved to the `downloads/` directory.

---

## 📊 Sample Output Log

**Structured JSON Output (Headless Mode):**

```json
{
  "status": "complete",
  "emails_processed": 2,
  "details": [
    {
      "email_subject": "Invoice #9921 - Global Freight",
      "sender": "billing@globalfreight.com",
      "files_downloaded": [
        "invoice_9921.pdf"
      ],
      "status": "success"
    }
  ]
}

```

**Maintainer:** Sam Sanchez
