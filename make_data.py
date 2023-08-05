import os 
import random
from zhtools.langconv import Converter
import pandas as pd 


word_list = []
datas = []

converter = Converter('zh-hans')

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False

def is_number(uchar):
    """判断一个unicode是否是半角数字"""
    if uchar >= u'\u0030' and uchar<=u'\u0039':
        return True
    else:
        return False

def is_english(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u0061' and uchar<=u'\u007a':
        return True
    else:
        return False

def Q2B(uchar):
    """单个字符 全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e: #转完之后不是半角字符返回原来的字符
        return uchar
    return chr(inside_code)


# 读取标注文件
data = pd.read_csv('data/train_label.csv',encoding = 'gb2312')
for i in range(len(data)):
    name, label = data.iloc[i,:]
    label = label.replace('　','')
    label = converter.convert(label)
    label.lower()
    new_label = []
    for word in label:
        word = Q2B(word)
        if is_chinese(word) or is_number(word) or is_english(word):
            new_label.append(word)
            if word not in word_list:
                word_list.append(word)
    if new_label!=[]:
        datas.append('%s\t%s\n' % (os.path.join('train_images',name), ''.join(new_label)))

word_list.sort()

# 生成词表
with open('data/vocab.txt', 'w', encoding='UTF-8') as f:
    for word in word_list:
        f.write(word+'\n')

random.shuffle(datas)
# 训练数据95% 验证数据%5
split_num = int(len(datas)*0.95)

print('训练数据：',split_num,'验证数据：',int(len(datas)*0.05))
# 分割数据为训练和验证集
with open('data/train.txt', 'w', encoding='UTF-8') as f:
    for line in datas[:split_num]:
        f.write(line)

with open('data/dev.txt', 'w', encoding='UTF-8') as f:
    for line in datas[split_num:]:
        f.write(line)