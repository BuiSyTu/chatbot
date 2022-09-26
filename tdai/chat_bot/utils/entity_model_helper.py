from chat_bot.models import EntityModel
import pickle


def get_latest_model():
    entity_model_dumps = EntityModel.objects.order_by('created_time')
    entity_model_dump = entity_model_dumps[len(entity_model_dumps) - 1]
    return pickle.loads(entity_model_dump.data)
