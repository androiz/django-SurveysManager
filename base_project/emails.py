from django.core.mail import send_mail

def account_activation_email(url, email_to):
    print url
    send_mail(
        'Account activation',
        'You can activate your account with this link.\n\n' + url,
        'androiz10@gmail.com',
        [email_to],
        fail_silently=False,
    )

    return True