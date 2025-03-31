"""Email utility functions"""
import json
import logging
from io import BytesIO
import pycurl
import requests

def send_email(to_email, subject, link, code=None, postmark_api=None):
    """Send an email using the Postmark API"""
    postmark_token = postmark_api  # Client's Postmark server API token
    sender_email = "info@digitalU3.com" # Client's Sender email

    html_content = f"""
    <div>
        <p>Click <a href="{link}">here</a> to proceed.</p>
    """
    if code:
        html_content += f"<p>Your OTP is: <strong>{code}</strong></p>"
    html_content += "</div>"

    payload = {
        "From": sender_email,
        "To": to_email,
        "Subject": subject,
        "HtmlBody": html_content,
        "MessageStream": "verify"
    }

    try:
        url = "https://api.postmarkapp.com/email"
        headers = [
            "Accept: application/json",
            "Content-Type: application/json",
            f"X-Postmark-Server-Token: {postmark_token}"
        ]
        data = json.dumps(payload)
        response_buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.POST, 1)
        c.setopt(c.POSTFIELDS, data)
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, response_buffer)
        c.setopt(c.TIMEOUT, 30)
        c.perform()
        response_body = response_buffer.getvalue().decode('utf-8')
        c.close()
        logging.info(f"Email sent successfully to {to_email}. With {response_body}")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending email: {e}")
        return False