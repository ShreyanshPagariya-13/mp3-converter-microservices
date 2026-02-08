import smtplib, os, json, traceback
from email.message import EmailMessage

def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_address = os.environ.get("GMAIL_ADDRESS")
        sender_password = os.environ.get("GMAIL_PASSWORD")
        receiver_address = message.get("username")

        if not receiver_address:
            raise ValueError("message missing 'username' (receiver email)")
        if not sender_address or not sender_password:
            raise ValueError("GMAIL_ADDRESS and GMAIL_PASSWORD must be set")

        msg = EmailMessage()
        msg.set_content(f"mp3 file_id: {mp3_fid} is now ready!")
        msg["Subject"] = "MP3 Download"
        msg["From"] = sender_address
        msg["To"] = receiver_address

        session = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login(sender_address, sender_password.strip())
        session.send_message(msg)
        session.quit()
        print(f"Mail sent to {receiver_address}")
    except Exception as err:
        print(f"notification error: {type(err).__name__}: {err}")
        traceback.print_exc()
        return err