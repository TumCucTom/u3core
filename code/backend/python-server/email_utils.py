"""Email utility functions"""
import json
import logging
from io import BytesIO
import pycurl
import requests

def send_email(to_email, subject, link, code=None, postmark_api=None):
    """
    Send an email using the Postmark API
    """
    sender_email = "info@digitalU3.com"  # Client's Sender email

    # Build email content
    html_content = f"""
    <div>
        <p>Click <a href="{link}">here</a> to proceed.</p>
    """
    if code:
        html_content += f"<p>Your OTP is: <strong>{code}</strong></p>"
    html_content += "</div>"

    # Prepare payload
    payload = {
        "From": sender_email,
        "To": to_email,
        "Subject": subject,
        "HtmlBody": html_content,
        "MessageStream": "verify"
    }

    try:
        # Send request to Postmark API
        url = "https://api.postmarkapp.com/email"
        headers = [
            "Accept: application/json",
            "Content-Type: application/json",
            f"X-Postmark-Server-Token: {postmark_api}"
        ]
        data = json.dumps(payload)
        response_buffer = BytesIO()

        # Using pycurl to send the request
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

        logging.info(
            "Email sent successfully to %(email)s. Response: %(response)s",
            {"email": to_email, "response": response_body}
        )
        return True
    except requests.exceptions.RequestException as error:
        logging.error("Error sending email: %(error)s", {"error": error})
        return False