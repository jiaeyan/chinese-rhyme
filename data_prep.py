import re
from collections import defaultdict
from typing import List, Tuple
from pypinyin import lazy_pinyin
from pypinyin.phrases_dict import phrases_dict
from parser import word_parser
from phrase_dict import phrase_dict


vocab = set()

with open('data/cidian.txt', 'r', encoding='gb18030') as f:
    for line in f:
        if '【' in line:
            words = re.findall(r'【(.+?)】', line.strip())[0].split('，')
            for word in words:
                vocab.add(word.strip())

with open('data/chengyu.txt', 'r', encoding='gb18030') as f:
    for line in f:
        if "拼音" in line:
            words = re.findall(r'(.+?)拼音.+', line.strip())[0].strip().split('，')
            for word in words:
                vocab.add(word.strip())

for words in phrases_dict:
    for word in words.split('，'):
        vocab.add(word.strip())

look_up = defaultdict(list)
for word in vocab:
    pinyins = word_parser(word)
    look_up[tuple([pinyin[1][-1] for pinyin in pinyins])].append(word)

with open('phrase_dict.py', 'w') as f:
    f.write('phrase_dict = {\n')
    for k, v in look_up.items():
        f.write('\t{}:{},\n'.format(k, sorted(v)))
    f.write('}')
    print('done!')


#
# for k, v in look_up.items():
#     print(k, sorted(v))

# look_up = defaultdict(list)
# for word, vowels in [(word, get_vowels(word)) for word in vocab]:
#     look_up[vowels].append(word)

# print('[双押词]:\n', '\n'.join(look_up[get_vowels(input('请输入一个你想押韵的词: '))]))