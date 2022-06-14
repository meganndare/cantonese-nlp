import re
import os
import pandas as pd
import pycantonese
import jieba
import sys
import emoji
from bs4 import BeautifulSoup

class text_preprocessor():
    def __init__(self):
        pass

    def pre_process(self,text):
        c_texts = list()
        m_texts = list()
        for i in text:
            sentences = [self.cut_sent(j) for j in i]
            sentences = [val for sublist in sentences for val in sublist]
            sentences = [item for item in sentences if pd.isnull(item) == False]
            c_text, m_text = self.cantonese_mandarin_filter(sentences) #seperate Cantonese text from Mandarin text

            c_text = [self.clean_sent(i) for i in c_text]
            c_text = [item for item in c_text if pd.isnull(item) == False]
            c_text = self.foreign_text_filter(c_text)
            c_text = [pycantonese.segment(i) for i in c_text]

#            m_text = [self.clean_sent(i) for i in m_text]
#            m_text = [item for item in m_text if pd.isnull(item) == False]
#            m_text = [jieba.lcut(i) for i in m_text]

            c_texts.append(c_text)
#            m_texts.append(m_text)
        return c_texts

    def pre_process_monolingual(self,text,language):
        texts = list()
        for i in text:
            sentences = [self.cut_sent(j) for j in i]
            sentences = [val for sublist in sentences for val in sublist]
            sentences = [item for item in sentences if pd.isnull(item) == False]
#            sentences = [self.clean_sent(i) for i in sentences]
            sentences = [item for item in sentences if pd.isnull(item) == False]
            if language =="c":
                sentences = [pycantonese.segment(i) for i in sentences]
            else:
                sentences = [jieba.lcut(i) for i in sentences]
            texts.append(sentences)

        return texts



    def cut_sent(self,para):
        """
        :param para: a paragraph of text
        :return: a list of sentences contained in the paragraph
        """
        para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
        para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
        para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
        para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
        # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
        para = para.rstrip()  # 段尾如果有多余的\n就去掉它
        # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
        return para.split("\n")

    def clean_sent(self,sent):
        """
        remove hashtag, link and emoji from sentence
        """
        #remove url
        sentence = re.sub('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})',
                          '',sent)

        #remove hashtag
        sentence = re.sub('(#.*?[\s\n$])','',sentence)

        #remove emoji
        emojis_iter = map(lambda y: y, emoji.UNICODE_EMOJI['en'].keys())
        regex_set = re.compile('|'.join(re.escape(em) for em in emojis_iter))
        sentence = re.sub(regex_set,'',sentence)

        return sentence

    def cantonese_mandarin_filter(self,text):
        """
        :param text: a list of texts that we are unsure in which language they are written
        :return: c_text is a list of Cantonese text, m_text is a list of Mandarin text
        """
        mandarin_texts = list()
        cantonese_texts = list()
        hky_markers = ['咗', '唔', '係', '喺', '啦', '嘅', '既', '咁',
                       '佢', '哋', '冇', '仲', '嘢', '乜', '噉', '咪',
                       '咩', '俾', '㗎', '呢', '嚟', '黎', '啫', '喂',
                       '喇', '喎', '睇']

        zh_markers = ['是', '的', '他', '她', '沒', '也', '看', '說', '在','说']
        c_text = list()
        m_text = list()
        for line in text:

            if len(line) <= 15:
                continue # if a line is too short, it is simply ignored

            # reset stats
            hky_dict = {}
            zh_dict = {}
            total_words = 0
            hky_words = 0
            zh_words = 0
            en_words = 0
            for word in hky_markers:
                hky_dict[word] = 0
            for word in zh_markers:
                zh_dict[word] = 0

            #filter lines written in foreign languages
            foreigner_text = re.findall(r"[^\u4e00-\u9fff]+", line)
            if len(foreigner_text)/len(line)>=0.4:
                continue

            characters = list(map(str, line.rstrip()))
            for character in characters:
                total_words = total_words + 1
                if character in hky_dict:
                    hky_words = hky_words + 1
                    hky_dict[character] = hky_dict[character] + 1
                elif character in zh_dict:
                    zh_words = zh_words + 1
                    zh_dict[character] = zh_dict[character] + 1

            hky_percent = hky_words / total_words
            zh_percent = zh_words / total_words
            hky_diff_percent = hky_percent - zh_percent

            if hky_diff_percent > 0.02:
                c_text.append(line)
            else:
                m_text.append(line)

        return c_text,m_text

    def foreign_text_filter(self,text):
        text_onlymc = list()
        for sentence in text:
            mc = re.findall(r'[\u4e00-\u9fff]+',sentence)
            mc_characters = [val for sublist in mc for val in sublist]
            if len(mc_characters)>len(text)*0.05:
                text_onlymc.append(sentence)
        return text_onlymc

class file_opener():

    def __init__(self):
        pass

    def open_scraped_files(self,path):
        """
        :param path: the folder that contains files
        :return texts: the list of text of files, names: the list of file names
        """
        texts = list()
        names = list()
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                f_path = os.path.join(root, name)
                f = pd.read_csv(f_path, engine="python", error_bad_lines=False, encoding="utf-8", sep=",")

                if "comment" in name:
                    text = list(f["comments"])
                else:
                    text = list(f["text"])

                text = [item for item in text if pd.isnull(item)==False] #remove NAN
                texts.append(text)
                names.append(name)
        self.scraped_texts = texts
        self.scraped_names = names

    def open_wiki_files(self,path):
        """
        :param path: the folder that contains files
        :return texts: the list of text of files, names: the list of file names
        """
        texts = list()
        names = list()
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                f_path = os.path.join(root, name)
                f = open(f_path,encoding = "utf-8")
                t =f.read()
                t_soup = BeautifulSoup(t,'html.parser')
                text = t_soup.get_text()
                texts.append(text)
                names.append(name)
        self.wiki_texts = texts
        self.wiki_names = names
        



def save_monolingual_sentences(resource_name,path,sentences):
    f = open(path, "a", encoding="utf-8")
    for s in sentences:
        tokens = " ".join(s)
        f.write(str(resource_name + "|||" + tokens + "\n"))
    f.close()

def save_parallel_sentences(sentences_c,sentences_m,resource_name,path):

    f = open(path, "a", encoding="utf-8")
    for c,m in zip(sentences_c,sentences_m):
        c_tokens = " ".join(c)
        m_tokens = " ".join(m)
        f.write(str(resource_name + "|||" + c_tokens + "|||" + m_tokens + "\n"))
    f.close()