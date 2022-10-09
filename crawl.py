#!/usr/bin/env python
# coding: utf-8


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from youtube_transcript_api import YouTubeTranscriptApi



headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'}



def get_soup(url):
    """get source code in soup format from a given link, if failed, retry up to 5 times 
    :param str url: a url from which the source code is to be obtained
    :return: the source code of the url
    :rtype: bs4.BeautifulSoup"""
    
    try:
        response = requests.get(url)
    except:
        pass
    if re.match("(?!200)\d{3}", str(response.status_code)): #200 means the request is successful
        tries = 1
        while tries < 5 and re.match("(?!200)\d{3}", str(response.status_code)):
            tries += 1
            response = requests.get(url)
        if re.match("(?!200)\d{3}", str(response.status_code)):
            print(url, ": request unsuccessful after 5 attempts.")
            return None
    soup = BeautifulSoup(response.content, 'html5lib')
    return soup


def crawl_website_links(domain_url, feature, link_set = None, target_link_set = None, domain_name = None, url = None, exclude_feature = None):
    """get all links within a website domain recursively, identifying or excluding links by a specific feature
    :param str domain_url: the main website from which all links is to be parsed 
    :param str feature: an identifying feature that defines the type of web pages to be retained in regex format (eg. 'youtube.com')
    :param link_set: a set that records all the links that has previously been parsed so they won't be parsed again
    :type link_set: set or None
    :param target_link_set: a set that records all the links that match the feature and thus will be retained in the return object
    :type target_link_set: set or None
    :param domain_name: specify the domain name of the target links, if it is different from the domain_url
    :type domain_name: str or None
    :param url: a custom url to initialise the crawling function, if it is not the same as the domain url 
    :type url: str or None
    :param exclude_feature: a feature to be excluded that defines the type of web pages to be skipped, in regex format
    :type exclude_feature: str or None
    :return: target_link_set, which contains only the links which contains the feature within the domain
    :rtype: set"""
    
    if domain_name == None:
        domain_name = "https://" + re.search("(?<=//).+", domain_url).group(0) + "/"
    if url == None:
        url = domain_url
        link_set = set()
        target_link_set = set()
    link_set.add(url)
    if len(link_set) % 20 == 0:
        print('currently went through', len(link_set), 'links.')
    soup = get_soup(url)

    if soup != None:
        for line in set(soup.select('[src]')).union(set(soup.select('[href]'))):
            try:
                link = line['href']
            except:
                link = line['src']
            # skip the link if excluded feature is found in the link
            if re.search("%s" %exclude_feature, link):
                continue
            # modify link if it starts with "//..." or "/..."
            elif re.match("^(?!\s*http).*$", link):
                if re.match("^\s*//", link):
                    link = "https:" + link
                else:
                    link = domain_name + link[1:]
            # skip the link if the link has been processed previously 
            if link in link_set:
                continue
            else:
                link_set.add(link)
                # add link to target_link_set if it contains the target feature
                if re.search(feature, link):
                    target_link_set.add(link)
                    # report progress
                    if len(target_link_set) % 20 == 0:
                        print('currently', len(target_link_set), 'links collected.')
                # skip if the link does not belong to the current domain
                elif re.search("^%s"%domain_name, link) == None:
                    continue
                else:
                    # continue to look for links recursively 
                    crawl_website_links(domain_url, feature = feature, link_set= link_set, target_link_set = target_link_set, domain_name = domain_name, url = link, exclude_feature = exclude_feature)
                    
    return target_link_set




