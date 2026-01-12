import requests
from bs4 import BeautifulSoup

from config import book_url, chapter_url, headers, ORDER_FILE, METADATA_FILE

XML_TEMPLATE = None
with open('templates/chapter.xml', 'r') as file:
    XML_TEMPLATE = file.read()

class save:
    @staticmethod
    def xml(title, content_tag):
        content = XML_TEMPLATE

        content = content.replace('Title', title)
        content = content.replace('Content', ''.join([str(x) for x in content_tag.find_all("div", "entry")[0].contents]))

        filename = title.replace('\n', ' ').replace('"', '').replace(':', '').replace('/', '').replace('\\', '').replace('?', '').replace('*', '').replace('<', '').replace('>', '').replace('|', '').strip()
        with open(f"chapters/{filename}.xml", 'w', encoding='UTF-8') as file:
            file.write(content)
        
        return filename

    def txt(title, content_tag):
        content = title + '\n\n'
        content += ''.join([str(x) for x in content_tag.find_all("div", "entry")[0].contents])
        content = content.replace('<p>', '')
        content = content.replace('</p>', '\n')

        filename = title.replace('\n', ' ').replace('"', '').replace(':', '').replace('/', '').replace('\\', '').replace('?', '').replace('*', '').replace('<', '').replace('>', '').replace('|', '').strip()
        with open(f"chapters/{filename}.txt", 'w', encoding='UTF-8') as file:
            file.write(content)

        return filename


def delifex(context, args):
    found = context.find_all(*args)

    for e in found:
        e.decompose()


def download_chapter(next_url, rec_counter=1):
    if not rec_counter:
        print('Рекурсия завершена.')
        return

    response = requests.get(next_url, headers=headers)
    # print(response.status_code)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        title_tag = soup.find_all("h1", "entry-title")[0]
        content_tag = soup.find_all("div", "entry-content")[0]
        
        delifex(content_tag, ("div", "adblock-service"))
        delifex(content_tag, ("div", "adfoxblock"))
        delifex(content_tag, ("div", "add-hand-mark"))
        delifex(content_tag, ("div", "clear"))
        delifex(content_tag, ("a",))

        ch_title = title_tag.get_text()
        xml_filename = save.xml(ch_title, content_tag)
        save.txt(ch_title, content_tag)
        
        with open(f'chapters/{ORDER_FILE}', 'a', encoding='utf-8') as file:
            file.write(xml_filename + '\n')

        print(f"Загружена [{ch_title}]")

        next_url_a = soup.find("li", "next").a
        if not next_url_a:
            print("Следующая глава не найдена.")
            return 
        
        next_url = next_url_a['href'] 

    else:
        print("BAD RESPONSE (Ошибка запроса)")
        print(response)
        return


    download_chapter(next_url, rec_counter-1)


def download_metadata(url):
    response = requests.get(url, headers=headers)
    # print(response.status_code)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        metadata_tag = soup.find_all('div', 'desc-book')[0]
        
        title = metadata_tag.find('h1').get_text()
        date = metadata_tag.find('div', 'date-home').contents[-1].get_text()
        annotation = ''.join([str(x) for x in metadata_tag.find('div', attrs={'id':'desc-tab'}).contents])

        with open(METADATA_FILE, 'w', encoding='utf-8') as file:
            file.write(title.strip().strip('\n') + '\n')
            file.write(date.strip().strip('\n') + '\n')
            file.write(annotation.strip().strip('\n'))


download_chapter(chapter_url, 50)
#download_metadata(book_url)