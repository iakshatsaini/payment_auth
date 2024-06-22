from flask import Flask, request, render_template, redirect, url_for
import stripe
import paypalrestsdk
import os
from config import config
app = Flask(__name__)

# Configure Stripe
stripe.api_key = config.STRIPE_SECRET_KEY

# Configure PayPal
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": config.CLIENT_ID,
    "client_secret": config.CLIENT_SECRET
})

@app.route('/')
def index():
    return render_template('index.html', stripe_publishable_key = config.STRIPE_PUBLISHABLE_KEY)

@app.route('/charge', methods=['POST'])
def charge():
    try:
        amount = int(request.form['amount']) * 100  # Amount in cents
        customer = stripe.Customer.create(
            email=request.form['email'],
            source=request.form['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='inr',
            description='Flask Charge'
        )
        return redirect(url_for('success'))
    except stripe.error.StripeError as e:
        return str(e)

@app.route('/success')
def success():
    return "Payment Successful"

@app.route('/send_payment', methods=['POST'])
def send_payment():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": url_for('payment_executed', _external=True),
            "cancel_url": url_for('payment_cancelled', _external=True)
        },
        "transactions": [{
            "amount": {
                "total": request.form['amount'],
                "currency": "INR"
            },
            "description": "Payment from Flask App"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                return redirect(approval_url)
    else:
        return payment.error

@app.route('/payment_executed')
def payment_executed():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return "Payment executed successfully"
    else:
        return payment.error

@app.route('/payment_cancelled')
def payment_cancelled():
    return "Payment cancelled"

if __name__ == '__main__':
    app.run(debug=True)
