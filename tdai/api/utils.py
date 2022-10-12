import json
import pybars
from django.core.serializers import serialize


def convert_json(model):
    return json.loads(serialize('json', model))

def json_try_loads(text):
    try:
        value = json.loads(text)
        return (value, True)
    except Exception as e:
        print(e)
        return (None, False)

def handle_regex(source, dict):
    try:
        compiler = pybars.Compiler()
        template = compiler.compile(source)
        output = template(dict)
        if hasattr(output, "__len__") and len(output) > 2 and output[len(output) - 2] == ',':
            tmp = list(output)
            tmp[-2] = ''
            output = "".join(tmp)

        output = output.replace('&#123;', '{')
        output = output.replace('&#125;', '}')
        return output
    except Exception as e:
        print(e)
        return source