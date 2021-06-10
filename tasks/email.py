from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_welcome_email(name,receiver):
    # Creating message subject and sender
    subject = 'Welcome to tasking application'
    sender = 'mwangiapps1992@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('email/registeremail.txt',{"name": name})
    html_content = render_to_string('email/registeremail.html',{"name": name})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()


def send_tasking_notification_email(user):
    # Creating message subject and sender
    subject = 'New task'
    sender = 'mwangiapps1992@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('email/notifyemail.txt',{"name": user.username})
    html_content = render_to_string('email/notifyemail.html',{"name": user.username})

    msg = EmailMultiAlternatives(subject,text_content,sender,[user.email])
    msg.attach_alternative(html_content,'text/html')
    msg.send()