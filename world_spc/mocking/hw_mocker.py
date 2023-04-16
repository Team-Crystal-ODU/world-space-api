from datetime import datetime, timedelta
from dateutil.rrule import rrule, HOURLY, SECONDLY
import random
import pytz


def generate_hour(start, end):
    data = []
    cpu_variance = random.uniform(0.3, 1)
    gpu_variance = random.uniform(0.3, 1)
    x = [0, 1]
    gaming = random.choice(x)
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
                cpu = random.randint(75, 120) * cpu_variance
                gpu = random.randint(195, 320) * gpu_variance
            else:
                cpu = random.randint(10, 75) * cpu_variance
                gpu = random.randint(30, 80) * gpu_variance
            count += 1
            sum += (int(cpu) + int(gpu))
            data.append({
                'timestamp': est.localize(second),
                'watts': {
                    'gpu_watts': int(gpu),
                    'cpu_watts': int(cpu)
                }
            })
    return data, count, sum


def generate(db):
    est = pytz.timezone('US/Eastern')
    start = datetime(2023, 4, 1, 0)
    end = datetime(2023, 4, 25, 0)

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
        bucket.update(
            {'samples': data, 'sample_count': count, 'total': sum})
        col.insert_one(bucket)


if __name__ == "__main__":
    generate()
