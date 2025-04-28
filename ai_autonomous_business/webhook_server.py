import os
import json
import hmac
import hashlib
import base64
import stripe
from flask import Flask, request, abort
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Retrieve secrets from environment variables
# Note: Using SHOPIFY_API_SECRET_KEY for HMAC verification as suggested in PHASE_1_SETUP.md
SHOPIFY_WEBHOOK_SECRET = os.getenv("SHOPIFY_API_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
NOWPAYMENTS_IPN_SECRET = os.getenv("NOWPAYMENTS_IPN_SECRET")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

# Configure Stripe API key
stripe.api_key = STRIPE_SECRET_KEY

# --- Verification Functions ---

def verify_shopify_webhook(data, hmac_header):
    """Verifies the HMAC signature of an incoming Shopify webhook."""
    if not SHOPIFY_WEBHOOK_SECRET:
        print("Error: SHOPIFY_API_SECRET_KEY (for webhook verification) not set.")
        return False
    if not isinstance(data, bytes):
        data = data.encode('utf-8') # Ensure data is bytes

    calculated_hmac = base64.b64encode(hmac.new(
        SHOPIFY_WEBHOOK_SECRET.encode('utf-8'),
        data,
        hashlib.sha256
    ).digest()).decode()

    return hmac.compare_digest(calculated_hmac, hmac_header)

def verify_nowpayments_ipn(request_data_dict, signature_header):
    """Verifies the signature of an incoming NOWPayments IPN."""
    if not NOWPAYMENTS_IPN_SECRET:
        print("Error: NOWPAYMENTS_IPN_SECRET not configured.")
        return False
    if not isinstance(request_data_dict, dict):
        print("IPN verification requires data as dict.")
        return False
    if not signature_header:
        print("Error: Missing X-NOWPAYMENTS-Sig header.")
        return False

    try:
        # Recreate the exact string signed by NOWPayments:
        # Sort the dictionary by key alphabetically
        # Convert to JSON string with no spaces between separators
        sorted_data_string = json.dumps(request_data_dict, sort_keys=True, separators=(',', ':'))

        # Calculate HMAC-SHA512 signature using the IPN secret
        digest = hmac.new(
            NOWPAYMENTS_IPN_SECRET.encode('utf-8'),
            sorted_data_string.encode('utf-8'),
            hashlib.sha512
        ).hexdigest()

        # Securely compare the calculated signature with the one from the header
        if hmac.compare_digest(digest, signature_header):
            print("NOWPayments IPN Signature Verified.")
            return True
        else:
            print(f"NOWPayments IPN Signature Mismatch! Header: {signature_header}, Calculated: {digest}")
            # print(f"Data signed: {sorted_data_string}") # Uncomment for debugging
            return False
    except Exception as e:
        print(f"Error verifying NOWPayments IPN signature: {e}")
        return False

# --- Webhook Endpoints ---

@app.route('/webhooks/shopify', methods=['POST'])
def shopify_webhook():
    hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
    data = request.get_data() # Raw body needed for verification

    if not verify_shopify_webhook(data, hmac_header):
        print("Shopify webhook verification failed!")
        abort(401) # Unauthorized

    # Verification successful, process payload
    try:
        payload = json.loads(data) # Or request.get_json() if preferred after verification
        topic = request.headers.get('X-Shopify-Topic')
        print(f"--- Received Shopify Webhook ---")
        print(f"Topic: {topic}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        # TODO (Phase 2/3): Route payload to specific handlers based on topic
        return "Webhook received", 200
    except json.JSONDecodeError:
        print("Error decoding Shopify webhook JSON payload.")
        abort(400) # Bad Request
    except Exception as e:
        print(f"Error processing Shopify webhook: {e}")
        abort(500) # Internal Server Error


@app.route('/webhooks/stripe', methods=['POST'])
def stripe_webhook():
    payload_data = request.data # Raw body
    sig_header = request.headers.get('Stripe-Signature')

    if not STRIPE_WEBHOOK_SECRET:
        print("Error: STRIPE_WEBHOOK_SECRET not set.")
        abort(500)
    if not stripe.api_key:
         print("Error: STRIPE_SECRET_KEY not set for Stripe SDK.")
         abort(500)

    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload_data, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        print(f"Invalid Stripe webhook payload: {e}")
        abort(400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(f"Invalid Stripe webhook signature: {e}")
        abort(401)
    except Exception as e:
         print(f"Error constructing Stripe event: {e}")
         abort(500)

    # Handle the event
    event_type = event['type']
    event_data = event['data']['object']
    print(f"--- Received Stripe Webhook ---")
    print(f"Event Type: {event_type}")
    print(f"Event Data: {json.dumps(event_data, indent=2)}")

    # TODO (Phase 2/3): Route event to specific handlers based on event_type
    # Example:
    # if event_type == 'payment_intent.succeeded':
    #     handle_payment_success(event_data)
    # elif event_type == 'payment_intent.payment_failed':
    #     handle_payment_failure(event_data)

    return jsonify({'status': 'success'}), 200


@app.route('/webhooks/nowpayments', methods=['POST'])
def nowpayments_ipn():
    signature_header = request.headers.get('x-nowpayments-sig') # Case-insensitive header get might be safer depending on framework
    ipn_data = request.get_json()

    if not ipn_data:
        print("Error: Missing NOWPayments IPN data.")
        abort(400)

    if not verify_nowpayments_ipn(ipn_data, signature_header):
        print("NOWPayments IPN verification failed!")
        abort(401)

    # Verification successful, process payload
    print(f"--- Received NOWPayments IPN ---")
    print(f"Payload: {json.dumps(ipn_data, indent=2)}")
    payment_status = ipn_data.get('payment_status')
    order_id = ipn_data.get('order_id')
    print(f"Payment Status: {payment_status}, Order ID: {order_id}")

    # TODO (Phase 2/3): Route payload to specific handlers based on payment_status
    # Example:
    # if payment_status == 'finished':
    #     handle_nowpayments_success(ipn_data)
    # elif payment_status in ['failed', 'refunded', 'expired']:
    #     handle_nowpayments_failure(ipn_data)

    return jsonify({'status': 'IPN processed'}), 200


if __name__ == '__main__':
    # Note: Use 'flask run' command for development, which handles debugging and reloading better.
    # app.run(port=5000, debug=True) # Use debug=False in production
    print("Webhook server starting...")
    print("Ensure required environment variables are set in .env:")
    print(f"  SHOPIFY_API_SECRET_KEY: {'Set' if SHOPIFY_WEBHOOK_SECRET else 'Not Set'}")
    print(f"  STRIPE_WEBHOOK_SECRET: {'Set' if STRIPE_WEBHOOK_SECRET else 'Not Set'}")
    print(f"  NOWPAYMENTS_IPN_SECRET: {'Set' if NOWPAYMENTS_IPN_SECRET else 'Not Set'}")
    print(f"  STRIPE_SECRET_KEY: {'Set' if STRIPE_SECRET_KEY else 'Not Set'}")
    # For development, run using: flask --app webhook_server run --port 5000
    # Or if running directly: python webhook_server.py (less ideal for Flask dev)
    app.run(port=5000) # Default port 5000
