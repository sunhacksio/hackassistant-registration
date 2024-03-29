# HACKATHON PERSONALIZATION
import os

from django.utils import timezone

HACKATHON_NAME = 'sunhacks'
# What's the name for the application
HACKATHON_APPLICATION_NAME = 'sunhacks registration'
# Hackathon timezone
TIME_ZONE = 'MST'
# This description will be used on the html and sharing meta tags
HACKATHON_DESCRIPTION = 'sunhacks is a student-run hackathon at Arizona State University' \
                        'committed to growing the local tech community, providing students' \
                        'with brand new opportunities and connections, and contributing to a' \
                        'world-wide community: the hacker community. Our vision is to bring people of '\
                        'all backgrounds together to develop skills together as they learn, build, and code here at sunhacks.'
# Domain where application is deployed, can be set by env variable
HACKATHON_DOMAIN = os.environ.get('DOMAIN', 'localhost:8000')
# Hackathon contact email: where should all hackers contact you. It will also be used as a sender for all emails
HACKATHON_CONTACT_EMAIL = 'team@sunhacks.io'
# Hackathon logo url, will be used on all emails
HACKATHON_LOGO_URL = 'https://github.com/sun-hacks/website/blob/master/assets/small-yellow-sun.png?raw=true'

HACKATHON_OG_IMAGE = 'https://hackcu.org/img/hackcu_ogimage870x442.png'
# (OPTIONAL) Track visits on your website
# HACKATHON_GOOGLE_ANALYTICS = 'UA-7777777-2'
# (OPTIONAL) Hackathon twitter user
HACKATHON_TWITTER_ACCOUNT = 'sun_hacks'
# (OPTIONAL) Hackathon Facebook page
HACKATHON_FACEBOOK_PAGE = 'sunhacksofficial'
# (OPTIONAL) Github Repo for this project (so meta)
HACKATHON_GITHUB_REPO = 'https://github.com/hackassistant/registration/'

# (OPTIONAL) Applications deadline
HACKATHON_APP_DEADLINE = timezone.datetime(2019, 9, 18, 23, 59, tzinfo=timezone.pytz.timezone(TIME_ZONE))
# (OPTIONAL) When to arrive at the hackathon
HACKATHON_ARRIVE = 'Check in opens at 5:00 PM on Friday September 20th, ' \
                   'the opening ceremony will be at 7:00 pm.'

# (OPTIONAL) When to arrive at the hackathon
HACKATHON_LEAVE = 'Closing ceremony will be held on Sunday September 22nd and are expected to end by 12:15 PM. ' \
                  'However, the projects demo fair will be held in the morning starting at 9:00 AM.'
# (OPTIONAL) Hackathon live page
# HACKATHON_LIVE_PAGE = 'https://gerard.space/live'

# (OPTIONAL) Regex to automatically match organizers emails and set them as organizers when signing up
REGEX_HACKATHON_ORGANIZER_EMAIL = '^.*@sunhacks\.io$'

# (OPTIONAL) Sends 500 errors to email whilst in production mode.
HACKATHON_DEV_EMAILS = []

# Reimbursement configuration
REIMBURSEMENT_ENABLED = False
CURRENCY = '$'
REIMBURSEMENT_EXPIRY_DAYS = 5
REIMBURSEMENT_REQUIREMENTS = 'You have to submit a project and demo it during the event in order to be reimbursed.'
REIMBURSEMENT_DEADLINE = timezone.datetime(2018, 2, 24, 3, 14, tzinfo=timezone.pytz.timezone(TIME_ZONE))

# (OPTIONAL) Max team members. Defaults to 4
TEAMS_ENABLED = True
HACKATHON_MAX_TEAMMATES = 4

# (OPTIONAL) Code of conduct link
CODE_CONDUCT_LINK = "https://static.mlh.io/docs/mlh-code-of-conduct.pdf"

# (OPTIONAL) Slack credentials
# Highly recommended to create a separate user account to extract the token from
SLACK = {
    'team': os.environ.get('SL_TEAM', 'team'),
    # Get it here: https://api.slack.com/custom-integrations/legacy-tokens
    'token': os.environ.get('SL_TOKEN', "team")
}

# (OPTIONAL) Logged in cookie
# This allows to store an extra cookie in the browser to be shared with other application on the same domain
# LOGGED_IN_COOKIE_DOMAIN = '.gerard.space'
# LOGGED_IN_COOKIE_KEY = 'hackassistant_logged_in'

# Hardware configuration
HARDWARE_ENABLED = False
# Hardware request time length (in minutes)
HARDWARE_REQUEST_TIME = 15
# Can Hackers start a request on the hardware lab?
# HACKERS_CAN_REQUEST = False
