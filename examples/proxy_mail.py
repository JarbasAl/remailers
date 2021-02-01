from remailers.mail import send_tor_email

# temp_email + tor .....
# https://www.smtp2go.com
YOUR_EMAIL_ADDRESS = "me@email.fake"
DESTINATARY_ADDRESS = "you@email.fake"
YOUR_PASSWORD = "FlJaBf34dYz1"

subject = 'why'
body = 'this is a test bruh'

send_tor_email(YOUR_EMAIL_ADDRESS, YOUR_PASSWORD,
               DESTINATARY_ADDRESS, subject, body)

