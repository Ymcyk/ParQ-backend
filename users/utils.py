from django.conf import settings
from django.core.mail import send_mail, EmailMessage

#TODO dodać w mailu informacje o pojeździe
#TODO wysyłanie raczej powinno być asynchroniczne
def send_badge(recipient, badge):
    email = EmailMessage(
        'ParQ kod QR',
        'Kod w załączniku',
        settings.EMAIL_HOST_USER,
        [recipient],
        [settings.EMAIL_HOST_USER]
        )
    try:
        email.attach_file(badge.path_to_file())
    except FileNotFoundError:
        badge.generate_image()
        email.attach_file(badge.path_to_file())

    email.send()

