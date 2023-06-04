import comment_crawler
from selenium import webdriver

post_home_url = 'https://www.douban.com/group/topic/281977473/'
driver = webdriver.Chrome()   


cmt_data = comment_crawler.get_all_comments_data(post_home_url=post_home_url, driver=driver)

print(cmt_data)
print(type(cmt_data))
