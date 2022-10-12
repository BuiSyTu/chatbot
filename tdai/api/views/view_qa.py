import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Intent, Card
from api.services import service_variable, service_qa


@csrf_exempt
def QA(request):
    if request.method == "POST":
        params = json.loads(request.body)
        text = params.get('sentence')
        step_id = params.get('step_id')
        user_name = params.get('user_name')
        answer = []

        entities = service_qa.predict_entity(text)

        if not step_id:
            # Lấy ý định
            intent_name = service_qa.classification_text(text)
            if intent_name == None:
                return JsonResponse({'answers': []}, safe=False)
            intent = list(Intent.objects.filter(intent=intent_name).values())[0]
            intent_id = intent['id']
            # Lấy bước có ý định intennt_id
            cards = list(Card.objects.all().values().filter(card_type='intent'))
            for card in cards:
                config = json.loads(card['config'])
                if config.get('intent_id') == intent_id:
                    step_id = card['step_id']
            # Trường hợp không có bước nào xử lý intent đó
            if not step_id:
                answers = []
                default_answer = {
                    'card_type': 'text',
                    'text': 'Xin lỗi, mời bạn nhập lại câu hỏi',
                    'buttons': []
                }
                answers.append(default_answer)
                return JsonResponse({'answers': answers}, safe=False)
            status = service_variable.init_history_variables(step_id, user_name)
            if status:
                answer_cards = service_qa.get_answer_cards(step_id, user_name, entities=entities)

                answer = service_qa.get_answer(answer_cards, step_id, user_name, entities)
        else:
            answer_cards = service_qa.get_answer_cards(step_id, user_name, entities=entities)[-1]  # form_card
            lent = len(service_qa.get_answer_cards(step_id, user_name, entities=entities)) - 1
            text = params.get('sentence')
            key, check = service_variable.check_variable_values(answer_cards, user_name)
            if service_variable.validate_variables(text, key):
                # Nếu chưa lấy câu yêu cầu nhập biến
                if not check:
                    update_status = service_variable.update_variables(step_id, key, text, user_name)
                    if update_status:
                        key1, check1 = service_variable.check_variable_values(answer_cards, user_name)
                        if check1:
                            answer_cards = service_qa.get_answer_cards(step_id, user_name, entities=entities)
                            answer = service_qa.get_answer(answer_cards, step_id, user_name, entities)
                        else:
                            answer = service_qa.get_answer([answer_cards], step_id, user_name, entities)
                else:
                    answer_cards = service_qa.get_answer_cards(step_id, user_name, lent, entities=entities)
                    answer = service_qa.get_answer(answer_cards, step_id, user_name, entities)
            else:
                answer = service_qa.get_requestion(answer_cards, user_name)
        return JsonResponse(answer, safe=False)

@csrf_exempt
def test_api(request):
    if (request.method == 'GET'):
        url = 'https://apigateway.thanhhoa.gov.vn/chatbotdvc/SearchDocByKey'

        headers = {
            'Authorization': 'Bearer 1fb94be5-8b97-3fc0-9324-8257d9074a51'
        }

        body = {
            'key': '000.00.14.H56-200203-0118'
        }

        rs = requests.post(url=url, headers=headers, body=body)

        print(rs)
