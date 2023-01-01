import os 
import time 
import requests
import json
import pandas       
from bs4 import BeautifulSoup     
from selenium import webdriver
from tqdm import tqdm


def get_comments(post_url):
    driver = webdriver.Chrome()
    driver.get(post_url)
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")
    page_num = int(soup.find("span", {"class":"thispage"}).attrs["data-total-page"])
    
    tmp = [] # list of list of comments
    for p in tqdm(range(page_num)):
        curr_page_url = post_url + '?start=' + str(p*100)
        driver.get(curr_page_url)
        html = driver.page_source
        soup = BeautifulSoup(html, features="lxml")
        curr_comments = soup.find_all("li", {"class":"clearfix comment-item reply-item"})
        tmp.append(curr_comments)

    comments = [c for sub_comments in tmp for c in sub_comments] # flatten tmp comments
    return comments

def get_op_comments(post_url):
    driver = webdriver.Chrome()
    op_post_url = post_url + '?author=1'
    driver.get(op_post_url)
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")
    page_num = int(soup.find("span", {"class":"thispage"}).attrs["data-total-page"])
    
    tmp = [] # list of list of comments
    for p in tqdm(range(page_num)):
        curr_page_url = post_url + '?start=' + str(p*100)
        driver.get(curr_page_url)
        html = driver.page_source
        soup = BeautifulSoup(html, features="lxml")
        curr_comments = soup.find_all("li", {"class":"clearfix comment-item reply-item"})
        tmp.append(curr_comments)

    op_comments = [c for sub_comments in tmp for c in sub_comments] # flatten tmp comments
    return op_comments
   
def get_top5_comments(post_url):
    driver = webdriver.Chrome()
    driver.get(post_url)
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")
    top5_comments = soup.find_all("li", {"class":"clearfix comment-item reply-item"})[:5]
    return top5_comments

 
def save_comment(comment, i, cmt_type):
    '''
        comment --  one comment tag
        i -- idx
        type: 'all', 'op', 'top5'
    '''
    comment_data = {}

    # user face
    user_face_link = comment.find('div', {'class':'user-face'}).find('img').attrs['src']
    user_face_fname = str(i) + '-user-face.png'
    # save user face
    with open('./images/' + cmt_type + '/' + user_face_fname, 'wb') as f:
        f.write(requests.get(user_face_link).content)
    comment_data['user_face'] = user_face_fname

    # cmt header 1. is_starter 2. user_id 3. time + location
    try:
        is_starter = comment.find('h4').find("span", {"class":"topic-author-icon"}).text == "楼主"
    except:
        is_starter = False

    user_id = comment.find('h4').find('a').text
    user_pubtime = comment.find('span', {"class":"pubtime"}).text
    comment_data['user_id'] = user_id
    comment_data['is_starter'] = is_starter
    comment_data['user_pubtime'] = user_pubtime

    # quote section
    quote = {}
    quote_tag = comment.find('div', {'class':'reply-quote'})
    if quote_tag == None:
        quote_status = False
        quote['quote_status'] = quote_status
    else:
        quote_status = True
        # 1. quote_content, 2. quote user id
        quote_content = quote_tag.find('span', {'class': 'all ref-content'}).text
        quote_user_id = quote_tag.find('span', {"class":"pubdate"}).find('a').text
        quote['quote_status'] = quote_status
        quote['quote_content'] = quote_content
        quote['quote_user_id'] = quote_user_id

        # quote img section
        quote_img = {}
        quote_img_tag = quote_tag.find('div', {'class': 'cmt-img'})
        if quote_img_tag == None:
            quote_img_status = False
            quote_img['quote_img_status'] = quote_img_status
        else:
            quote_img_status = True
            quote_img['quote_img_status'] = quote_img_status

            # is gif
            try:
                is_gif = quote_img_tag.find('img').attrs['data-render-type'] =='gif'
                quote_img_link = quote_img_tag.find('img').attrs['data-original-url']
            except:
                is_gif = False
                quote_img_link = quote_img_tag.find('img').attrs['data-photo-url']
            quote_img['is_gif'] = is_gif

        # save quote img
            quote_img_fname = str(i) + '-quote.png'
            with open('./images/all/' + cmt_type + '/' + quote_img_fname, 'wb') as f:
                f.write(requests.get(quote_img_link).content)
            quote_img['quote_img_src'] = quote_img_fname

        quote['quote_img'] = quote_img

    comment_data['quote']=quote


    # comment section 
    cmt = {}
    cmt_content = comment.find('p', {'class':'reply-content'}).text
    cmt['cmt_content'] = cmt_content

    # comment img section
    cmt_img = {}
    cmt_img_tag = comment.find('div', {'class':'comment-photos'})
    # whether exist comment img 
    if cmt_img_tag == None:
        cmt_img_status = False
        cmt_img[cmt_img_status] = cmt_img_status
    else:
        cmt_img_status = True
        cmt_img['cmt_img_status'] = cmt_img_status
        try: 
            is_gif = cmt_img_tag.find('img').attrs['data-render-type'] =='gif'
            cmt_img_link = cmt_img_tag.find('img').attrs['data-original-url']
        except:
            is_gif = False
            cmt_img_link = cmt_img_tag.find('img').attrs['data-photo-url']
        cmt_img['is_gif'] = is_gif

        # save comment img
        cmt_img_fname = str(i) + '-cmt.png'
        with open('./images/' + cmt_type + '/' + cmt_img_fname, 'wb') as f:
            f.write(requests.get(cmt_img_link).content)
        cmt_img['cmt_img_src'] = cmt_img_fname
        
        cmt['cmt_img'] = cmt_img

    comment_data['cmt'] = cmt


    # like cnt section
    like_cnt = comment.find("a", {"class":"comment-vote lnk-fav lnk-reaction"}).text[3:-1]
    comment_data['like_cnt'] = like_cnt

    return comment_data


def save_comments(comments, cmt_type):
    comments_data = {}
    for idx in tqdm(range(len(comments))):
        comment = comments[idx]
        comments_data[str(idx)] = save_comment(comment, idx, cmt_type)
    return comments_data


def save_data(comments_data, fname):
    with open(fname, 'w') as f:
        json.dump(comments_data, f, indent = 4, ensure_ascii=False)



post_url = 'https://www.douban.com/group/topic/279199969/'

top5_comments = get_top5_comments(post_url)
top5_data = save_data(save_comments(top5_comments, 'top5'), 'top5_data.json')

op_comments = get_op_comments(post_url)
op_data = save_data(save_comments(op_comments, 'op'), 'op_data.json')

comments = get_comments(post_url)
all_data = save_data(save_comments(comments, 'all'), 'all_data.json')