def crawl_imginn(ig_account_name, title_regex= None, max_n_page = None, from_last_url = None):
    """get all text content from the posts of an instagram account via imginn.org
    :param str ig_account_name: the instagram account name 
    :param title_regex: a regex that can identify 'title' patterns from the instagram account, if it exists
    :type title_regex: str or None
    :param max_n_page: max number of pages (one page contains 12 posts) to be crawled; this can divide the crawling into multiple batches in case of a large number of posts
    :type max_n_page: int or None
    :param from_last_url: specify a different page to initialise the crawling function, if not starting from the first page
    :type from_last_url: str or None
    :return: a tuple with the first element a dictionary containing index, url, (title), content and comments of the instagram account, the second element of the next url to be crawled (if there is no next url, it will return an int 0)
    :rtype: tuple(dict, str or int)"""
    
    data = {}
    ind = 0
    if from_last_url == None:
        url = "https://imginn.org/%s/"%ig_account_name
        n_url = 0
    else:
        url = from_last_url
        account_id = re.search("(?<=id\=)\d+", next_url).group(0)
        n_url = 1
    has_next = True
    while has_next == True:
        n_url += 1 # number of pages that are loaded, every page should load 12 new articles 
        if n_url % 10 == 0:
            print("currently", n_url, 'pages.')
          
        #get the html source code of the loading webpage
        soup_load = get_soup(url)

        #get url code for each article, each loading page should contain 12 articles therefore 12 codes (except the bottom page)
        if n_url > 1:
            codes = re.findall("(?<=code\":\").+?(?=\")", soup_load.get_text())
        else: #the first page keeps the codes at a different place
            codes = [re.search("(?<=/p/).+(?=/)", item['href']).group(0) for item in soup_load.find_all("a", class_='item')]
        for code in codes: #access each article link
            doc_link = "https://imginn.org/p/" + code + "/"
              
            # get the source code for each post
            soup = get_soup(doc_link)

            ind += 1 # article id 
            data[ind] = {}
            data[ind]['url'] = doc_link

            # retrieve the text content of the post
            article = soup.find("div", class_='desc').get_text()
            
            # retrieve title if they're marked by a certain format (in terms of regex)
            if title_regex != None: 
                if re.search("(%s)"%title_regex, article):
                    title = re.search("(%s)"%title_regex, article).group(0)
                    data[ind]['title'] = title
                else:
                    data[ind]['title'] = '<untitled>'
    
            data[ind]['text'] = article

            # retrieve the comments under the post
            comments = soup.find("div", class_="comments").find_all("div", class_="text")
            data[ind]['comments'] = [comment.get_text() for comment in comments]

        # find next page cursor identification number
        if max_n_page == None:
            max_n_page = float('inf')
        if n_url < max_n_page:
            has_next = True
            #in the html source code, if there is a next page, it will have "hasNext: true"
            if n_url > 1 and re.search("\"hasNext\":true", soup_load.get_text()):
                cursor = re.search("(?<=\"cursor\":\").+(?=\")", soup_load.get_text()).group(0)
                if len(codes) != 12: #print a message if the page didnt have 12 codes in it 
                    print("not 12 articles:", url)
                    print(codes)
            elif n_url == 1: # this is encoded differently in the first page
                cursor = soup_load.find("a", class_= "more-posts")['data-cursor']
                #user id number, only need to retrieve once from the first page
                id = soup_load.find('div', class_= 'user-wrapper')['data-id']
            else: # reached the bottom of the posts
                has_next = False
                break
            #this is the url for the next loading page
            url = "https://imginn.org/api/posts/?id=%s&cursor="%id + cursor + "&type=user"
        # when reaching max_n_page but not the bottom of the account, return the url of the next loading page 
        elif re.search("\"hasNext\":true", soup_load.get_text()):
            has_next = False
            cursor = re.search("(?<=\"cursor\":\").+(?=\")", soup_load.get_text()).group(0)
            url = "https://imginn.org/api/posts/?id=%s&cursor="%id + cursor + "&type=user"
            return (data, url)
        else: # reached the bottom of the posts
            has_next = False
    if from_last_url == None:
        print("we have reached the end. There are ", n_url, "pages.")
    elif max_n_page != None:
        print("we have reached", max_n_page, "pages. There are ", n_url-1, "pages.")
    else:
        print("we have reached the end. There are ", n_url-1, "pages.")
    
    return (data, 0)



def get_youtube_transcript(url):
    """get cantonese and mandarin subtitles from a youtube video. A transcript contains a list of dictionaries that looks like this:
    [
    {
        'text': 'Hey there',
        'start': 7.58,
        'duration': 6.13
    },
    {
        'text': 'how are you',
        'start': 14.08,
        'duration': 7.58
    },
    # ...
    ]
    Note: Youtube sometimes blocks this module due to too many requests (code: 429), we may need to use a VPN to continue
    
    :param str url: a link to a youtube video which contains at least cantonese subtitles
    :return: a tuple of two lists, the former being the cantonese transcript and latter the mandarin transcript. 
             Returns empty list(s) if mandarin and/or cantonese subtitles do not exist. 
    :rtype: tuple(list, list)"""
    
    try:
        video_id = re.search("(?<=embed\/).+", url).group(0)
    except:
        try:
            video_id = re.search("(?<=v\=).+", url).group(0)
        except:
            print(url)
            print("invalid link")
            return ([],[])
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    except:
        print(url)
        print('transcripts not accessible')
        return ([],[])
    try:
        can_transcript = transcript_list.find_transcript(['zh-HK', 'yue-HK']).fetch()
    except:
        print(url)
        print('no cantonese')
        return ([],[])
    try:
        man_transcript = transcript_list.find_transcript(['zh-TW', 'zh-HANS', 'zh-HANT']).fetch()
    except:
        return (can_transcript, [])
    return (can_transcript, man_transcript)



