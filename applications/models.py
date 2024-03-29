from __future__ import unicode_literals

import json
import uuid as uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, EmailValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone

from app import utils
from user.models import User

from applications.validators import FileValidator


APP_PENDING = 'P'
APP_REJECTED = 'R'
APP_INVITED = 'I'
APP_LAST_REMIDER = 'LR'
APP_CONFIRMED = 'C'
APP_CANCELLED = 'X'
APP_ATTENDED = 'A'
APP_EXPIRED = 'E'
APP_DEADLINE_REMINDER = 'D'

STATUS = [
    (APP_PENDING, 'Under review'),
    (APP_REJECTED, 'Wait listed'),
    (APP_INVITED, 'Invited'),
    (APP_LAST_REMIDER, 'Last reminder'),
    (APP_CONFIRMED, 'Confirmed'),
    (APP_CANCELLED, 'Cancelled'),
    (APP_ATTENDED, 'Attended'),
    (APP_EXPIRED, 'Expired'),
    (APP_DEADLINE_REMINDER, 'Last reminder (deadline)'),
]

NO_ANSWER = 'NA'
MALE = 'M'
FEMALE = 'F'
NON_BINARY = 'NB'
GENDER_OTHER = 'X'

GENDERS = [
    (NO_ANSWER, 'Prefer not to answer'),
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (NON_BINARY, 'Non-binary'),
    (GENDER_OTHER, 'Prefer to self-describe'),
]

INDIAN = "IN"
ASIAN = "AS"
BLACK = "BK"
HISPANIC = "HS"
WHITE = "WH"
E_NO_ANSWER = "NA"
E_OTHER = "X"

ETHNICITIES = [
    (INDIAN, "American Indian or Alaskan Native"),
    (ASIAN, "Asian/Pacific Islander"),
    (BLACK, "Black or African American"),
    (HISPANIC, "Hispanic"),
    (WHITE, "White/Caucasian"),
    (E_OTHER, "Multiple Ethnicity/Other (Please Specify)"),
    (E_NO_ANSWER, "Prefer not to answer"),
]

HIGHSCHOOL = "HS"
UNDERGRAD = "UG"
GRAD = "GR"

STUDY_LEVEL = [
    (HIGHSCHOOL, "High School"),
    (UNDERGRAD, "Undergraduate"),
    (GRAD, "Graduate"),
]

D_NONE = 'None'
D_VEGETERIAN = 'Vegeterian'
D_VEGAN = 'Vegan'
D_NO_PORK = 'No pork'
D_GLUTEN_FREE = 'Gluten-free'
D_OTHER = 'Other'

DIETS = [
    (D_NONE, 'No requirements'),
    (D_VEGETERIAN, 'Vegeterian'),
    (D_VEGAN, 'Vegan'),
    # (D_NO_PORK, 'No pork'),
    (D_GLUTEN_FREE, 'Gluten-free'),
    (D_OTHER, 'Other')
]


W_XXS = 'W-XSS'
W_XS = 'W-XS'
W_S = 'W-S'
W_M = 'W-M'
W_L = 'W-L'
W_XL = 'W-XL'
W_XXL = 'W-XXL'
T_XXS = 'XXS'
T_XS = 'XS'
T_S = 'S'
T_M = 'M'
T_L = 'L'
T_XL = 'XL'
T_XXL = 'XXL'
TSHIRT_SIZES = [
    # (W_XXS, "Women's - XXS"),
    (W_XS, "Women's - XS"),
    (W_S, "Women's - S"),
    (W_M, "Women's - M"),
    (W_L, "Women's - L"),
    (W_XL, "Women's - XL"),
    (W_XXL, "Women's - XXL"),
    # (T_XXS, "Unisex - XXS"),
    (T_XS, "Unisex - XS"),
    (T_S, "Unisex - S"),
    (T_M, "Unisex - M"),
    (T_L, "Unisex - L"),
    (T_XL, "Unisex - XL"),
    (T_XXL, "Unisex - XXL"),
]
DEFAULT_TSHIRT_SIZE = T_M

YEARS = [(int(size), size) for size in ('2019 2020 2021 2022 2023'.split(' '))] + [(2024, "2024 or later")]
DEFAULT_YEAR = 2018


