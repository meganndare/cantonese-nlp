read_file = '../data/m_monolingual.txt'
write_file = '../data/mandarin.txt'


with open(read_file, 'r', encoding='utf-8') as f1:
    with open(write_file, 'w', encoding='utf-8') as f2:
        prev_resource, prev_text = f1.readline().split('|||')
        prev_text = prev_text.replace('\n', '')
        for line in f1.readlines():
            resource, text = line.split('|||')
            text = text.replace('\n', '')
            if 'wiki' in prev_resource and text.find(prev_text) == 0 and len(prev_text.split(' ')) <= 5:
                prev_resource, prev_text = resource, text
            elif 'zh - ' in prev_text:
                prev_resource, prev_text = resource, text
                print("zh detected and removed")
            else:
                f2.write(prev_text)
                f2.write('\n')
                prev_resource, prev_text = resource, text
        f2.write(prev_text)

