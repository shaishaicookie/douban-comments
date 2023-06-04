from bs4 import BeautifulSoup     
from selenium import webdriver
from datetime import datetime


def parse_p(tag):
    tag_type = 'p'
    text = tag.text
    if 'https' in text:
        text = text.split('https')[0]

    text = text.replace('\n', '')

    is_href = not (tag.find('a') == None)
    if is_href:
        href = tag.find('a').text
    else:
        href = ''
    result = {
        'tag_type': tag_type,
        'text': text,
        'is_href': is_href,
        'href': href
    }

    return result


def parse_img(tag):
    tag_type = 'img'
    is_gif = tag.find('img').has_attr('data-render-type')
    if is_gif:
        img_src = tag.find('img').attrs['data-original-url']
    else:
        img_src = tag.find('img').attrs['src']
    have_img_caption = not (tag.find('div', {'class': 'image-caption'}) == None)
    if have_img_caption:
        img_caption = tag.find('div', {'class': 'image-caption'}).text
    else:
        img_caption = ''

    result = {
        'tag_type': tag_type,
        'is_gif': is_gif,
        'img_src': img_src,
        'have_img_caption': have_img_caption,
        'img_caption': img_caption
    }

    return result


def parse_topic_card(tag):
    tag_type = 'topic-card'
    # grop_info
    group_link = tag.find('a', {'class': 'group-hd'}).attrs['href']
    group_img = tag.find('div', {'class': 'group-avatar'}).find('img').attrs['src']
    group_name = tag.find('strong').text
    group_detial = tag.find('span').text

    # topic info
    topic_link = tag.find('a', {'class': 'topic-main'}).attrs['href']
    topic_img = tag.find('div', {'class': 'topic-cover'}).find('img').attrs['src']
    topic_title = tag.find('span', {'class':'topic-title'}).text
    topic_desc = tag.find('span', {'class': 'topic-desc'}).text


    result = {
        'tag_type': tag_type,
        'group_link': group_link,
        'group_img': group_img,
        'group_name': group_name,
        'group_detial': group_detial,
        'topic_link': topic_link,
        'topic_img': topic_img,
        'topic_title': topic_title,
        'topic_desc': topic_desc
    }
    return result


def parse_poll(tag):
    tag_type = 'poll'
    poll_title = tag.find('div', {'class':'poll-title'}).text
    poll_meta = tag.find('div', {'class':'poll-meta'}).text
    poll_options = [option.text for option in tag.find_all('span', {'class': 'poll-option'})]

    result = {
        'tag_type': tag_type,
        'poll_title': poll_title,
        'poll_meta': poll_meta,
        'poll_options': poll_options
    }
    return result

def parse_video_card(tag):
    tag_type = 'video-card'
    video_href = tag.find('a').attrs['href']
    video_cover = tag.find('img', {'class': 'video-cover'}).attrs['src']
    video_card_title = tag.find('div', {'class': 'video-card-title'}).text
    video_card_source = tag.find('div', {'class': 'video-card-source'}).text

    result = {
        'tag_type': tag_type,
        'video_href': video_href,
        'video_cover': video_cover,
        'video_cover': video_cover,
        'video_card_source': video_card_source
    }

    return result
    

def parse_video_wrapper(tag):
    tag_type = 'video-wrapper'
    video_link = tag.find('iframe').attrs['src']
    result = {
        'tag_type': tag_type,
        'video_link': video_link
    }
    return result


def assign_parse_type(contents):
    result = []
    for c in contents:
        tag_name = c.name
        if tag_name == 'p':
            result.append({
                'tag': c,
                'parse_type': parse_p
            })
        
        # div
        else:
            spec_div_tag = c.get('class')[0]

            if spec_div_tag == 'image-container':
                result.append({
                    'tag': c,
                    'parse_type': parse_img
                })
            if spec_div_tag == 'topic-card':
                result.append({
                    'tag': c,
                    'parse_type': parse_topic_card
                })
            if spec_div_tag == 'rendered':
                result.append({
                    'tag': c,
                    'parse_type': parse_poll
                })
            if spec_div_tag == 'video-card':
                result.append({
                    'tag': c,
                    'parse_type': parse_video_card
                })
            if spec_div_tag == 'video-wrapper':
                result.append({
                    'tag': c,
                    'parse_type': parse_video_wrapper
                })

    return result
            


def craw_body(driver, post_url):
    driver.get(post_url)
    html = driver.page_source
    soup = BeautifulSoup(html, features='lxml')
    
    return soup


def parse_body_data(soup, post_url):
    body = soup.find('div', {'class', 'article'})
    # header info
    title = soup.find('h1').text.replace('\n', '').replace(' ', '')
    op_user_face_src = soup.find('div', {'class': 'user-face'}).find('img', {'class': 'pil'}).attrs['src']
    op_user_id = soup.find('div', {'class': 'user-face'}).find('img', {'class': 'pil'}).attrs['alt']
    created_at = soup.find('span', {'class': 'create-time color-green'}).text + ' ' + soup.find('span', {'class': 'create-ip'}).text

    # contents
    contents = body.find('div', {'class': 'rich-content topic-richtext'}).contents[1:-1]

    assigned_contents = assign_parse_type(contents)
    # [{tag, parse_type}]
    body_data = []

    for idx, c in enumerate(assigned_contents):
        c_tag = c['tag']
        c_data = c['parse_type'](c_tag)
        c_data['idx'] = idx
        body_data.append(c_data)


    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = {
        'post_url': post_url,
        'update_time': update_time,
        'title': title,
        'op_user_face_src': op_user_face_src,
        'op_user_id': op_user_id,
        'created_at': created_at, 
        'body_data': body_data
    }

    return result



def get_body_data(driver, post_url):
    soup = craw_body(driver, post_url)
    return parse_body_data(soup, post_url)

