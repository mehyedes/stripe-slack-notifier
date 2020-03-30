# stripe-slack-notifier

![CI](https://github.com/mehyedes/stripe-slack-notifier/workflows/CI/badge.svg?branch=master)

`stripe-slack-notifier` is an [OpenFaas](https://www.openfaas.com/) function that can be used as a webhook for sending Slack notifications when triggered by [Stripe API](https://stripe.com/) events(only `charge.succeeded` events are supported for now).

It is based on the [python3-http](https://github.com/openfaas-incubator/python-flask-template) template.

This function was created to showcase a real-world use case that onvolves [faasd](https://github.com/openfaas/faasd) and [inlets](https://github.com/inlets/inlets)

---
### TODO:
  - [ ] Add instructions on how to deploy the function
  - [ ] Add link to the blog post
