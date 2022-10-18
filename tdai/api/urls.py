from django.urls import path

from api.views import view_ai, view_entity, view_intent, view_keyword, view_reply, view_step, view_sentence, view_bot, view_user, view_dictionary, view_qa, view_scenario, view_variable, view_card,view_qa
from api.views import view_historychat,view_requirevariables
from api.views import view_testcallapi, view_voice, view_common
urlpatterns = [
    # common
    path('common/current_date', view_common.get_current_date),
    # fpt
    path('t2s',view_voice.text_to_speed),
    # test call api
    path('test_callapi',view_testcallapi.testAPI),
    # require variable
    path('revariables', view_requirevariables.requirevariables),
    path('revariables/<id>', view_requirevariables.requirevariables_detail),
    #history chat
    path('history', view_historychat.historychat),
    path('history/<id>', view_historychat.historychat_detail),
    #Qna
    path('qa',view_qa.QA),
    # user
    path('users/login', view_user.login),
    path('users', view_user.users),
    path('users/<id>', view_user.user_detail),
    # bot
    path('bots', view_bot.bots),
    path('bots/choose/<id>', view_bot.bot_choose),
    path('bots/<id>', view_bot.bot_detail),
    # sentence
    path('sentences', view_sentence.sentences),
    # path('sentences/filter_table', view_sentence.filter_table),
    path('sentences/<id>', view_sentence.sentence_detail),
    # intent
    path('intents', view_intent.intents),
    path('intents/<id>', view_intent.intent_detail),
    # entity
    path('entities', view_entity.entity_types),
    path('entities/<id>', view_entity.entity_type_detail),
    # key word
    path('keywords', view_keyword.key_words),
    path('keywords/<id>', view_keyword.key_word_detail),
    # dictionary
    path('dictionaries', view_dictionary.dictionaries),
    path('dictionaries/<id>', view_dictionary.dictionary_detail),
    # step
    path('steps', view_step.steps),
    path('steps/jumpto', view_step.jumpto_step),
    path('steps/<id>', view_step.step_detail),
    # training and test
    path('training', view_ai.training),
    path('test_nlp', view_ai.test_nlp),
    # reply
    path('reply', view_reply.reply),
    # scenario
    path('scenarios', view_scenario.scenarios),
    path('scenarios/<id>', view_scenario.scenario_detail),
    # variable
    path('variables', view_variable.variables),
    path('variables/<id>', view_variable.variable_detail),
    # card
    path('cards', view_card.cards),
    path('cards/<id>', view_card.card_detail),
]
