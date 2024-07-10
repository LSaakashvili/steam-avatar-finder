from bs4 import BeautifulSoup
from os import system
from termcolor import colored
import threading
import time
import requests

system("color")

search_url = "https://steamcommunity.com/search/SearchCommunityAjax?text={name}&filter=users&sessionid={session_id}&steamid_user=false&page={page}"
params = { 'found': False }


def avatar_finder(name, avatar, session_id):
    print(name, avatar)
    if (avatar == "https://avatars.cloudflare.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_medium.jpg"):
        return None

    def find_pages(page):
        exact_search_url = search_url.format(session_id=session_id, name=name, page=page)

        res = requests.get(url=exact_search_url, headers={
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"sessionid={session_id};",
            "Host": "steamcommunity.com",
            "Origin": "https://steamcommunity.com",
            "Referer": "https://steamcommunity.com/groups/plus-rep"
        }).json()
        html_txt = res['html']
            
        soup = BeautifulSoup(html_txt, 'html.parser')
        all_imgs = soup.find_all('img')

        for img in all_imgs:
            if img['src'] == avatar:
                username = img.parent.parent.parent.parent.find_all('a')[1].text

                if (username.lower() == name.lower()):
                    print(colored("PROFILE FOUND - " + img.parent['href'], "green"))
                    params["found"] = True
                    return True
    
    page = 1
    while page <= 500 and params["found"] == False:
                thread = threading.Thread(target=find_pages, args=[page])
                thread.start()
                page += 1
                
    time.sleep(7)

if __name__ == "__main__":
    print("Input Steam Name Of User...")
    username = input("")
    
    print("Input Steam Avatar Url Of User...")
    avatar_url = input("")
    
    avatar_finder(username, avatar_url, "aeaefaefaefa")