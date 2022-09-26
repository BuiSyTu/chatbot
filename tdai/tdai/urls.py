from django.conf.urls import include, url

from api import urls as api_urls
from chat_bot import urls as chat_bot_urls

# from rest_framework_swagger.views import get_swagger_view
#
# schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    # api
    url(r'api/', include(api_urls)),
    # chat_bot
    url(r'', include(chat_bot_urls))
]
