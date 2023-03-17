from datetime import datetime, timedelta
from dateutil.rrule import rrule, HOURLY, SECONDLY
import random


def generate_hour(start, end):
    data = []
    seconds = [timestamp for timestamp in rrule(
        SECONDLY, dtstart=start, until=end
    )]
    for second in seconds:
        timestamp = second.strftime('%Y-%m-%dT%H:%M:%S')
        cpu = random.randint(9, 50)
        gpu = random.randint(35, 120)
        data.append({
            'timestamp': timestamp,
            'watts': {
                'gpu_watts': gpu,
                'cpu_watts': cpu
            }
        })
    return data


def generate(db):
    start = datetime(2023, 2, 14, 0)
    end = datetime(2023, 2, 20, 0)

    hours = [timestamp for timestamp in rrule(
        HOURLY, dtstart=start, until=end
    )]

    col = db['ecogamer']

    for hour in hours:
        start = hour - timedelta(hours=1)
        end = hour - timedelta(seconds=1)
        bucket = {
            'start_time': start.strftime('%Y-%m-%dT%H:%M:%S'),
            'end_time': end.strftime('%Y-%m-%dT%H:%M:%S')
        }
        bucket.update({'data': generate_hour(start, end)})
        col.insert_one(bucket)


if __name__ == "__main__":
    generate()
