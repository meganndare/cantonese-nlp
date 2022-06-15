#!/usr/bin/env python
# coding: utf-8

# In[43]:


from crawl import *
from tqdm import tqdm


# # An example of crawling a website


# obtain all relevant links with the feature '/article/' in the domain
hsms_links = crawl_website_links("https://handstopmouthstop.com", feature = '/article/')


# get article title and content from each article link and save the data in a dict 'hsms_docs'. 
# This step is to be customised for every website

hsms_docs = {}
for i, link in enumerate(tqdm(hsms_links)):
    art_soup = get_soup(link)
    if art_soup != None:
        # get article title
        try:
            title = art_soup.h1.string
        except:
            title = ""

        #get article content (words only)
        content = []
        for line in art_soup.find("div", class_=re.compile("^entry-content")):
            string = line.get_text()
            # replace \xa0 (space)
            string = re.sub(u'\xa0', u' ', string)
            # replace \n+
            string = re.sub('\n+', '\n', string)
            string = string.split("\n")
            for s in string: #there might be multiple lines in the string, separated by \n
                # remove empty lines
                if re.match("^\s*$", s):
                    continue
                content.append(s)
        # save everything in a dictionary
        hsms_docs[i] = {}
        hsms_docs[i]["title"] = title
        hsms_docs[i]["url"] = link
        hsms_docs[i]["content"] = content


# # An example for crawling an instagram account via imginn.org


# crawling from instagram account: nownewshk
data, url = crawl_imginn("nownewshk")


# # Save data to df


df_hsms = df_from_dict(hsms_docs)


df_nownewshk = df_from_imginn(data, retain_comments = True)


# # An example of crawling subtitles from a list of youtube videos


# obtain all relevant links with the feature 'youtube.com' in the domain
domain = "https://sites.google.com/view/lihkg-kongjisubtitles/drama?authuser=0"
kjs_links = crawl_website_links(domain_url = domain, feature = 'youtube.com', domain_name = "https://sites.google.com/", exclude_feature = "#h")



# obtain df for each video, matching any cantonese-mandarin parallel subtitles
df_kjs = df_from_subtitles(kjs_links, parallel = True)

