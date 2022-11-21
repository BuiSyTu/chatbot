from chat_bot.models import IntentModel
import pickle


def get_latest_model():
    intent_model_dumps = IntentModel.objects.order_by('created_time')
    intent_model_dump = intent_model_dumps[len(intent_model_dumps) - 1]
    return pickle.loads(intent_model_dump.data)

def get_lastest_model_by_bot_id(bot_id):
    intent_model_dumps = IntentModel.objects.filter(bot_id=bot_id).order_by('created_time')
    intent_model_dump = intent_model_dumps[len(intent_model_dumps) - 1]
    return pickle.loads(intent_model_dump.data)