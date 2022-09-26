from pyvi.ViPosTagger import ViPosTagger
from pyvi.ViTokenizer import ViTokenizer

from chat_bot.models import KeyWord, Entity

from .feature_extractor import sent2features


def predict_entity(text, model):
    # process text
    tokenized_text = ViTokenizer.tokenize(text)
    pos_tagging_text = ViPosTagger.postagging(ViTokenizer.tokenize(tokenized_text))
    rs_word = pos_tagging_text[0]
    rs_pos = pos_tagging_text[1]

    # len(rs_word) = len(rs_pos)
    length = len(rs_word)

    # add feature
    sent = []
    [sent.append((rs_word[i], rs_pos[i])) for i in range(length)]

    # predict
    features = [sent2features(sent)]
    y_pred = model.predict([sent2features(sent)])
    rs = []
    [rs.append((rs_word[i].replace("_", " "), rs_pos[i], y_pred[0][i])) for i in range(length) if y_pred[0][i] != 'O']
    
    # FIXME: hard code keyword to entity
    keywords = KeyWord.objects.all()
    for keyword in keywords:
        text_compare = text.lower()
        keyword_compare = keyword.keyword.lower()

        if (keyword_compare in text_compare):
            rs_tmp = [item[0] for item in rs]
            if keyword.keyword not in rs_tmp:
                entity = Entity.objects.get(id=keyword.entity_id)
                rs.append((keyword.keyword, '', entity.entity))

    return rs


# test
# import pickle
# model = pickle.load(open('./../model/ner.sav', 'rb'))
# print(predict_entity('Ngày 28/10, lực lượng An ninh điều tra, Công an tỉnh An Giang phối hợp cùng Phòng Kỹ thuật hình sự, Công an huyện Mù Cang và các lực lượng chức năng kiểm tra hành chính địa điểm trên. Qua kiểm tra, lực lượng chức năng phát hiện và thu giữ hơn 28 triệu đồng tiền giả với các mệnh giá 50.000 đồng, 200.000 đồng và 500.000 đồng; một máy in màu hiệu Cannon, một laptop, một bàn là cùng nhiều tang vật liên quan đến việc làm tiền giả.',model))