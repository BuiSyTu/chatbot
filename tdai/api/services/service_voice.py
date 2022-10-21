from api.repositories import repository_chatvoice
from api.services import service_fpt

def get_voice(text: str):
    link_by_db = repository_chatvoice.get_link_by_text(text=text)

    if link_by_db != None:
        return {
            'async': link_by_db,
            'error': 0,
            'message': 'The content will be returned after a few seconds under the async link.'
        }
    else:
        rs_fpt = service_fpt.get_voice(text)
        return rs_fpt

