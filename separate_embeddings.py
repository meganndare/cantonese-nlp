path_man = 'mandarin_shared_embedding.txt'
path_can = 'cantonese_shared_embedding.txt'
path_shared = 'shared_embedding.txt'

can_vocab = []
man_vocab = []

with open(path_man, 'r', encoding='utf-8') as f:
    i = 0
    for line in f.readlines():
        if i == 0:
            i += 1
            man_num = line.split(' ')[0]
        else:
            man_vocab.append(line.split(' ')[0])
with open(path_can, 'r', encoding='utf-8') as f:
    i = 0
    for line in f.readlines():
        if i == 0:
            i += 1
            can_num = line.split(' ')[0]
        else:
            can_vocab.append(line.split(' ')[0])

path_can_write = 'cantonese_con_embedding.txt'
path_man_write = 'mandarin_con_embedding.txt'
with open(path_can_write, 'w', encoding='utf-8') as f1:
    with open(path_man_write, 'w', encoding='utf-8') as f2:
        f1.write(str(can_num)+' '+str(512)+'\n')
        f2.write(str(man_num)+' '+str(512)+'\n')
        with open(path_shared, 'r', encoding='utf-8') as f:
            i = 0
            for line in f.readlines():
                if i == 0:
                    i += 1
                else:
                    if line.split(' ')[0] in can_vocab:
                        f1.write(line)
                    if line.split(' ')[0] in man_vocab:
                        f2.write(line)
