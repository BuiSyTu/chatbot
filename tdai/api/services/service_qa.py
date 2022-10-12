import json

import numpy as np
import requests
from chat_bot.utils import intent_model_helper
from tandan_nlp.classification import prediction as clf_prediction
from tandan_nlp.ner import prediction_bert as ner_prediction
from api.repositories import repository_card
from api.utils import handle_regex, json_try_loads
from api.services import service_card, service_variable


def get_answer_cards(step_id, user_name, start_position=0, entities=[]):
    cards = repository_card.get_by_step_id(step_id)

    indexes = service_card.find_indexes_formcard(cards)

    start, end = service_card.get_to_formcard(cards, indexes, user_name, start_position, entities)
    return cards[start:end]


# Hàm trả lại giá trị cho client
def get_answer(cards, step_id, user_name, entities = []):
    arr = []

    if len(cards) == 0:
        return {'answer': arr}

    for card in cards:
        if card['card_type'] == 'text':
            config = json.loads(card['config'].replace('\'', '\"'))  # Lấy config
            answer = handle_text(config=config, step_id=step_id, user_name=user_name, entities=entities)
            arr.append(answer)
        elif card['card_type'] == "reset":
            variables = json.loads(card['config'].replace('\'', '"'))['variables']
            service_variable.reset_variables(variables, user_name)
        elif card['card_type'] == 'api':
            config = json.loads(card['config'].replace('\'', '"'))
            res = handle_api(config=config, entities=entities)
            arr.append(res)
        elif card['card_type'] == 'form':
            res = handle_card_form(card=card, user_name=user_name, entities=entities)
            arr.append(res)
    return {'step_id': step_id, 'answers': arr}


def get_requestion(card, user_name, entities):
    arr = []
    step_id = card['step_id']
    if card['card_type'] == 'form':
        key, check = service_variable.check_variable_values(card, user_name, entities)
        if not check:
            config = json.loads(card['config'])
            questions = config['questions']
            for i in range(len(questions)):
                if key == questions[i]['variable_name']:
                    new_config = {
                        'card_type': 'text',
                        'text': questions[i]['re_question'],
                        'buttons': []
                    }
                    arr.append(new_config)
    return {'step_id': step_id, 'answer': arr}

def handle_card_form(card, user_name, entities):
    arr = []
    key, check = service_variable.check_variable_values(card, user_name, entities)
    # Nếu mà các biến chưa đủ giá trị
    if not check:
        config = json.loads(card['config'])
        questions = config['questions']
        for i in range(len(questions)):
            if key == questions[i]['variable_name']:
                # arr.append(questions[i]['question'])
                new_config = {
                    'card_type': 'form',
                    'text': questions[i]['question'],
                    'buttons': []
                }
                arr.append(new_config)
    return arr

def handle_api(config, entities):
    __urls = config.get('url')
    __method = config.get('method').upper()
    __headers = config.get('headers')
    __body = config.get('body')
    __answer = config.get('source')
    __button = config.get('buttons')

    __dict = {}
    js_res = None

    # FIXME: Change hard code entities
    for entity in entities:
        __dict[entity['entity']] =  entity['keyword']

    body_str = json.dumps(__body)
    body_str = handle_regex(body_str, __dict)
    __body = json.loads(body_str)

    headers_str = json.dumps(__headers)
    headers_str = handle_regex(headers_str, __dict)
    __headers = json.loads(headers_str)

    if __method.lower() == 'get':
        res = requests.request('GET', url=__urls, headers=__headers)

        if (res.status_code == 200):
            (js_res, status) = json_try_loads(res.text)
            if status == False or (js_res.get('error').get('code') != 200):
                return get_api_error_answer()
        else:
            return get_api_error_answer()

    if __method.lower() == 'post':
        res = requests.request('POST', url=__urls, headers=__headers, data=json.dumps(__body))
        if (res.status_code == 200):
            (js_res, status) = json_try_loads(res.text)
            if status == False or (js_res.get('error').get('code') != 200):
                return get_api_error_answer()
        else:
            return get_api_error_answer()

    if js_res != None:
        __answer = handle_regex(__answer, js_res)
        button_str = json.dumps(__button) if type(__button) is list else __button
        button_str = handle_regex(button_str, js_res)
        __button = json.loads(button_str)

    __dict = {}
    for entity in entities:
        __dict[entity['entity']] =  entity['keyword']
    __answer = handle_regex(__answer, __dict)
    
    return {
        "card_type": "text",
        "text": __answer,
        "buttons": __button
    }

def handle_text(config, step_id, user_name, entities):
    __source = config.get('source')
    __variables = config.get('variables')
    __button = config.get('buttons', [])
    __dict = {}

    # FIXME: Change hard code entities
    for entity in entities:
        __dict[entity['entity']] =  entity['keyword']

    if __variables is not None:
        for variable in __variables:
            value, status = service_variable.get_value_by_variablename(step_id, user_name, variable)
            __dict[variable] = value
    
    txt = handle_regex(__source, __dict)
    button_str = json.dumps(__button)
    button_str = handle_regex(button_str, __dict)
    __button = json.loads(button_str)

    return {
        'card_type': 'text',
        'text': txt,
        'buttons': __button
    }

def classification_text(text):
    thres_scores = 0.05
    intent_model = intent_model_helper.get_latest_model()
    intents = intent_model.classes_
    scores_int = clf_prediction.predict_proba_intent(text, intent_model)
    max_scores_int = np.max(scores_int)

    if max_scores_int > thres_scores:
        intent = intents[np.argmax(scores_int)]
    else:
        return None
    return intent

def predict_entity(sentence):
    rs_entity = ner_prediction.predict_entity(sentence)
    return rs_entity

def get_api_error_answer():
    return {
        "card_type": "text",
        "text": "Không tìm thấy kết quả phù hợp, vui lòng thử lại sau.",
        "buttons": []
    }
