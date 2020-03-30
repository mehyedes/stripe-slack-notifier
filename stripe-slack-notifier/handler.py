import stripe
from babel import numbers
from slack_webhook import Slack

def fetch_secret(secret_name):
    secret_file = open(f"/var/openfaas/secrets/{secret_name}", 'r')
    return secret_file.read()


def handle(event, context):

    # Make sure to create the secrets below
    webhook_url = fetch_secret("slack-webhook-url")
    stripe.api_key = fetch_secret("stripe-secret-key")
    webhook_secret = fetch_secret("webhook-secret")
    
    payload = event.body
    received_sig = event.headers.get("Stripe-Signature", None)
    
    try:
        event = stripe.Webhook.construct_event(
            payload, received_sig, webhook_secret
        )
    except ValueError:
        print("Error while decoding event!")
        return {
            "body": "Bad payload",
            "statusCode": 400
        }
    except stripe.error.SignatureVerificationError:
        print("Invalid signature!")
        return {
            "body": "Bad signature", 
            "statusCode": 400
        }

    # Fail for all other event types  
    if event.type != "charge.succeeded":
        return {
            "body":"Unsupported event type",
            "statusCode": 422
        }
  
    amount = numbers.format_currency(
      event.data.object.amount / 100,
      event.data.object.currency.upper(), 
      locale='en'
    )

    try:
        slack = Slack(url=webhook_url)
        slack.post(text=f"You have a received a new payment of {amount} :moneybag: :tada:")
    except:
        print("An error occured when trying to send slack message.")
        return {
            "body": "Could not send slack message", 
            "statusCode": 500
        }
    return {
        "body": "Notification was sent successfully to Slack", 
        "statusCode": 200
    }
