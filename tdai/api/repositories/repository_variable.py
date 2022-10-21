from django.utils import timezone
from django.forms import model_to_dict

from chat_bot.models import RequireVariables, Variable

def get_all(request):
    _variables = Variable.objects.values()
    result = list(_variables.values())
    return result

def create(params):
    try:
        Variable.objects.create(
            name=params.get('name'),
            variable_type=params.get('variable_type'),
            created_time=timezone.now
        )

        return {
            'status': 201,
            'message': 'Thêm thành công'
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }

def get_by_id(id: int):
    try:
        _variable = Variable.objects.get(id=id)
        result = model_to_dict(_variable)

        return {
            'status': 200,
            'message': None,
            'result': result
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e),
            'result': None
        }

def update(id: int, params):
    try:
        variable = Variable.objects.get(id=id)
        variable.name = params.get('name')
        variable.variable_type = params.get('variable_type')        
        variable.updated_time = timezone.now()
        variable.save()
        return {
            'status': 204,
            'message': None
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }

def delete(id: int):
    try:
        variable = Variable.objects.get(id=id)
        variable.delete()
        return {
            'status': 204,
            'message': None
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }


def init_require_variables(step_id: int, list_variable_id: list):
    try:
        for variable_id in list_variable_id:
            RequireVariables.objects.create(
                step_id=step_id,
                variable_id=variable_id
            )
    except Exception as e:
        print(e)

def remove_require_variables(step_id: int, list_variable_id: list):
    try:
        for variable_id in list_variable_id:
            RequireVariables.objects.filter(step_id=step_id).filter(variable_id=variable_id).delete()
    except Exception as e:
        print(e)