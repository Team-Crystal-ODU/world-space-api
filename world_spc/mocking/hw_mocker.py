from datetime import datetime, timedelta
from dateutil.rrule import rrule, HOURLY, SECONDLY
import random
import pytz


def generate_hour(start, end):
    data = []
    gaming = random.randint(0, 1)
    est = pytz.timezone('US/Eastern')
    seconds = [timestamp for timestamp in rrule(
        SECONDLY, dtstart=start, until=end
    )]
    count = 0
    sum = 0
    for i, second in enumerate(seconds):
        # timestamp = second.strftime('%Y-%m-%dT%H:%M:%S')
        if i % 5 == 0:
            if gaming == 1:
                cpu = random.randint(75, 120)
                gpu = random.randint(195, 320)
            else:
                cpu = random.randint(10, 75)
                gpu = random.randint(30, 80)
            count += 1
            sum += (cpu + gpu)
            data.append({
                'timestamp': est.localize(second),
                'watts': {
                    'gpu_watts': gpu,
                    'cpu_watts': cpu
                }
            })
    return data, count, sum


def generate(db):
    est = pytz.timezone('US/Eastern')
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
            'start_time': est.localize(start),
            'end_time': est.localize(end)
        }
        data, count, sum = generate_hour(start, end)
        bucket.update({'samples': data, 'sample_count': count, 'total': sum})
        col.insert_one(bucket)


if __name__ == "__main__":
    generate()
