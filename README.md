# stripe-slack-notifier

![CI](https://github.com/mehyedes/stripe-slack-notifier/workflows/CI/badge.svg?branch=master)

`stripe-slack-notifier` is an [OpenFaaS](https://www.openfaas.com/) function that can be used as a webhook for sending Slack notifications when triggered by [Stripe API](https://stripe.com/) events( only `charge.succeeded` events are supported for now).

This function was created to showcase a real-world use case that involves [faasd](https://github.com/openfaas/faasd) and [inlets](https://github.com/inlets/inlets).

More details can found on the blog post on [myedes.io](https://myedes.io/stripe-serverless-webhook-faasd/).

## Deployment to OpenFaaS

Clone the repository:
```bash
$ git clone https://github.com/mehyedes/stripe-slack-notifier.git
$ cd stripe-slack-notifier/
```
Fetch the `python3-http` template:
```bash
$ faas-cli template pull stack -f stripe-slack-notifier.yml
```
Create the necessary secrets for the function:
```bash
$ export ${OPENFAAS_GATEWAY_URL}
$ faas-cli secret create slack-webhook-url \
  --from-literal=${SLACK_WEBHOOK_URL} --gateway ${OPENFAAS_GATEWAY_URL}
$ faas-cli secret create stripe-secret-key \
  --from-literal=${STRIPE_API_KEY} --gateway ${OPENFAAS_GATEWAY_URL}
$ faas-cli secret create webhook-secret \
  --from-literal=${WEBHOOK_SIGNING_SECRET} --gateway ${OPENFAAS_GATEWAY_URL}
$ faas-cli secret list --gateway ${OPENFAAS_GATEWAY_URL}
NAME
slack-webhook-url
stripe-secret-key
webhook-secret
```
Deploy to the OpenFaaS gateway
```bash
$ faas-cli deploy -f stripe-slack-notifier.yml --gateway ${OPENFAAS_GATEWAY_URL}
```
