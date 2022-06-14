import pre_processing as p
import sys
#wikipedia Cantonese data

opener = p.file_opener()
preprocessor = p.text_preprocessor()
if __name__ == "__main__":
    if sys.argv[1]=="wiki_cantonese":
        print("Text preprocessing might take very long time. Please be patient.")
        opener.open_wiki_files(path = sys.argv[2])
        c_cleaned = preprocessor.pre_process_monolingual(opener.wiki_texts,language = "c")
        c_cleaned_sentences = list()
        for file in c_cleaned:
            file_without_empty_list = [x for x in file if x != []]
            c_cleaned_sentences.append(file_without_empty_list)
        for name,text in zip(opener.wiki_names,c_cleaned_sentences):
            p.save_monolingual_sentences(resource_name = name,path= sys.argv[3],sentences = text)
    elif sys.argv[1]=="scraped_cantonese":
        print("Text preprocessing might take very long time. Please be patient.")
        opener.open_scraped_files(path = sys.argv[2])
        c_scraped_cleaned = preprocessor.pre_process(opener.scraped_texts)
        for name,text in zip(opener.scraped_names,c_scraped_cleaned):
            p.save_monolingual_sentences(resource_name = name,path= sys.argv[3],sentences = text)