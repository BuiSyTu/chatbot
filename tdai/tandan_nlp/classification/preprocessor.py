import re

from pyvi.ViTokenizer import ViTokenizer


def _remove_html(text):
    text = re.sub('<.*?>', '', text).strip()
    return text


def _normalize(text):
    return text.lower()


def _sentence_segment(text):
    sentences = re.split("[.?!]|[\n]", text)
    rs = [sentence.strip() for sentence in sentences if len(sentence) > 2]
    return rs


def _remove_special(sentence):
    return ''.join(e for e in sentence if e.isalnum() or e == ' ')


def _get_stop_words(file_path):
    data = open(file_path, encoding='utf8').read()
    return data.strip().split("\n")


def _remove_stop_words(sentence, stop_word_path='./tandan_nlp/dictionary/stop_words.txt'):
    list_stop_words = _get_stop_words(stop_word_path)
    words = sentence.split()
    pre_text = [word for word in words if word not in list_stop_words]
    rs = ' '.join(pre_text)
    return rs


def _word_segment(sent):
    return ViTokenizer.tokenize(sent)


def pre_processing(text):
    text = _remove_html(text)
    text = _normalize(text)
    sentences = _sentence_segment(text)
    rs = ''
    for sentence in sentences:
        sentence = _remove_special(sentence)
        word_in_sentence = _word_segment(sentence)
        sentence = ''.join(word_in_sentence)
        # sentence = _remove_stop_words(sentence)
        rs += ' ' + sentence
    return rs

# text = '<h1>Đây là tiêu đề. $%^####% Đây cũng là tiêu đề</h1>';
# print(_remove_html(text))
# print(_normalize(text))
# print(_sentence_segment(text))
# print(_remove_stop_words(text))
# print(_remove_special(text))
# print(pre_processing(text))
