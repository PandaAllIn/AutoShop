import stripe
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API key securely (using environment variable)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

if not stripe.api_key:
    print("Warning: STRIPE_SECRET_KEY not found in environment variables.")
    # In a real application, you might raise an error or handle this differently
else:
    print("Stripe client initialized.")

# TODO: Implement Payment Intent creation logic (Phase 1)
# Example function structure:
# def create_stripe_payment_intent(amount_cents, currency="usd", customer_id=None, metadata=None):
#     """Creates a Stripe Payment Intent."""
#     if not stripe.api_key:
#         print("Error: Stripe API key not configured.")
#         return None
#     try:
#         # ... (Implementation based on Section VI.B sample code) ...
#         pass
#     except stripe.error.StripeError as e:
#         print(f"Stripe API error creating Payment Intent: {e}")
#         return None
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         return None

# TODO: Implement other Stripe related functions as needed (e.g., retrieving intent, handling webhooks - potentially in webhook_server.py)
