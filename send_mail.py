import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

   
def send_mail(sender, password, receiver, subject, dates):
    """
    Sends an email using the provided sender, password, receiver, subject, and body.
    
    Args:
        sender (str): The email address of the sender.
        password (str): The password associated with the sender's email address.
        receiver (str): The email address of the receiver.
        subject (str): The subject line of the email.
        dates (str[]): A list of dates to be included in the email body.
        
    """ 


    sender_email = sender
    sender_password = password
    receiver_email = receiver

    em = MIMEMultipart()

    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject

    mail_body = f"""
                    <html>
                        <body style="margin:0;padding:0;">
                            <p style="font-size: large;">Hay citas disponibles!</p>"""
                            
    for date in dates:
        mail_body += f'<p> style="font-weight: bold;">{date}</p>'
        
    mail_body += """     
                        </body>
                    </html>
                """

    em.attach(MIMEText(mail_body, 'html'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, em.as_string())
        logging.info(f"Correo electrónico enviado correctamente a {receiver_email}")
        print(f"Correo electrónico enviado correctamente a {receiver_email}")
    except Exception as e:
        logging.info(f"No se pudo enviar el correo: {str(e)}")
        print(f"No se pudo enviar el correo: {str(e)}")
        quit()

    server.quit()
