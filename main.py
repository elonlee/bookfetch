import os
import time
from pyquery import PyQuery as pq
from concurrent.futures import ThreadPoolExecutor

cookies = {'Cookie':'cookie'}
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
Host = "https://domain.domain"
HomeUrl = "/xxxx/xxxxx"





def fetch(title, url, filename):
    print(url)
    page = pq(url=f'{Host}{url}',headers=headers)
    ele_main = page.find("#content")
    ele_main("script").remove()
    content = ele_main.text(
        squash_space=True, block_symbol='\n', sep_symbol='\n')
    with open(filename, "w", encoding="utf-8") as f:
        f.write(title)
        f.write("\r\n")
        f.write(content)
    time.sleep(3)


if __name__ == '__main__':
    doc = pq(url=f'{Host}{HomeUrl}',headers=headers)

    maintarget = doc.find("div.listmain a")

    index = 1
    if not os.path.exists("output"):
        os.mkdir("output")

    with ThreadPoolExecutor(8) as t:   #定义1个20的线程池
        for dd in maintarget.items():
            title = dd.text()
            url = dd.attr("href")
            filename = f'output/{index}.txt'
            index += 1
            if os.path.exists(filename):
                continue
            t.submit(fetch, title, url, filename)

