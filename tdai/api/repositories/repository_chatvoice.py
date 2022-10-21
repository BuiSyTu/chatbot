from chat_bot.models import ChatVoice

def add(text: str, link: str):
    try:
        ChatVoice.objects.create(
            text=text,
            link=link
        )
    except Exception as e:
        print(e)

def get_link_by_text(text: str):
    try:
        chat_voice = ChatVoice.objects.filter(text=text)
        return chat_voice[0].link
    except Exception as e:
        print(e)
        return None