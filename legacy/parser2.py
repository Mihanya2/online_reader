import requests
from bs4 import BeautifulSoup



url = 'https://jaomix.ru/ya-korrumpirovannyj-chinovnik-no-oni-govoryat-chto-ya-loyalnyj-ministr/glava-69-krasivyj-muzhchina-vsegda-odinok/'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cache-Control': 'no-cache',
    'Cookie': '_ga=GA1.1.1307277134.1751123287; wordpress_test_cookie=WP%20Cookie%20check; wordpress_logged_in_35981584ee49ee4e18131611545f1192=%D0%9C%D0%B8%D1%85%D0%B0%D0%B8%D0%BB-%D0%A1%D0%BB%D0%B0%D0%B1%D0%B5%D0%BD%D0%BA%D0%BE%7C1752332907%7C2xQZDXmmFpJORtSzvXk0EfUWnDiC45oNPNmkZGgM3FW%7C2bcd4b033f48ca556fb3e514b2f3197b73f4254db8ef371fd230ed309c0cfc50; wpdiscuz_nonce_35981584ee49ee4e18131611545f1192=33d0c50520; nightLight=on; _ga_C7J1M8PT9N=GS2.1.s1751123287$o1$g1$t1751123718$j59$l0$h0',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}

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

        ch_title = soup.find_all("h1", "entry-title")[0].get_text()
        content_txt = ch_title + '\n\n'

        content = soup.find_all("div", "entry-content")[0]
        
        delifex(content, ("div", "adblock-service"))
        delifex(content, ("div", "adfoxblock"))
        delifex(content, ("div", "add-hand-mark"))
        delifex(content, ("div", "clear"))
        delifex(content, ("a",))

        content_txt += ''.join([str(x) for x in content.find_all("div", "entry")[0].contents])
        content_txt = content_txt.replace('<p>', '')
        content_txt = content_txt.replace('</p>', '\n')

        filename = ch_title.replace('\n', ' ').replace('"', '').replace(':', '').replace('/', '').replace('\\', '').replace('?', '').replace('*', '').replace('<', '').replace('>', '').replace('|', '').strip()
        # print(filename)
        with open(f"chapters/{filename}.txt", 'w', encoding='UTF-8') as file:
            file.write(content_txt)
        
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

download_chapter(url, 40)