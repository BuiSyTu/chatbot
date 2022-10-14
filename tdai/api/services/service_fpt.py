import json
import requests

from api.repositories import repository_chatvoice

def get_voice(payload):
    try:
        url = 'https://api.fpt.ai/hmi/tts/v5'

        headers = {
            'api-key': 'cnnvqSxKkxOHXwJvkff681tgU7O8Gi0B',
            'speed': '',
            'voice': 'banmai'
        }

        response = requests.request('POST', url, data=payload, headers=headers)
        if (response.status_code == 200):
            rs = json.loads(response.text)
            repository_chatvoice.add(text=payload, link=rs['async'])
            return rs
        return None
    except Exception as e:
        print(e)
        return None
    