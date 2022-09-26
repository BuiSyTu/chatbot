from django.urls import re_path, path

from chat_bot.views import view_sentence, view_intent, view_entity, view_card, view_scenario
from chat_bot.views import view_keyword, view_step, view_ai, view_reply, view_home, view_user, view_dictionary, view_bot, view_variable, view_test

urlpatterns = [
    # home
    path('', view_sentence.sentences),
    # user
    re_path(r'^users/?$', view_user.users),
    re_path(r'^add_user/?$', view_user.add_user),
    path('users/<id>', view_user.user_detail),
    # bot
    re_path(r'^bots/?$', view_bot.bots),
    re_path(r'^add_bot/?$', view_bot.add_bot),
    path('bots/<id>', view_bot.bot_detail),
    # sentence
    re_path(r'^sentences/?$', view_sentence.sentences),
    re_path(r'^add_sentences/?$', view_sentence.add_sentences),
    path('sentences/<id>', view_sentence.sentence_detail),
    # intent
    re_path(r'^intents/?$', view_intent.intents),
    re_path(r'^add_intents/?$', view_intent.add_intents),
    path('intents/<id>', view_intent.intent_detail),
    # entity
    re_path(r'^entities/?$', view_entity.entity_types),
    re_path(r'^add_entities/?$', view_entity.add_entity_types),
    path('entities/<id>', view_entity.entity_type_detail),
    # key word
    re_path(r'^keywords/?$', view_keyword.key_words),
    re_path(r'^add_keywords/?$', view_keyword.add_key_words),
    path('keywords/<id>', view_keyword.key_word_detail),
    # dictionary
    re_path(r'^dictionaries/?$', view_dictionary.dictionaries),
    re_path(r'^add_dictionary/?$', view_dictionary.add_dictionary),
    path('dictionaries/<id>', view_dictionary.dictionary_detail),
    # step
    re_path(r'^steps/?$', view_step.steps),
    path('steps/<id>', view_step.step_detail),
    re_path(r'^add_steps/?$', view_step.add_steps),
    path('reply_steps/', view_step. reply_step),
    # training and test
    re_path(r'^training/?$', view_ai.training),
    re_path(r'^test_nlp/?$', view_ai.test_nlp),
    # reply
    path('reply/', view_reply.reply),
    # speech_to_text
    path('stt', view_ai.speech_to_text),
    # variable
    re_path(r'^variables/?$', view_variable.variables),
    re_path(r'^add_variable/?$', view_variable.add_variable),
    path('variables/<id>', view_variable.variable_detail),
    # test
    path('test/', view_test.test),
    #card
    re_path(r'^cards/?$', view_card.cards),
    re_path(r'^add_card/?$', view_card.add_cards),
    path('cards/<id>', view_card.card_detail),
    #scenario
    re_path(r'^scenarios/?$', view_scenario.scenarios),
    re_path(r'^add_scenario/?$', view_scenario.add_scenario),
    path('scenarios/<id>', view_scenario.scenario_detail),
]
