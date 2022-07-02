import pickle
path = '../data/cantonese.txt'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# for line in lines:
#
#     sents.append(line.split('|||')[1])
print(len(set(lines)))
print(len(lines))
sents = [line.split(' ') for line in lines]
len_dict = dict()
for sent in sents:
    if len(sent) not in len_dict.keys():
        len_dict[len(sent)] = 1
    else:
        len_dict[len(sent)] += 1

with open('can_stat.pkl', 'wb') as f:
    pickle.dump(len_dict, f)
