import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import threading
from dotenv import load_dotenv

def send_email_async(to_email, subject, body_html):
    def send():
        load_dotenv(override=True) # Force reload to ensure latest credentials
        sender_email = os.environ.get('SMTP_EMAIL')
        sender_password = os.environ.get('SMTP_PASSWORD')
        
        if not sender_email or not sender_password:
            print(f"[MOCK EMAIL - SMTP Not Configured]")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"Body: {body_html}")
            return
            
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = f"Secure Bank <{sender_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body_html, 'html'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            print(f"Email successfully sent to {to_email}")
        except Exception as e:
            print(f"Failed to send email to {to_email}: {str(e)}")
            
    # Run in a separate thread so it doesn't block the request
    thread = threading.Thread(target=send)
    thread.start()

def send_welcome_email(to_email, user_name, account_number):
    subject = "Welcome to Secure Bank"
    body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #2563eb;">Hello {user_name},</h2>
        <p>Your bank account has been successfully created.</p>
        <p style="font-size: 18px; padding: 10px; background-color: #f3f4f6; border-radius: 5px; display: inline-block;">
            <strong>Account Number:</strong> {account_number}
        </p>
        <br><br>
        <p>Thank you for choosing Secure Bank.</p>
      </body>
    </html>
    """
    send_email_async(to_email, subject, body)

def send_transaction_email(to_email, txn_type, amount, other_account, current_balance):
    if txn_type == 'credit':
        subject = "Money Received - Secure Bank"
        action = "received"
        from_to = f"from account <strong>{other_account}</strong>"
        color = "#10b981" # Green
    else:
        subject = "Money Sent - Secure Bank"
        action = "sent"
        from_to = f"to account <strong>{other_account}</strong>"
        color = "#ef4444" # Red

    body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: {color};">Transaction Alert</h2>
        <p>You have successfully {action} <strong>${amount:.2f}</strong> {from_to}.</p>
        <p><strong>Current Balance:</strong> ${current_balance:.2f}</p>
        <br>
        <p>Thank you for choosing Secure Bank.</p>
      </body>
    </html>
    """
    send_email_async(to_email, subject, body)
