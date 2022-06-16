import requests
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }

login_data = {
    'anchor': '',
    'logintoken': '',
    'username': 'USERNAME EINGEBEN',
    'password': 'PASSWORT EINGEBEN'
    }

input_data = {
    'chat_sid': '',
    'chat_message': ''
    }

update_data = {
    'chat_sid': '',
    'chat_lasttime': 1655383881,
    'chat_lastrow': 0
    }

with requests.Session() as S:
    #LOGIN
    url = 'https://moodle.htwg-konstanz.de/moodle/login/index.php'
    r = S.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    login_data['logintoken'] = soup.find('input', attrs={'name': 'logintoken'})['value'] #Logintoken herausfinden
    
    r = S.post(url, data=login_data, headers=headers) #Einloggen
    soup = BeautifulSoup(r.content, 'html5lib')
    
    
    #AUFGABENSTELLUNG DOWNLOAD
    r = S.get(soup.find(attrs={'title': 'RN'})['href'], headers=headers) #Rechnernetze aufrufen
    Rechnernetze = r.url
    soup = BeautifulSoup(r.content, 'html5lib')
    
    r = S.get('https://moodle.htwg-konstanz.de/moodle/mod/assign/view.php?id=219345', headers=headers) #Aufgabenstellung
    soup = BeautifulSoup(r.content, 'html5lib')
    
    r = S.get(soup.find('a', attrs={'target': '_blank'})['href'], headers=headers)
    with open('HTTP-Aufgabenstellung.docx', 'wb') as out_file: #Runterladen
        out_file.write(r.content)
        
    
    #CHATTEN
    r = S.get('https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_header_js/index.php?id=354', headers=headers) #chat starten
    soup = BeautifulSoup(r.content, 'html5lib')
    
    input_data['chat_sid'] = soup.find('frame', attrs={'name': 'users'})['src'].split('chat_sid=')[1] #chat_sid herausfinden
    input_data['chat_message'] = input('Nachricht eingeben:\n')
    S.post('https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_header_js/insert.php', data=input_data, headers=headers) #schreiben
    
    update_data['chat_sid'] = input_data['chat_sid']
    url2 = 'https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_header_js/jsupdate.php?chat_sid=' + update_data['chat_sid'] + '&chat_lasttime=' + str(update_data['chat_lasttime']) + '&chat_lastrow=' + str(update_data['chat_lastrow'])
    while(True):
        r = S.get(url2, data=update_data, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        nachrichten = str(r.content).split('<td class=\\\\"text\\\\"><span class=\\\\"title\\\\">')
        for i in range(len(nachrichten)-1):
            nachricht = nachrichten[i+1].split('<\\\\/span>: <p>')
            nameUhr = nachricht[0]
            na = nachricht[1].split('<\\\\/p><\\\\/td><\\\\/tr>', 1)
            msg = na[0]
            print(nachricht[0] + '\n\t' + msg)
        time.sleep(20)
        break
    