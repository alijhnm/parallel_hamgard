import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def thread_email(func):
    def wrapper(subject, email_text, reciever_emails, *args, **kwargs):
        print("ARGS: ", args)
        print("KWARGS: ", kwargs)
        thread = threading.Thread(target=func, args=(subject, email_text, reciever_emails, *args, *kwargs), daemon=False)
        thread.start()
    return wrapper


@thread_email
def send_html_mail(subject, email_text, receiver_emails,
                   host="smtp.gmail.com",
                   port=465,
                   username="hamgard.invitation@gmail.com",
                   password="Tahlil9798"):

    print("In send_html_mail. Sending email.")
    print("subject", subject)
    print("email_text", email_text)
    print("receiver_emails", receiver_emails)
    print("host", host)
    print("port", port)
    print("username", username)
    print("password", password)
    print("!@$@RGQASDXFafadsgzCDF")
    try:
        server = smtplib.SMTP_SSL(host, port)
        server.ehlo()
        server.login(username, password)
        print("Connected to SMTP server.")
    except Exception as e:
        print("unable to connect to SMTP server\nError text: {error_text}".format(error_text=e))
        return

    message = MIMEMultipart('alternative')
    message["Subject"] = subject
    message["From"] = username

    text = MIMEText(email_text, "html")
    message.attach(text)
    for email in receiver_emails:
        message["To"] = email
        try:
            server.sendmail(username, email, message.as_string())
            print("Email sent to {}".format(email))
        except Exception as e:
            print(e)

