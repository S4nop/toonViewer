from bs4 import BeautifulSoup
import requests
import urllib.request

from utils.ImageProcessor import ImageProcessor


class Crawler:
    def __init__(self):
        self.__set_opener()

    #정답은 아래에!
    #마지막화의 회차 번호를 크롤링해서 반환하기
    def get_last_epi_no(self, toon_id):
        # -----------------------------여기에 코드를 작성하세요---------------------------------
        toon_main = requests.get("https://comic.naver.com/webtoon/list.nhn?titleId=" + toon_id)
        soup = BeautifulSoup(toon_main.content, "html.parser")
        for i in range(1, 10):
            td = soup.select("table > tr")[i].select_one("a")["href"]
            if td.find('no=') != -1:
                return td.split("no=")[1].split("&")[0]

        # ----------------------------------------------------------------------------------

    #해당하는 회차의 웹툰 이미지들을 모두 받아서 image_urls에 넣기
    def get_toon_images(self, toon_id, epi_no):
        #-----------------------------여기에 코드를 작성하세요---------------------------------
        toon_page = requests.get("https://comic.naver.com/webtoon/detail.nhn?titleId=" + toon_id + "&no=" + str(epi_no))
        soup = BeautifulSoup(toon_page.content, "html.parser")
        image_urls = soup.select(".wt_viewer > img")

        #----------------------------------------------------------------------------------

        img_binaries = [urllib.request.urlopen(image_url["src"]) for image_url in image_urls]
        return ImageProcessor().from_binary_list(img_binaries).process()

    def __set_opener(self):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)