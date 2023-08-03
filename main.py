import os
import time
from pyquery import PyQuery as pq

Host = "https://domain.domain"
HomeUrl = "/xxxx/xxxxx"

doc = pq(url=f'{Host}{HomeUrl}')

maintarget = doc.find("div.listmain a")

index = 1
if not os.path.exists("output"):
    os.mkdir("output")
for dd in maintarget.items():
    title = dd.text()
    url = dd.attr("href")
    print(url)
    filename = f'output/{index}.txt'
    index += 1
    if os.path.exists(filename):
        continue
    page = pq(url=f'{Host}{url}')
    ele_main = page.find("#content")
    ele_main("script").remove()
    content = ele_main.text(
        squash_space=True, block_symbol='\n', sep_symbol='\n')
    with open(filename, "w", encoding="utf-8") as f:
        f.write(title)
        f.write("\r\n")
        f.write(content)
    time.sleep(3)
