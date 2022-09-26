import json
from django.core.serializers import serialize


def convert_json(model):
    return json.loads(serialize('json', model))