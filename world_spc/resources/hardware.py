from flask_restful import Resource

from flask import request, abort
from marshmallow import Schema, fields

from world_spc.extensions import mongo
from world_spc.mocking import hw_mocker

from datetime import datetime, timedelta


class HardwareUpdateSchema(Schema):
    mock = fields.Str(required=False)


class HardwareSampleSchema(Schema):
    timestamp = fields.DateTime(required=True)
    watts = fields.Dict(
        gpu_watts=fields.Int(required=False),
        cpu_watts=fields.Int(required=False)
    )


q_str_schema = HardwareUpdateSchema()
payload_schema = HardwareSampleSchema()


def get_start_and_end_times(timestamp: datetime):
    """
    Get the corresponding start and end timestamps for a given sample based on
    the supplied timestamp. A one-hour bucket starts at minute:second 00:00 and
    ends at minute:second 59:59.
    Args: timestamp (datetime)
    Returns: start time (datetime), end time (datetime)
    """
    # TODO put datetime obj in correct timezone here
    offset = timedelta(hours=4)
    start = datetime(timestamp.year, timestamp.month,
                     timestamp.day, timestamp.hour)
    start += offset
    end = start + timedelta(minutes=59, seconds=59)
    # convert EDT to UTC
    return start, end


def update_db(body):
    start, end = get_start_and_end_times(body['timestamp'])
    offset = timedelta(hours=4)
    body.update({'timestamp': body['timestamp'] + offset})
    user = 'ecogamer'
    col = mongo.db[user]
    q = col.count_documents({"start_time": start})
    if q != 0:
        id = col.find_one({"start_time": start})['_id']
        count = col.find_one({"_id": id})['sample_count']
        count += 1
        total = col.find_one({"_id": id})['total']
        total = total + body['watts']['gpu_watts'] + body['watts']['cpu_watts']

        col.update_one(
            {'_id': id},
            {'$push': {'samples': body}},
        )
        col.update_one(
            {'_id': id},
            {'$set': {'sample_count': count}},
        )
        col.update_one(
            {'_id': id},
            {'$set': {'total': total}},
        )
        return True
    else:
        # insert a new doc with start and end times
        # init sample count to 1
        # init sum to gpu_watts + cpu_watts
        pass


class Hardware(Resource):
    """
    Routes requests submitted to the API for storing CPU and
    GPU wattage samples collected by the World Space hardware
    monitoring daemon.
    """

    def post(self):
        errors = q_str_schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        # TODO Check if user is in a list of users
        # Possibly use a simple decorator for this
        response = ''
        if request.args['mock'] is True:
            hw_mocker.generate(mongo.db)
        else:
            body = request.get_json(force=True)
            timestamp = datetime.strptime(
                body['timestamp'], '%Y-%m-%dT%H:%M:%S')
            errors = payload_schema.validate(body)
            if errors:
                abort(400, str(errors))
            else:
                body.update({'timestamp': timestamp})
                update_db(body)

        return response
