import random
import string

from .models import URLMap


def get_unique_short_id():
    short_link = ''.join(random.choices(
        string.ascii_letters + string.digits, k=6)
    )
    if URLMap.query.filter_by(short=short_link).first():
        short_link = get_unique_short_id()
    return short_link
