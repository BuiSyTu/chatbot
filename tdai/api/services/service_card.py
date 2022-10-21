from chat_bot.models import HistoryUsedIntent
from api.services import service_variable


# Trả về vị trí bắt đầu và kết thúc của form_card
def get_to_formcard(arr: list, indexes: list, user_name: str, start=-1, entities=[]):
    end = len(arr)
    if len(indexes) == 0:
        return start, end
    for i in indexes:
        key, check = service_variable.check_variable_values(arr[i], user_name, entities=entities)
        if check:
            start = i + 1
        else:
            end = i + 1
            break
    return start, end


# Trả về các index có card_type = form trong tập card truyền vào
def find_indexes_formcard(cards: list):
    arr = []
    for i in range(len(cards)):
        if cards[i]['card_type'] == 'form':
            arr.append(i)
    return arr
