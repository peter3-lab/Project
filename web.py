import requests
from bs4 import BeautifulSoup
from MySqlHelper import MySqlHelper

def scrape_baidu_hot_search():
    """
    爬取百度热搜榜 Top 10。
    """
    url = "https://top.baidu.com/board?tab=realtime"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        
 
        hot_list = []

        items = soup.find_all('div', class_='c-board-item')
        
        for index, item in enumerate(items[:10]): # 获取前10个
            title_div = item.find('div', class_='c-single-text-ellipsis')
            link_tag = item.find('a', class_='c-board-title')
            
            if title_div:
                title = title_div.text.strip()
                link = link_tag['href'].strip() if link_tag else ''
                hot_list.append({'rank': index + 1, 'title': title, 'url': link})
                
        return hot_list

    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return []

def save_to_db(hot_list):
    """
    将热搜列表保存到数据库。
    """
    if not hot_list:
        print("没有可保存的数据。")
        return


    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'database': 'project_db'
    }

    try:
        with MySqlHelper(**db_config) as db:
            # 可选：先清空旧数据
            db.execute_update("DELETE FROM baidu_hot_search")
            print("旧数据已清除。")
            
            sql = "INSERT INTO baidu_hot_search (rank, title, url) VALUES (%s, %s, %s)"
            for item in hot_list:
                db.execute_update(sql, (item['rank'], item['title'], item['url']))
            print(f"成功将 {len(hot_list)} 条百度热搜数据存入数据库。")
    except Exception as e:
        print(f"数据库操作失败: {e}")


if __name__ == '__main__':
    top10_list = scrape_baidu_hot_search()
    save_to_db(top10_list)