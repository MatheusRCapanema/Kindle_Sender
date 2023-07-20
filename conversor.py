import os
from PIL import Image
from fpdf import FPDF
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def convert_jpg_to_pdf(directory, email_to):
    # Create a new PDF object
    pdf = FPDF()

    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            # Open the image file
            img = Image.open(os.path.join(directory, filename))

            # If image is in RGB mode convert it to grayscale
            if img.mode == 'RGB':
                img = img.convert('L')

            # Add a page to the PDF
            pdf.add_page()

            # Set the right size for the pdf image
            pdf.image(os.path.join(directory, filename), 0, 0, 210, 297)

    # Path where the output PDF file will be stored
    pdf_path = os.path.join(directory, "cap5.pdf")

    # Save the PDF to a file
    pdf.output(pdf_path, "F")

    # Convert the PDF file to EPUB
    convert_pdf_to_epub(pdf_path, email_to)

def convert_pdf_to_epub(pdf_path, email_to):
    # Path where the output EPUB file will be stored
    epub_path = pdf_path.replace(".pdf", ".epub")

    # Convert PDF to EPUB
    subprocess.run(["ebook-convert", pdf_path, epub_path])

    # Send the .epub file to the specified email
    send_email_with_attachment(email_to, "Converted File", epub_path)

def send_email_with_attachment(email_to, email_subject, attachment_path):
    email_from = "" # Replace with your email
    email_password = "" # Replace with your password
    smtp_server = "smtp.gmail.com" # Replace with your SMTP server
    smtp_port = 587 # Replace with your SMTP port

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = email_subject

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attachment_path, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment_path))
    msg.attach(part)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_from, email_password)
    server.send_message(msg)
    server.quit()

# Call the function
convert_jpg_to_pdf('C:/Users/mathe/Downloads/The God of High School/capitulo #5 - The God of High School', 'matheus.rocap_PWWjXe@kindle.com')
