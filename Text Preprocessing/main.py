import pre_processing as p
import sys
#wikipedia Cantonese data

opener = p.file_opener()
preprocessor = p.text_preprocessor()
if __name__ == "__main__":
    if sys.argv[1]=="wiki_cantonese":
        print("Text preprocessing might take very long time. Please be patient.")
        opener.open_wiki_files(path = sys.argv[2])
        c_cleaned = preprocessor.pre_process_wiki(opener.wiki_texts,language = "c")
        for name,text in zip(opener.wiki_names,c_cleaned):
            p.save_monolingual_sentences(resource_name = name,path= sys.argv[3],sentences = text)
    elif sys.argv[1]=="scraped_cantonese":
        print("Text preprocessing might take very long time. Please be patient.")
        opener.open_scraped_files(path = sys.argv[2])
        c_scraped_cleaned = preprocessor.pre_process(opener.scraped_texts)
        for name,text in zip(opener.scraped_names,c_scraped_cleaned):
            p.save_monolingual_sentences(resource_name = name,path= sys.argv[3],sentences = text)

    elif sys.argv[1]=="youtube_cantonese":
        print("Text preprocessing might take very long time. Please be patient.")
        opener.open_youtube(path = sys.argv[2])
        c_youtube_cleaned = preprocessor.pre_process(opener.youtube_texts)
        for name,text in zip(opener.youtube_names,c_youtube_cleaned):
            p.save_monolingual_sentences(resource_name = name,path= sys.argv[3],sentences = text)

    elif sys.argv[1]=="wiki_mandarin":
        print("Text preprocessing might take very long time. Please be patient.")
        opener.open_wiki_files(path = sys.argv[2])
        m_cleaned = preprocessor.pre_process_wiki(opener.wiki_texts,language = "m")
        for name, text in zip(opener.wiki_names, m_cleaned):
            p.save_monolingual_sentences(resource_name=name, path=sys.argv[3], sentences=text)
    else:
        print("There is something wrong with your second argument.")
