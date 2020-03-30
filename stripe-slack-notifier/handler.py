import stripe
from babel import numbers
from slack_webhook import Slack
from flask import Flask, request

def fetch_secret(secret_name):
    secret_file = open(f"/var/openfaas/secrets/{secret_name}", 'r')
    return secret_file.read()


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """    
    stripe.api_key = fetch_secret("stripe-secret-key")
    webhook_secret = fetch_secret("webhook-secret")
    payload = request.data.decode("utf-8")
    received_sig = request.headers.get("Stripe-Signature", None)

    # Make sure you create a secret named slack-webhook-url with the Webhook URL as value
    # using the faas CLI command: faas-cli secret create 
    webhook_url = fetch_secret("slack-webhook-url")
    try:
        event = stripe.Webhook.construct_event(
            payload, received_sig, webhook_secret
        )
    except ValueError:
        print("Error while decoding event!")
        return "Bad payload", 400
    except stripe.error.SignatureVerificationError:
        print("Invalid signature!")
        return "Bad signature", 400
    # Fail for all other event types  
    if event.type != "charge.succeeded":
        return "Unsupported event type", 422
  
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
        return "Could not send slack message", 500
    return "Notification was sent successfully to Slack", 200
