from bs4 import BeautifulSoup     
from selenium import webdriver
import concurrent.futures
from datetime import datetime


def get_total_pages(post_home_url, driver):
    driver.get(post_home_url)
    html = driver.page_source
    soup = BeautifulSoup(html, features='lxml')

    try: 
        total_pages = int(soup.find('span', {'class':'thispage'}).attrs['data-total-page'])
    except:
        total_pages = 0
    return total_pages

def get_urls(post_home_url, driver):
    total_pages = get_total_pages(post_home_url, driver)
    if total_pages != 0:
        urls = [f'{post_home_url}?start={p}'for p in range(total_pages)]
    else:
        urls = [post_home_url]
    return urls

def parse_comment(comment_element):
    comment_data = {}

    # header info
    user_face = comment_element.find('div', {'class':'user-face'}).find('img').attrs['src']
    user_id = comment_element.find('h4').find('a').text
    created_at = comment_element.find('span', {"class":"pubtime"}).text
    # is_op
    try:
        is_op = comment_element.find('h4').find("span", {"class":"topic-author-icon"}).text == "楼主"
    except:
        is_op = False


    # 必备内容 comment_content 
    cmt_content = comment_element.find('p', {'class':'reply-content'}).text

    # 保存必备内容
    comment_data['user_face'] = user_face
    comment_data['user_id'] = user_id
    comment_data['is_op'] = is_op
    comment_data['created_at'] = created_at
    comment_data['cmt_content'] = cmt_content



    # 先看有没有quote 再决定有没有quote img
    quoted_element = comment_element.find('div', {'class':'reply-quote'})
    if quoted_element == None:
        is_quoted = False
        comment_data['is_quoted'] = is_quoted
        have_quoted_img = False
        comment_data['have_quoted_img'] = have_quoted_img
    else:
        # 有quote 再拿到必备的quote content
        is_quoted = True
        comment_data['is_quoted'] = is_quoted

        quoted_content = quoted_element.find('span', {'class': 'all ref-content'}).text
        comment_data['quoted_content'] = quoted_content

        quoted_user_id = quoted_element.find('span', {"class":"pubdate"}).find('a').text
        comment_data['quoted_user_id'] = quoted_user_id
        # 有没有quote image
        quoted_img_element = quoted_element.find('img')
        if quoted_img_element == None:
            have_quoted_img = False
            comment_data['have_quoted_img'] = have_quoted_img
        else:
            have_quoted_img = True
            comment_data['have_quoted_img'] = have_quoted_img
            # gif
       
            try:
                is_quoted_img_gif = quoted_img_element.attrs['data-render-type'] =='gif'
                quoted_img_src = quoted_img_element.attrs['data-original-url']
            except:
                is_quoted_img_gif = False
                quoted_img_src = quoted_img_element.attrs['data-photo-url']
        
            comment_data['quoted_img_src'] = quoted_img_src
            comment_data['is_quoted_img_gif'] = is_quoted_img_gif


    # comment image
    if not have_quoted_img:
        have_cmt_img = len(comment_element.find_all('div', {'class':'comment-photos'})) == 1 
        comment_data['have_cmt_img'] = have_cmt_img

        if have_cmt_img:
            cmt_img_element = comment_element.find_all('div', {'class':'comment-photos'})[0]
            # is gif
            try:
                is_cmt_img_gif = cmt_img_element.find('img').attrs['data-render-type'] =='gif'
                cmt_img_src = cmt_img_element.find('img').attrs['data-original-url']
            except:
                is_cmt_img_gif = False
                cmt_img_src = cmt_img_element.find('img').attrs['data-photo-url']
            comment_data['cmt_img_src'] = cmt_img_src
            comment_data['is_cmt_img_gif'] = is_cmt_img_gif
    if have_quoted_img:
        have_cmt_img = len(comment_element.find_all('div', {'class':'comment-photos'})) == 2 
        comment_data['have_cmt_img'] = have_cmt_img

        if have_cmt_img:
            cmt_img_element = comment_element.find_all('div', {'class':'comment-photos'})[-1]
            # is gif
            try:
                is_cmt_img_gif = cmt_img_element.find('img').attrs['data-render-type'] =='gif'
                cmt_img_src = cmt_img_element.find('img').attrs['data-original-url']
            except:
                is_cmt_img_gif = False
                cmt_img_src = cmt_img_element.find('img').attrs['data-photo-url']
            comment_data['cmt_img_src'] = cmt_img_src
            comment_data['is_cmt_img_gif'] = is_cmt_img_gif
        
                
    # like cnt
    like_cnt = comment_element.find("a", {"class":"comment-vote lnk-fav lnk-reaction"}).text[3:-1]
    comment_data['like_cnt'] = like_cnt


    return comment_data


def get_all_comments_data(post_home_url, driver):
    urls = get_urls(post_home_url, driver)
    results = []
    def get_comments(url):
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, features='lxml')
        comments_elements = soup.find_all('li', {'class':'clearfix comment-item reply-item'})
        for comment_element in comments_elements:
            comment_data = parse_comment(comment_element)
            results.append(comment_data)
        return 
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_comments, urls)

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        'post_url': post_home_url,
        'update_time': update_time,
        'cmt_data': results
    }



