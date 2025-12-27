from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from loguru import logger
from core_apps.accounts.models import BankAccount


def send_account_creation_email(user, bank_account):
    subject = _("Your New Bank Account has been Created")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    context = {"user": user, "account": bank_account, "site_name": settings.SITE_NAME}
    """
    
    ⭐ render() = gives HTML + converts to HTTP response for browser
    ⭐ render_to_string() = gives HTML only (string) → you can use it anywhere, not only web pages
    render() send result to browser but render_to_string gives you the result you decide where to use it.
    
    """
    html_email = render_to_string("emails/account_created.html", context)
    plain_email = strip_tags(html_email)
    """
    This is used to extract only content from the html page. Incase the html cant be displayed inside gmail.
    """
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)
    """
    EmailMultiAlternatives is used to send both HTML and Plain text, Incase the email doesnt allow your page to load or be displayed.
    """
    email.attach_alternative(html_email, "text/html")
    """
    attach_alternative is saying if the html is not loading use alternative "text/html"
    """
    try:
        email.send()
        logger.info(f"Account Created email sent to: {user.email}")
    except Exception as e:
        logger.error(
            f"Failed to send account created email to {email}: Error: {str(e)}"
        )