def df_from_dict(data, save_csv = False, csv_file_path= None):
    """generate a pandas DataFrame from a dictionary object; creates a new index as id
    :param dict data: the data to be transformed into a df
    :param bool save_csv: an option to decide whether to save the df into a csv or not, default False
    :param csv_file_path: an option to specify where the csv is to be saved along with the file name. If None, the file will be saved in the current directory and the name 'crawled_data.csv'
    :type csv_file_path: str or None
    :return: data in df format
    :rtype: pandas.core.frame.DataFrame"""
    
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.reset_index(drop=False)
    df = df.rename(columns={"index": "id", "content": "text"})
    if save_csv == True:
        if csv_file_path == None:
            csv_file_path = "./crawled_data"
        df.to_csv('%s.csv'%csv_file_path)  
    return df


def df_from_subtitles(list_of_videos, parallel = False, save_csv = False, csv_file_path= None):
    """generate a pandas DataFrame from a list of youtube videos that contains at least cantonese subtitles; creates a new index as id
    :param list_of_videos: list of videos from which cantonese (and/or mandarin) subtitles are to be obtained
    :type list_of_videos: collections
    :param bool parallel: specify whether a cantonese-mandarin parallel df is to be created, default False. If True, cantonese subtitles will be matched to the nearest 'start' time of the mandarin subtitles in each video; if only some videos are parallel, the non-parallel ones will be filled with NaN values in the mandarin column.  
    :param bool save_csv: an option to decide whether to save the df into a csv or not, default False
    :param csv_file_path: an option to specify where the csv is to be saved along with the file name. If None, the file will be saved in the current directory and the name 'crawled_subtitle.csv'
    :type csv_file_path: str or None
    :return: data in df format
    :rtype: pandas.core.frame.DataFrame"""
    
    df = pd.DataFrame()
    for vid in list_of_videos:
        c, m = get_youtube_transcript(vid)
        if c ==[]:
            continue
        df1 = pd.DataFrame(c)
        df1['url'] = vid
        if parallel == True:
            if m == []:
                df2 = pd.DataFrame(np.zeros((len(df1),3)), index = range(len(df1)), columns = ['text','start','duration'])      
            else:
                df2 = pd.DataFrame(m)
            df2['url'] = vid
            dft = pd.merge_asof(df1.sort_values('start'), df2.sort_values('start'), on = 'start', by = 'url', tolerance=0.5, direction='nearest', allow_exact_matches = True)
        else:
            dft = df1
        df = df.append(dft, ignore_index = True)
    if save_csv == True:
        if csv_file_path == None:
            csv_file_path = "./crawled_subtitle"
        df.to_csv('%s.csv'%csv_file_path)  
    return df


def df_from_imginn(data, retain_comments = False, save_csv = False, csv_file_path= None):
    """generate a pandas DataFrame from data crawled from imginn (dict)
    :param dict data: the data to be transformed into a df
    :param bool retain_comments: specify whether comments are to be retained in the df, default False. If True, the function will 'explode' the df such that row contains one line of comment. 
    :param bool save_csv: an option to decide whether to save the df into a csv or not, default False
    :param csv_file_path: an option to specify where the csv is to be saved along with the file name. If None, the file will be saved in the current directory and the name 'crawled_imginn.csv'
    :type csv_file_path: str or None
    :return: data in df format
    :rtype: pandas.core.frame.DataFrame"""
    
    df = pd.DataFrame.from_dict(data, orient = 'index')
    if retain_comments == True:
        df = df.explode('comments')
    else:
        df = df.drop(columns = ["comments"])
    if save_csv == True:
        if csv_file_path == None:
            csv_file_path = "./crawled_imginn"
        df.to_csv('%s.csv'%csv_file_path)  
    return df

