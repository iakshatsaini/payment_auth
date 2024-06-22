from flask import Flask, request, render_template, redirect, url_for, flash, session
import pyotp
from twilio.rest import Client
from config import config
app = Flask(__name__)
app.secret_key = config.APP_SECRET_KEY

TWILIO_ACCOUNT_SID = config.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = config.TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER = config.TWILIO_PHONE_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        totp = pyotp.TOTP(config.OTP_AUTH_SECRET) 
        otp = totp.now()

        client.messages.create(
            body=f'Your OTP is {otp}',
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        session['phone_number'] = phone_number
        print('OTP has been sent to your phone number', 'success')
        return redirect(url_for('verify_otp'))

    return render_template('login.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp = request.form['otp']
        totp = pyotp.TOTP(config.OTP_AUTH_SECRET) 

        if totp.verify(otp):
            print('OTP verification successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            print('Invalid OTP', 'danger')

    return render_template('verify_otp.html')

@app.route('/dashboard')
def dashboard():
    return 'Welcome to your dashboard'

if __name__ == '__main__':
    app.run(debug=True)
