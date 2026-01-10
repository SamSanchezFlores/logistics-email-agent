# src/connect_test.py

# ---------------------------------------------------------
# IMPORT STATEMENTS
# ---------------------------------------------------------

# 'os' allows us to interact with the operating system (specifically to read environment variables)
import os

# 'json' allows us to format our output as structured data (The "Headless" Rule)
import json

# 'load_dotenv' is the function that reads our secret .env file
from dotenv import load_dotenv

# 'MailBox' is the main tool from the 'imap-tools' library that handles the connection
from imap_tools import MailBox

# ---------------------------------------------------------
# CONFIGURATION & SETUP
# ---------------------------------------------------------

# 1. Load the environment variables from the .env file into Python's memory.
#    This keeps passwords out of the code itself.
load_dotenv()

# 2. Retrieve the credentials.
#    We use .get() to avoid crashing if the variable is missing (it just returns None).
USERNAME = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

# ---------------------------------------------------------
# MAIN LOGIC
# ---------------------------------------------------------

def test_connection():
    """
    Connects to Gmail to verify credentials.
    Returns: JSON object with success status and folder list.
    """
    
    # Safety Check: Did we actually find the credentials?
    if not USERNAME or not PASSWORD:
        error_msg = {
            "status": "error",
            "message": "Credentials missing. Check .env file."
        }
        print(json.dumps(error_msg, indent=2))
        return

    try:
        # 3. Establish the Connection
        #    'imap.gmail.com' is the server address for Google.
        #    The 'with' statement ensures the connection closes automatically when done (prevents memory leaks).
        with MailBox('imap.gmail.com').login(USERNAME, PASSWORD) as mailbox:
            
            # 4. Fetch Folders (Labels)
            #    We loop through mailbox.folder.list() and grab the .name of each one.
            #    This proves we have deep access to the account.
            folders = [f.name for f in mailbox.folder.list()]
            
            # 5. Build the Success Payload
            #    This dictionary is what n8n or the user will see.
            result = {
                "status": "success",
                "message": "Authentication successful.",
                "account": USERNAME,
                "folder_count": len(folders),
                # We slice [:5] to show only the first 5 folders (keeps the output clean)
                "folder_sample": folders[:5]
            }
            
            # 6. Print the JSON (The Final Output)
            print(json.dumps(result, indent=2))

    except Exception as e:
        # 7. Error Handling
        #    If the password is wrong or internet is down, this block runs.
        error_result = {
            "status": "error",
            "message": str(e),
            "hint": "Ensure 'Less Secure Apps' is allowed OR use an App Password."
        }
        print(json.dumps(error_result, indent=2))

# ---------------------------------------------------------
# EXECUTION
# ---------------------------------------------------------

# This check ensures the code only runs if we execute this file directly.
if __name__ == "__main__":
    test_connection()