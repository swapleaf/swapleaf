import datetime
from random import random

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from django.db import models, IntegrityError
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.loader import render_to_string
from django.utils.hashcompat import sha_constructor
from django.utils.translation import gettext_lazy as _

from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from allauth.account.signals import email_confirmed, email_confirmation_sent

from swapleaf.settings import WEBSITE_HOMEPAGE

# this code based in-part on django-registration
class SwapLeafEmailAddressManager(models.Manager):
    
    def add_email(self, user, email):
        try:
            email_address = self.create(user=user, email=email)
            SwapLeafEmailConfirmation.objects.send_confirmation(email_address)
            return email_address
        except IntegrityError:
            return None
    
    def get_primary(self, user):
        try:
            return self.get(user=user, primary=True)
        except SwapLeafEmailAddress.DoesNotExist:
            return None
    
    def get_users_for(self, email):
        """
        returns a list of users with the given email.
        """
        # this is a list rather than a generator because we probably want to
        # do a len() on it right away
        return [address.user for address in SwapLeafEmailAddress.objects.filter(
            verified=True, email=email)]


class SwapLeafEmailAddress(models.Model):
    
    user = models.ForeignKey(User)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    primary = models.BooleanField(default=False)
    
    objects = SwapLeafEmailAddressManager()
    
    def set_as_primary(self, conditional=False):
        old_primary = SwapLeafEmailAddress.objects.get_primary(self.user)
        if old_primary:
            if conditional:
                return False
            old_primary.primary = False
            old_primary.save()
        self.primary = True
        self.save()
        self.user.email = self.email
        self.user.save()
        return True
    
    def __unicode__(self):
        return u"%s (%s)" % (self.email, self.user)
    
    class Meta:
        verbose_name = _("email address")
        verbose_name_plural = _("email addresses")
        unique_together = (
            ("user", "email"),
        )

class SwapLeafEmailConfirmation(models.Model):
    
    email_address = models.EmailField()
    sent = models.DateTimeField()
    confirmation_key = models.CharField(max_length=40,blank=True)
    
    def confirm_email(self, confirmation_key):
        try:
            email_confirmation = self.get(confirmation_key=confirmation_key)
        except self.model.DoesNotExist:
            return None
        if not email_confirmation.key_expired():
            #email_confirmation.verified = True
            email_confirmation.save()
            return email_address

    def send_confirmation(self):
        confirmation_key = self.confirmation_key
        activate_url = WEBSITE_HOMEPAGE + 'confirmation/' + confirmation_key
        context = {
            "activate_url": activate_url,
        }
        subject = "Welcome to SwapLeaf"
        html_content = render_to_string('text/email/emailconfirmation/email_confirmation_message.html',context)
        text_content = strip_tags(html_content)
        mail = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [self.email_address])
        mail.attach_alternative(html_content, "text/html")
        mail.send()
        #send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email_address])
        email_confirmation_sent.send(
            sender=self,
            confirmation=self,
        )

    def delete_expired_confirmations(self):
        for confirmation in self.all():
            if confirmation.key_expired():
                confirmation.delete()

    def key_expired(self):
        expiration_date = self.sent + datetime.timedelta(
            days=settings.EMAIL_CONFIRMATION_DAYS)
        return expiration_date <= datetime.datetime.now()
    key_expired.boolean = True
    
    def save(self, *args, **kwargs):
        salt = sha_constructor(str(random())).hexdigest()[:5]
        self.confirmation_key = sha_constructor(salt + self.email_address).hexdigest()
        super(SwapLeafEmailConfirmation, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"confirmation for %s" % self.email_address
    
    class Meta:
        verbose_name = _("email confirmation")
        verbose_name_plural = _("email confirmations")
