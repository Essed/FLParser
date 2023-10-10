from requests import Response
from requests_html import HTMLSession
from sortutils import findWP, hasWords, hasWords2, hasWordsCamel, copyPattern, findW
from urlmoder import mod_url
from saver import write_csv
from helpers import repeator
import re

FILE = 'C:/Users/vipar/OneDrive/Desktop/FData/florders.csv'
URL = "https://www.fl.ru/projects/category/programmirovanie/?page=&kind=5"


def get_content_body(response: Response):

    b_post = response.html.find('.b-post__txt')

    post_content = [post.text for post in b_post if len(post.text.strip().replace('\n', ''))]

    tmp_list = [post for post in post_content if post.isnumeric() == False and hasWords(post,
     ['исполнитель определён', 'больше 300', 'вакансия (россия)']) == False and hasWordsCamel(post, ['Вакансия']) == False 
     and findW(post, "Заказ") == False and findW(post, "Вакансия") == False and findWP(post, "Конкурс\s+\w+") == False]

    return tmp_list

def get_link_header(response: Response):
    b_post_links = response.html.find('.b-post__link')
    
    post_list = [[*post.absolute_links,] for post in b_post_links]

    post_dict = dict()

    for x in post_list:
        post_dict[x[0]] = x[0]

    post_list = [post for post in post_dict.keys()]

    return post_list

def get_link_name(response: Response):
    b_post_links = response.html.find('.b-post__link')
    post_list = [post.text for post in b_post_links if hasWords2(post.text, ['ответов', 'ответа', 'исполнитель', 'определён' 'нет ответов', 'ответ']) == False 
    and hasWordsCamel(post.text, ['Нет участников']) == False]

    return post_list

def get_type_trade(response: Response):
    b_post_price = response.html.find('.b-post__price')

    price_list = list()

    for post in b_post_price:
        text = post.text
        type_trade = ""
        rewards = re.findall(r'\d+', text)
        delimeter = ''
        reward_str = ''

        if hasWords(text.lower(), ['безопасная сделка']):              
               type_trade = "безопасная сделка".capitalize() 
        else:               
               type_trade = "Не указано"
        
        if re.search(r'—', text):
            delimeter = '—'
            reward_str = (f"{delimeter}").join(rewards)
            reward_str += " руб"
        elif hasWords(text.lower(), ['по договоренности', 'по результатам собеседования']):
            reward_str = copyPattern(text.lower(), ['по договоренности', 'по результатам собеседования'])
        else:
            reward_str = " ".join(rewards).strip()
            reward_str += " руб"
          
        datatup = tuple([type_trade, reward_str])
        price_list.append(datatup)

    return price_list

def get_pages(response: Response):
    b_post_pages = response.html.find('.b-pager__item')

    return int(b_post_pages[-1].text)

def get_content(response: Response):
    content_list = get_content_body(response)
    link_list = get_link_header(response)
    linkname_list = get_link_name(response)
    trade_list = get_type_trade(response)


    orders = list()

    for x in range(0, len(content_list)):
        orders.append({
            'title': linkname_list[x],
            'link': link_list[x],
            'description': content_list[x],
            'pay_type': trade_list[x][0],
            'cost': trade_list[x][1]
        })
  
    return orders

@repeator(30)
def parse():
    session = HTMLSession()

    url = mod_url(URL, "page=", 1)
    
    r = session.get(url)
    
    r.html.render()        

    last_index_page = 1

    all_orders = list()
    while True:
        orders = list()

        pages_count = get_pages(r)

        if r.status_code == 200:

            for page in range(last_index_page, pages_count + 1):
                print(f"Парсинг {page} страницы ...")
                new_url = mod_url(URL, "page=", last_index_page)                
                r = session.get(new_url)
                r.html.render()
                orders.extend(get_content(r))                
                last_index_page+=1

            if len(orders) == 0:
                break
            
            all_orders.extend(orders)
         
        else:
            print("Error")

    write_csv(FILE, all_orders)


if __name__ == "__main__":
    parse()