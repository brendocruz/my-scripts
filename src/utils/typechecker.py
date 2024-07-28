import re
from datetime import datetime, timedelta


def parse_time(timestamp: str) -> timedelta:
    time: datetime
    if re.compile('^\\d+$').match(timestamp):
        time = datetime.strptime(timestamp, '%S')
    elif re.compile('^\\d+:\\d+$').match(timestamp):
        time = datetime.strptime(timestamp, '%M:%S')
    elif re.compile('^\\d+:\\d+:\\d+$').match(timestamp):
        time = datetime.strptime(timestamp, '%H:%M:%S')
    else:
        raise ValueError('Invalid timestamp.')


    delta = timedelta(hours=time.hour, 
                      minutes=time.minute, 
                      seconds=time.second)
    return delta
