import opencc

converter1 = opencc.OpenCC('s2hk.json')
converter2 = opencc.OpenCC('t2hk.json')

read_file = 'test/test_cantonese_cross_char.txt'
write_file = 'test/test_cantonese_char_hk.txt'

line_num = 0
with open(read_file, 'r', encoding='utf-8') as f1:
    with open(write_file, 'w', encoding='utf-8') as f2:
        for line in f1.readlines():
            hk_line = converter2.convert(converter1.convert(line))
            f2.write(hk_line)
            line_num += 1
            if line_num % 1000 == 0:
                print(str(line_num)+" sentences have been converted.")