import os
import time
from pyquery import PyQuery as pq
from concurrent.futures import ThreadPoolExecutor, as_completed
import config
import epub

cookies = {'Cookie': 'cookie'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def fetch(title, url, filename):
    print(title, url)
    try:
        page = pq(url=url, headers=headers)
        ele_main = page.find("#content")
        ele_main("script").remove()
        content = ele_main.text(
            squash_space=True, block_symbol='\n', sep_symbol='\n')
        if len(content) < 10:
            print(f'内容不正常: {filename} {url}')
    except Exception as e:
        print(e.__str__)
        exit(-1)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(title)
        f.write("\r\n")
        f.write(content)
    time.sleep(1)


if __name__ == '__main__':
    Host = config.host
    HomeUrl = config.homeUrl
    outputPath = f'output/{config.title}'

    doc = pq(url=f'{Host}{HomeUrl}', headers=headers)
    maintarget = doc.find("div.listmain a")
    index = 1
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    with ThreadPoolExecutor(20) as t:  # 定义1个20的线程池
        future_results = []
        for dd in maintarget.items():
            title = dd.text()
            url = f'{Host}{dd.attr("href")}'
            filename = f'{outputPath}/{index}.txt'
            index += 1
            if os.path.exists(filename):
                continue
            future_results.append(t.submit(fetch, title, url, filename))
       # 等待任务完成并获取结果
        results = []
        for future in as_completed(future_results):
            result = future.result()
            results.append(result)

    print('task complete, start to build epub')
    epub.buildEpub(
        13, index-1, outputPath=f'output/{config.title}', output_file=f'output/{config.title}.epub')
