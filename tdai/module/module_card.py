from chat_bot.models import HistoryUsedIntent, Card
from module import module_variables


# Kiểm tra intent dùng để tạo thẻ đã sử dụng hay chưa
def check_used_intent(request):
    message = "ok"

    if request['card_type'] != "intent":
        return True, message

    config = request['config']
    try:
        intent_id = int(config['intent_id'])
        history = list(HistoryUsedIntent.objects.filter(intent_id=intent_id).values())
        print(history)
        if len(history) > 0:
            message = "intent was used"
            return False, message
        else:
            HistoryUsedIntent.objects.create(
                step_id=request['step_id'],
                intent_id=intent_id
            )
            return True, message
    except Exception as e:
        print(e)
        message = "intent_id is empty"
        return True, message


# Lấy tất cả thẻ có step_id
# Thành công: Trả về thẻ sắp xếp theo position và status = True
# Thất bại: Trả về list rỗng và status = False
def get_all_cards(step_id):
    cards = list(Card.objects.filter(step_id=step_id).values())
    try:
        cards = sorted(cards, key=lambda k: k.get('position', 1000), reverse=False)
        return cards, True
    except Exception as e:
        print(e)
        return [], False


# Trả về vị trí bắt đầu và kết thúc của form_card
def get_to_formcard(arr, indexes, user_name, start=-1, entities=[]):
    end = len(arr)
    if len(indexes) == 0:
        return start, end
    for i in indexes:
        key, check = module_variables.check_variable_values(arr[i], user_name, entities=entities)
        if check:
            start = i + 1
        else:
            end = i + 1
            break
    return start, end


# Trả về các index có card_type = form trong tập card truyền vào
def find_indexof_formcards(cards, entities=[]):
    arr = []
    for i in range(len(cards)):
        if cards[i]['card_type'] == 'form':
            arr.append(i)
    return arr