class Application(models.Model):
    # META
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, primary_key=True)
    invited_by = models.ForeignKey(User, related_name='invited_applications', blank=True, null=True)

    # When was the application submitted
    submission_date = models.DateTimeField(default=timezone.now)
    # When was the last status update
    status_update_date = models.DateTimeField(blank=True, null=True)
    # Application status
    status = models.CharField(choices=STATUS, default=APP_PENDING,
                              max_length=2)

    sent_info = models.BooleanField(blank=True, default=False)

    # ABOUT YOU
    # Population analysis, optional
    gender = models.CharField(max_length=23, choices=GENDERS, default=NO_ANSWER)
    other_gender = models.CharField(max_length=50, blank=True, null=True)

    ethnicity = models.CharField(max_length=23, choices=ETHNICITIES, default=E_NO_ANSWER)
    other_ethnicity = models.CharField(max_length=50, blank=True, null=True)

    education = models.CharField(max_length=23, choices=STUDY_LEVEL, default=UNDERGRAD)

    # Personal data (asking here because we don't want to ask birthday)
    under_age = models.BooleanField()
    data_consent = models.BooleanField(default=False)
    sponsor_consent = models.BooleanField(default=False)

    phone_number = models.CharField(blank=True, null=True, max_length=16,
                                    validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                                               message="Phone number must be entered in the format: \
                                                                  '+#########'. Up to 15 digits allowed.")])

    # Where is this person coming from?
    origin = models.CharField(max_length=300)
    # Who invited them?
    referral = models.CharField(blank=True, null=True, max_length=320,
                                validators=[EmailValidator(message="Enter a valid email address for referral")])
    referred = models.BooleanField(blank=True, default=False)

    # Is this your first hackathon?
    first_timer = models.BooleanField()
    # Why do you want to come to X?
    description = models.TextField(max_length=1500)
    # Explain a little bit what projects have you done lately
    projects = models.TextField(max_length=1500, null=True)

    # Reimbursement
    reimb = models.BooleanField(default=False)
    reimb_amount = models.FloatField(blank=True, null=True, validators=[
        MinValueValidator(0, "Negative? Really? Please put a positive value")])

    # Random lenny face
    lennyface = models.CharField(max_length=300, blank=True, null=True)

    # Giv me a resume here!
    resume = models.FileField(upload_to='resumes', null=True, blank=True,
        validators=[FileValidator(max_size=settings.MAX_UPLOAD_SIZE,
            content_types=['application/pdf'])])

    # University
    graduation_year = models.IntegerField(choices=YEARS, default=DEFAULT_YEAR)
    university = models.CharField(max_length=300)
    degree = models.CharField(max_length=300)

    # URLs
    github = models.URLField(blank=True, null=True)
    devpost = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    site = models.URLField(blank=True, null=True)

    # Info for swag and food
    diet = models.CharField(max_length=300, choices=DIETS, default=D_NONE)
    other_diet = models.CharField(max_length=600, blank=True, null=True)
    tshirt_size = models.CharField(max_length=5, default=DEFAULT_TSHIRT_SIZE, choices=TSHIRT_SIZES)

    @classmethod
    def annotate_vote(cls, qs):
        return qs.annotate(vote_avg=Avg('vote__calculated_vote'))

    @property
    def uuid_str(self):
        return str(self.uuid)

    def get_soft_status_display(self):
        text = self.get_status_display()
        if "Not" in text or 'Rejected' in text:
            return "Pending"
        return text

    def __str__(self):
        return self.user.email

    def save(self, **kwargs):
        self.status_update_date = timezone.now()
        super(Application, self).save(**kwargs)

    def save_no_update(self, **kwargs):
        super(Application,self).save(**kwargs)

    def invite(self, user):
        # We can re-invite someone invited
        if self.status in [APP_CONFIRMED, APP_ATTENDED]:
            raise ValidationError('Application has already answered invite. '
                                  'Current status: %s' % self.status)
        self.status = APP_INVITED
        if not self.invited_by:
            self.invited_by = user
        self.last_invite = timezone.now()
        self.last_reminder = None
        self.status_update_date = timezone.now()
        self.save()

    def last_reminder(self):
        if self.status != APP_INVITED:
            raise ValidationError('Reminder can\'t be sent to non-pending '
                                  'applications')
        self.status_update_date = timezone.now()
        self.status = APP_LAST_REMIDER
        self.save()

    def deadline_reminder(self):
        if self.status != APP_INVITED:
            raise ValidationError('Reminder can\'t be sent to non-pending '
                                  'applications')
        self.status_update_date = timezone.now()
        self.status = APP_DEADLINE_REMINDER
        self.save()

    def expire(self):
        self.status_update_date = timezone.now()
        self.status = APP_EXPIRED
        self.save()

    def reject(self, request):
        if self.status == APP_ATTENDED:
            raise ValidationError('Application has already attended. '
                                  'Current status: %s' % self.status)
        self.status = APP_REJECTED
        self.status_update_date = timezone.now()
        self.save()

    def wait_list(self, request):
        if self.status == APP_ATTENDED:
            raise ValidationError('Application has already attended. '
                                  'Current status: %s' % self.status)
        self.status = APP_REJECTED
        self.status_update_date = timezone.now()
        self.save()

    def confirm(self):
        if self.status == APP_CANCELLED:
            raise ValidationError('This invite has been cancelled.')
        elif self.status == APP_EXPIRED:
            raise ValidationError('Unfortunately your invite has expired.')
        elif self.status in [APP_INVITED, APP_LAST_REMIDER, APP_DEADLINE_REMINDER]:
            self.status = APP_CONFIRMED
            self.status_update_date = timezone.now()
            self.save()
        elif self.status in [APP_CONFIRMED, APP_ATTENDED]:
            return None
        else:
            raise ValidationError('Unfortunately his application hasn\'t been '
                                  'invited [yet]')

    def cancel(self):
        if not self.can_be_cancelled():
            raise ValidationError('Application can\'t be cancelled. Current '
                                  'status: %s' % self.status)
        if self.status != APP_CANCELLED:
            self.status = APP_CANCELLED
            self.status_update_date = timezone.now()
            self.save()
            reimb = getattr(self.user, 'reimbursement', None)
            if reimb:
                reimb.delete()

    def check_in(self):
        self.status = APP_ATTENDED
        self.status_update_date = timezone.now()
        self.save()

    def is_confirmed(self):
        return self.status == APP_CONFIRMED

    def is_cancelled(self):
        return self.status == APP_CANCELLED

    def answered_invite(self):
        return self.status in [APP_CONFIRMED, APP_CANCELLED, APP_ATTENDED]

    def needs_action(self):
        return self.status == APP_INVITED

    def is_pending(self):
        return self.status == APP_PENDING

    def can_be_edit(self):
        return self.can_be_post_edit() or (
            self.status == APP_PENDING and not self.vote_set.exists() and not utils.is_app_closed()
        )

    def can_be_post_edit(self):
        return self.can_be_cancelled() or self.is_attended()

    def is_invited(self):
        return self.status == APP_INVITED

    def is_expired(self):
        return self.status == APP_EXPIRED

    def is_rejected(self):
        return self.status == APP_REJECTED

    def is_attended(self):
        return self.status == APP_ATTENDED

    def is_last_reminder(self):
        return self.status == APP_LAST_REMIDER or self.status == APP_DEADLINE_REMINDER

    def can_be_cancelled(self):
        return self.status == APP_CONFIRMED or self.status == APP_INVITED or self.status == APP_LAST_REMIDER or self.status == APP_DEADLINE_REMINDER

    def can_confirm(self):
        return self.status in [APP_INVITED, APP_LAST_REMIDER, APP_DEADLINE_REMINDER]

    def set_referred(self,val):
        self.referred = val
        self.save_no_update()

    def send_info(self):
        self.sent_info = True
        self.save_no_update()


class DraftApplication(models.Model):
    content = models.CharField(max_length=7000)
    user = models.OneToOneField(User, primary_key=True)

    def save_dict(self, d):
        self.content = json.dumps(d)

    def get_dict(self):
        return json.loads(self.content)
