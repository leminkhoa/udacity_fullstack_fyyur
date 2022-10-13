import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from wtforms.validators import ValidationError

def facebook_link_validator(form, field):
    pattern=r"(?:https?:\/\/)?(?:www\.)?facebook\.com\/(?:(?:\w)*#!\/)?"
    "(?:pages\/)?(?:[\w\-]*\/)*?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?(?:[\w\-\.]*)?"
    if not re.match(pattern, field.data):
        raise ValidationError('Please enter a valid Facebook link')


def start_time_validator(form, field):
    start_time = field.data
    if start_time < datetime.today() - relativedelta(years=2):
        raise ValidationError('Start time is too far from current time.')

