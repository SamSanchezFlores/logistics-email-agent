import os
import json
from dotenv import load_dotenv
from imap_tools import MailBox, A

# Load environment variables
load_dotenv()
USERNAME = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")
DOWNLOAD_FOLDER = "downloads"

# Ensure download directory exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def fetch_invoices():
    """
    Connects to IMAP, searches for unread emails with 'Invoice' in subject,
    and downloads PDF attachments to the local folder.
    """
    processed_log = []

    try:
        # Connect to Gmail via IMAP
        with MailBox('imap.gmail.com').login(USERNAME, PASSWORD) as mailbox:
            
            # Define search criteria: Unread messages AND Subject contains "Invoice"
            criteria = A(seen=False, subject='Invoice')
            
            # Fetch messages and mark as read (seen)
            for msg in mailbox.fetch(criteria, mark_seen=True):
                files_saved = []
                
                # Iterate through attachments
                for att in msg.attachments:
                    if att.filename.lower().endswith('.pdf'):
                        # Construct unique filename using Message ID to prevent overwrites
                        filename = f"{msg.uid}_{att.filename}"
                        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
                        
                        # Save payload locally
                        with open(filepath, 'wb') as f:
                            f.write(att.payload)
                        
                        files_saved.append(filename)

                # Log successful extractions
                if files_saved:
                    entry = {
                        "email_subject": msg.subject,
                        "sender": msg.from_,
                        "date": str(msg.date),
                        "files_downloaded": files_saved,
                        "status": "success"
                    }
                    processed_log.append(entry)

        # Output structured JSON for downstream processing
        result = {
            "status": "complete",
            "emails_processed": len(processed_log),
            "details": processed_log
        }
        print(json.dumps(result, indent=2))

    except Exception as e:
        # Handle connection or parsing errors
        error_payload = {
            "status": "error",
            "message": str(e)
        }
        print(json.dumps(error_payload, indent=2))

if __name__ == "__main__":
    fetch_invoices()