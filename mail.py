# importing libraries
import base64
import smtplib
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER']='add your server here'
app.config['MAIL_PORT'] = "add your port here"
app.config['MAIL_USERNAME'] = 'email'
app.config['MAIL_PASSWORD'] = '**********************'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
CORS(app)

@app.route('/')
def mailSend():
    try:
        msg = Message(
                    'Hello',
                    sender ='sender mail',
                    recipients = ['reciever mail']
                )
        msg.body = 'Hello Mr. user, this message sent by  Flask-Mail'
        mail.send(msg)
        return 'Email Sent'
    except Exception as e:
        print(type(e))
        print(e)
        return '<h2> Error </h2>'

if __name__ == '__main__':
    app.run(debug = True)
