from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

settings.configure(DEBUG=True)

## send mail(head of email, body, from email, to email as a list)
## inside the send email function for to email it was a randomly generated email. 
## from my email
def index(request):
    send_mail('head of email',
    'body text goes here',
    'rm842@nau.edu',
    ['satijop431@chinamkm.com'],
    fail_silently=False)

    return render(request,'send/index.html')

    ## todo: figure out the mass email system
    ## look over the database/archive files to set up for eaasier use
    ## finish setting up settings.py