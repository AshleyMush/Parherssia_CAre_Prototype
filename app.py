from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from forms import CallbackForm, ContactForm
import smtplib
from email.mime.text import MIMEText
import os
from twilio.rest import Client



app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap5(app)




ADMIN_EMAIL_ADDRESS = os.environ.get("EMAIL_KEY")
ADMIN_EMAIL_PW = os.environ.get("PASSWORD_KEY")


# ---Twilio api Variables----
twilio_number = os.environ.get('twilio_number')
admin_number = os.environ.get('admin_number')
account_sid = os.environ.get('account_sid')
auth_token = os.environ.get('auth_token')
client = Client(account_sid, auth_token)






@app.route('/', methods=['GET', 'POST'])
def go_home():
    callback_form = CallbackForm()
    contact_form = ContactForm()

    if callback_form.validate_on_submit() and callback_form.data:
        callback_name = callback_form.callback_name.data
        callback_number = callback_form.callback_number.data
        callback_message = callback_form.callback_message.data
        # Process the form data
        print(f'🟩Call Back data:\n'
              f'{callback_name}\n'
              f'{callback_number}\n'
              f'{callback_message}')

        send_admin_sms(name=callback_name,number=callback_number,callback_message=callback_message)


    if contact_form.validate_on_submit() and contact_form.data:

        name = contact_form.name.data
        email = contact_form.email.data
        subject = contact_form.subject.data
        message = contact_form.message.data
        print(f'🟩Sending contact form data:\n'
              f'{name}\n'
              f'{email}\n'
              f'{subject}\n'
              f'{message}\n')

        send_confirmation_email(name=name,email=email,subject=subject)
        send_admin_email(name=name, subject=subject,email=email,message=message)


    return render_template('index.html', callback_form=callback_form, contact_form=contact_form)


@app.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    contact_form = ContactForm()

    if contact_form.validate_on_submit() and contact_form.data:

        name = contact_form.name.data
        email = contact_form.email.data
        subject = contact_form.subject.data
        message = contact_form.message.data
        print(f'🟩Sending contact form data:\n'
              f'{name}\n'
              f'{email}\n'
              f'{subject}\n'
              f'{message}\n')

        send_confirmation_email(name=name,email=email,subject=subject)
        send_admin_email(name=name, subject=subject,email=email,message=message)


    return render_template('contact.html', contact_form=contact_form)

@app.route('/callback')
def callback():
    return render_template('callback.html')

@app.route('/jobs')
def get_jobs():
    return render_template('join-us.html')


@app.route('/services')
def services():
    return render_template('service.html')

@app.route('/about')
def get_about():
    return render_template('about-us.html')

@app.route('/complex')
def complex():
    return render_template('complex.html')


@app.route('/personal-care')
def personal_care():
    return render_template('personalcare.html')

@app.route('/live-in')
def livein():
    return render_template('live-in.html')

@app.route('/palliative')
def palliative():
    return render_template('palliative.html')

@app.route('/respite')
def respite():
    return render_template('respite.html')

@app.route('/practical-support')
def practicalsupport():
    return render_template('practicalsupport.html')







@app.route('/example')
def get_something():
    return render_template('about-us.html')

def send_confirmation_email(name, email, subject, service='gmail'):
    # Email content
    email_content = render_template('user_email.html', name=name)

    # MIMEText logic
    msg = MIMEText(email_content, 'html')
    msg['From'] = ADMIN_EMAIL_ADDRESS
    msg['To'] = email  # Send to the user's email
    msg['Subject'] = f"Confirmation: {subject}"
    msg['Reply-To'] = ADMIN_EMAIL_ADDRESS


    # ---SMTP logic-----

    smtp_settings = {
        'gmail': ('smtp.gmail.com', 587),
        'yahoo': ('smtp.mail.yahoo.com', 587),
        'outlook': ('smtp.office365.com', 587)
        # Add more services as needed
    }

    if service in smtp_settings:
        smtp_server, smtp_port = smtp_settings[service]
    else:
        raise ValueError("Unsupported email service")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            connection.login(ADMIN_EMAIL_ADDRESS, ADMIN_EMAIL_PW)
            connection.sendmail(ADMIN_EMAIL_ADDRESS, email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
        render_template('index.html')


def send_admin_email(name, subject, email, message, service='gmail'):


    email_content = render_template('admin_email.html', name=name, subject=subject, email=email,
                                    message=message)

    # -- MIMETEXT logic ---

    msg = MIMEText(email_content, 'html')
    msg['From'] = email
    msg['To'] = ADMIN_EMAIL_ADDRESS
    msg['Subject'] = f"New message from {name}: {subject}"
    msg['Reply-To'] = email

    # ---SMTP logic-----

    smtp_settings = {
        'gmail': ('smtp.gmail.com', 587),
        'yahoo': ('smtp.mail.yahoo.com', 587),
        'outlook': ('smtp.office365.com', 587)
        # Add more services as needed
    }

    if service in smtp_settings:
        smtp_server, smtp_port = smtp_settings[service]
    else:
        raise ValueError("Unsupported email service")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            connection.login(ADMIN_EMAIL_ADDRESS, ADMIN_EMAIL_PW)
            connection.sendmail(from_addr=email, to_addrs=ADMIN_EMAIL_ADDRESS,
                                msg=msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
        render_template('index.html')


def send_admin_sms(name, number, callback_message):
    """Sends the a message to the admin number using twilio api, letting the admin know the name,number and message the user has entered on the callback form"""
    message_body = (
        f"📞 Callback Request from Parrhesia Website\n\n"
        f"Name: {name}\n"
        f"Phone: {number}\n"
        f"Message: {callback_message}\n\n"
        f"Please reach out to the requester promptly."
    )

    message = client.messages.create(
        from_=twilio_number,
        body=message_body,
        to=admin_number
    )

    print(f"SMS sent successfully. Message SID: {message.sid}")







if __name__ == "__main__":
    app.run(debug=True, port=5002)