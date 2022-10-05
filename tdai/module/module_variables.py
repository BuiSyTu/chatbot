import json
import random
import re

from chat_bot.models import HistoryChat, Variable, RequireVariables


# Lưu thông tin các biến yêu cầu trong 1 bước
def init_require_variables(step_id, variable_ids):
    try:
        for variable_id in variable_ids:
            # Lưu lại vào HistoryChat
            RequireVariables.objects.create(
                step_id=step_id,
                variable_id=variable_id
            )
        return True
    except Exception as e:
        print(e)
        return False

def remove_require_variables(step_id, variable_ids):
    try:
        for variable_id in variable_ids:
            RequireVariables.objects.filter(step_id=step_id).filter(variable_id=variable_id).delete()
        return True
    except Exception as e:
        print(e)
        return False


def init_history_variables(step_id, user_name):
    user_variables = HistoryChat.objects.filter(step_id=step_id).filter(user_name=user_name)
    user_variables_id = list(user_variables.values('variable_id'))
    # khi user_name chưa sử dụng biến
    require_variables = RequireVariables.objects.filter(step_id=step_id)
    require_variables_id = list(require_variables.values('variable_id'))
    for require_variable_id in require_variables_id:
        status = True
        for user_variable_id in user_variables_id:
            if user_variable_id['variable_id'] == require_variable_id['variable_id']:
                status = False
        if status:
            try:
                HistoryChat.objects.create(
                    step_id=step_id,
                    user_name=user_name,
                    variable_id=require_variable_id['variable_id'],
                    value=""
                )
            except Exception as e:
                print(e)
                return False
    return True


# Cập nhật lại giá trị variable cho step
def update_variables(step_id, variable_name, value, user_name):
    user_variables = HistoryChat.objects.filter(step_id=step_id).filter(user_name=user_name)
    variable = list(Variable.objects.filter(name= variable_name).values())[0]
    variable_id = variable['id']
    for user_variable in user_variables:
        if user_variable.variable_id == variable_id:
            try:
                user_variable.value = value
                user_variable.save()
            except Exception as e:
                print(e)
                return False
    return True


def reset_variables(variable_names, user_name):
    variable_ids = []
    histories = HistoryChat.objects.filter(user_name=user_name)
    if len(variable_names) == 1 and variable_names[0] == '*':
        for history in histories:
            history.value = ''
            history.save()
    else:
        for variable_name in variable_names:
            _variables = Variable.objects.filter(name=variable_name)
            for _variable in _variables:
                variable_ids.append(_variable.id)
        for history in histories:
            for variable_id in variable_ids:
                if variable_id == history.variable_id:
                    history.value =''
            history.save()


def validate_variables(sentence, variable_name):
    variables = list(Variable.objects.filter(name = variable_name).values())

    if (len(variables) > 0):
        variable = variables[0]
        return check_variable_type(sentence, variable['variable_type'])
    return True


def check_variable_values(cards, user_name, entities=[]):
    step_id = cards.get('step_id')

    for entity in entities:
        HistoryChat.objects.filter(user_name=user_name).filter(step_id=step_id).filter(variable__name=entity['entity']).update(value=entity['keyword'])
        

    if cards['card_type'] == 'form':
        config = cards.get('config')
        js_config = json.loads(config)
        questions = js_config.get('questions')

        variables_id = []
        variables_name = []

        for question in questions:
            variables_id.append(question['variable_id'])
            variables_name.append(question['variable_name'])
        
        histories = HistoryChat.objects.filter(user_name=user_name).filter(step_id= step_id)
        for history in histories:
            for index in range(len(variables_id)):
                if history.variable.id == variables_id[index]:
                    if history.value == '':
                        return variables_name[index], False
    return "", True


def get_value_by_variablename(step_id,user_name,variable_name):
    variable = list(Variable.objects.filter(name=variable_name).values())[0]
    variable_id = variable['id']
    histories =  HistoryChat.objects.filter(user_name=user_name).filter(step_id= step_id)
    for history in histories:
        if history.variable_id == variable_id:
            return history.value,True
    return "",False


def check_variable_type(answer: str, variable_type: str):
    if variable_type == 'Number':
        return True if answer.isnumeric() else False
    elif variable_type == 'String':
        return True
    elif variable_type == 'Email':
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        return True if re.search(regex, answer) else False
    elif variable_type == 'Phone':
        # FIXME: find a regex for phone number
        return True if answer.isnumeric() and len(answer) == 10 else False

