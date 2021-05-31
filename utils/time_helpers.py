from datetime import datetime
import pytz


def utc_now():
    # return current time with UTC timezone aware info
    return datetime.now().replace(tzinfo=pytz.utc)
