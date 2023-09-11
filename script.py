# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
import datetime

# Database connection parameters
db_host = "****"
db_user = "****"
db_password = "****"
db_name = "****"

# Email configuration
sender_email = "****"
receiver_email = "****"
email_password = "*****"
smtp_server = "****"

# Initialize the 'conn' variable to None
conn = None

try:
    # Connect to the database
    conn = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = conn.cursor()

    # Check if the connection is open
    if conn.is_connected():
        # Retrieve ticket statistics for the day
        today = datetime.date.today()
        cursor.execute("SELECT COUNT(*) FROM tbltickets WHERE DATE(date) = %s", (today,))
        ticket_count = cursor.fetchone()[0]

        # Retrieve the number of responded tickets
        cursor.execute("SELECT COUNT(*) FROM tbltickets WHERE DATE(date) = %s AND status = '3'", (today,))
        responded_count = cursor.fetchone()[0]

        # Retrieve the number of closed tickets
        cursor.execute("SELECT COUNT(*) FROM tbltickets WHERE DATE(date) = %s AND status = '5'", (today,))
        closed_count = cursor.fetchone()[0]

        # Compose the email message
        subject = "Daily Ticket Statistics"
        body = "Date: {}\nTotal Tickets: {}\nResponded Tickets: {}\nClosed Tickets: {}".format(
        today, ticket_count, responded_count, closed_count)
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # Send the email
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

except mysql.connector.Error as e:
    print("Error connecting to the database:", e)

except Exception as e:
    print("An error occurred:", e)

finally:
    if conn is not None and conn.is_connected():
        cursor.close()
        conn.close()
