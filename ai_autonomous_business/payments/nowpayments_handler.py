import requests
import json
import hmac
import hashlib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

NOWPAYMENTS_API_KEY = os.getenv("NOWPAYMENTS_API_KEY")
NOWPAYMENTS_IPN_SECRET = os.getenv("NOWPAYMENTS_IPN_SECRET") # For webhook verification
NOWPAYMENTS_API_URL = "https://api.nowpayments.io/v1"

if not NOWPAYMENTS_API_KEY:
    print("Warning: NOWPAYMENTS_API_KEY not found in environment variables.")
if not NOWPAYMENTS_IPN_SECRET:
    print("Warning: NOWPAYMENTS_IPN_SECRET not found (needed for IPN verification).")

# TODO: Implement NOWPayments API request helper function (Phase 1)
# Example structure based on Section VI.C:
# def nowpayments_request(method, endpoint, params=None, data=None):
#     """Sends a request to the NOWPayments API."""
#     if not NOWPAYMENTS_API_KEY:
#         print("Error: NOWPayments API key not configured.")
#         return None
#     url = f"{NOWPAYMENTS_API_URL}/{endpoint}"
#     headers = {"x-api-key": NOWPAYMENTS_API_KEY}
#     # ... (Add Content-Type for POST/PUT, implement retries, error handling) ...
#     try:
#         # ... (Make request using requests library) ...
#         pass
#     except requests.exceptions.RequestException as e:
#         print(f"NOWPayments API request error: {e}")
#         return None
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         return None

# TODO: Implement invoice creation logic (Phase 1)
# Example function structure based on Section VI.C:
# def create_nowpayments_invoice(price_usd, pay_currency, order_id, callback_url, description=None, fixed_rate=False):
#     """Creates a NOWPayments invoice."""
#     # ... (Call nowpayments_request helper) ...
#     pass

# TODO: Implement payment status check logic (Phase 1 / 3)
# Example function structure based on Section VI.C:
# def get_nowpayments_status(payment_id):
#     """Gets the status of a NOWPayments payment."""
#     # ... (Call nowpayments_request helper) ...
#     pass

# TODO: Implement IPN verification logic (Phase 1 - in webhook_server.py)
# Example function structure based on Section VI.C:
# def verify_nowpayments_ipn(request_data_dict, signature_header):
#     """Verifies the signature of an incoming NOWPayments IPN."""
#     # ... (Implementation using NOWPAYMENTS_IPN_SECRET) ...
#     pass

print("NOWPayments handler structure created.")
