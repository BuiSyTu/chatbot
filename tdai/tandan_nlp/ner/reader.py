import re

from pyvi import ViTokenizer, ViPosTagger


def _sentence_segment(text):
    sentences = re.split("[.?!]|[\n]", text)
    rs = [sentence.strip() for sentence in sentences if len(sentence) > 2]
    return rs


def read_entities(text, _words, labels):
    tokenized_text = ViTokenizer.tokenize(text)
    print(tokenized_text)
    pos_tagging_texts = ViPosTagger.postagging(tokenized_text)

    rs_word = pos_tagging_texts[0]
    rs_pos = pos_tagging_texts[1]

    rs_entity = []
    for pos_tagging_text in pos_tagging_texts[0]:
        is_label = 0
        for j, word in enumerate(_words):
            tokenized_word = ViTokenizer.tokenize(word)
            if pos_tagging_text == tokenized_word:
                rs_entity.append(labels[j])
                is_label = 1
        if is_label == 0:
            rs_entity.append('O')
    return rs_word, rs_pos, rs_entity


# words = ['đại học', 'bách khoa', 'hà nội']
#
# entities = ['I', 'I-LOC2', 'I-LOC1']
# print(read_entities('trường đại_học bách_khoa hà_nội. trường đại học bách khoa hà nội', words, entities))
