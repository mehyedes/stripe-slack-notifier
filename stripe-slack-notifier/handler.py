from slack_webhook import Slack
import json

def get_slack_secret(secret_name):
    secret_file = open(f"/var/openfaas/secrets/{secret_name}", 'r')
    return secret_file.read()


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """    
    payload = json.loads(req)
    amount = payload['amount']
    currency = payload['currency']
    # Make sure you create a secret named slack-webhook-url with the Webhook URL as value
    # using the faas CLI command: faas-cli secret create 
    webhook_url = get_slack_secret("slack-webhook-url")
    try:
        slack = Slack(url=webhook_url)
        slack.post(text=f"You have a received a new payment of {amount} {currency} :moneybag: :tada:")
    except:
        print("An error occured when trying to send slack message.")
    else:
        print("Notification was sent successfully to Slack")
    return "Success!"