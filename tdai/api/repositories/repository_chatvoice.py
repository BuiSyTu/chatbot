from chat_bot.models import ChatVoice

def add(text, link):
    try:
        ChatVoice.objects.create(
            text=text,
            link=link
        )
    except Exception as e:
        print(e)

def get_link_by_text(text):
    try:
        chat_voice = ChatVoice.objects.filter(text=text)
        return chat_voice[0].link
    except Exception as e:
        print(e)
        return None