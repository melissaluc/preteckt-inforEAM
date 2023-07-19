import time
from datetime import datetime, date, timezone, timedelta
import pytz


def convertEpochtoDT(ts):
    dt_convert = datetime.fromtimestamp(ts)
    return dt_convert

def getEpochtoDT(ts):
    ts_convert = ts.strftime("%Y-%m-%dT%H:%M:%S")
    # YYYY-mm-ddTHH:MM:SS
    return ts_convert

def getLastN(ts, delta_dt=1, x='minutes'):
    """
    Returns ts epoch time
    x = days, minutes, hours, seconds
    """
    dt = convertEpochtoDT(ts)
    if x=="weeks":
        ts_convert = int((dt-timedelta(days=delta_dt)).timestamp())
    elif x=="days":
        ts_convert = int((dt-timedelta(days=delta_dt)).timestamp())
    elif x=="hours":
        ts_convert = int((dt-timedelta(hours=delta_dt)).timestamp())
    elif x=="minutes":
        ts_convert = int((dt-timedelta(minutes=delta_dt)).timestamp())
    elif x=="seconds":
        ts_convert = int((dt-timedelta(seconds=delta_dt)).timestamp())

    return ts_convert

def convertUTCtoLocal(utc_epoch):
    tz = pytz.timezone('America/Toronto')
    ts = utc_epoch.astimezone(tz)
    return ts

test_ts = getLastN(1686592114, delta_dt=1, x='days')
print(
    convertEpochtoDT(test_ts),convertEpochtoDT(1686592114)
)