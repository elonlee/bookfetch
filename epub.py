# coding=utf-8

from ebooklib import epub
import os
import config


def buildEpub(index, index_end, outputPath, output_file):
    print(
        f'starting to build epub: index:{index}, index_end:{index_end},output:{output_file}')
    book = epub.EpubBook()

    # add metadata
    book.set_title(config.title)
    book.add_author(config.author)
    book.set_identifier(config.identifier)
    book.set_language(config.language)

    # default style
    style = '''BODY { text-align: justify;}
h2 {
  display: block;
  background-color: #C1CCC0;
  font-size: 1.25em;
  font-weight: bold;
  line-height: 1.2;
  margin: 0.67em 0;
  padding: 5px 5px;
  text-align: center
}'''
    default_css = epub.EpubItem(
        uid="style_default", file_name="style/default.css", media_type="text/css", content=style)
    book.add_item(default_css)
    # define css style
    style = '''
@namespace epub "http://www.idpf.org/2007/ops";

body {
}
.cover {
	/*width:100%;*/
	height:100%;
	text-align:center;
	padding:0px;
}
/*扉页*/
.titlepages {
	text-align: center;
	line-height:100%;
}
.booktitle,.bookname {
	margin-top:38.2%;
	line-height:100%;
	text-align: center;
	font-weight:bold;
	font-size:xx-large;
	font-family: "h1","微软雅黑","黑体","zw",sans-serif;
}
.bookauthor {
	margin-top:2em;
	font-family:"kt","楷体","楷体_gb2312","zw",serif;
	text-align: center;
}
hr.titlepage {
	height: 50px;
	width:100%;
	border-style: none none dotted none;
	border-width: 0px 0px 1px 0px;
	border-color: blue yellow;
}
ol {  list-style-type: none;}
ol > li:first-child { margin-top: 0.3em;}
nav[epub|type~='toc'] > ol > li > ol  { list-style-type:square; }
nav[epub|type~='toc'] > ol > li > ol > li { margin-top: 0.3em;}

'''
    # add css file
    nav_css = epub.EpubItem(
        uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    # add cover image
    if config.cover != "":
        book.set_cover("image.jpg", open(config.cover, 'rb').read())

    # add navigation files
    book.add_item(epub.EpubNcx())
    if config.nav:
        nav = epub.EpubNav()
        nav.add_item(nav_css)
        book.add_item(nav)

    chapters = []
    # intro chapter
    title_html = epub.EpubHtml(title='标题', file_name="title_page.xhtml",
                               content=f'''<html><body>
                               <div class="titlepages">
                               <p class="booktitle">{config.title}</p>
                               <p class="bookauthor"> {config.author}  著</p>
                               <hr class="titlepage" />
                               ''')
    if config.intro != "":
        title_html.content += f'<p>{config.intro}</p>'
    title_html.content += '</div></body></html>'
    title_html.add_item(nav_css)
    book.add_item(title_html)
    chapters.append(title_html)
    # add chapters to the book
    for i in range(index, index_end+1):
        src = f'{outputPath}/{i}.txt'
        if not os.path.exists(src):
            print(f'{src} is not found')
            continue
        with open(src, 'r', encoding='utf-8') as fsrc:
            title = fsrc.readline()
            content = ""
            for line in fsrc.readlines():
                line = line.strip()
                if len(line) > 0:
                    content += f'<p>{line}</p>'
        # chapter
        ch = epub.EpubHtml(title=title, file_name=f'ch_{i}.xhtml')
        ch.content = f'<h2>{title}</h2><div>{content}</div>'
        ch.add_item(default_css)
        book.add_item(ch)
        chapters.append(ch)

    # create table of contents
    # - add manual link
    # - add section
    # - add auto created links to chapters
    book.toc = [] + chapters

    # create spin, add cover page as first page
    spine = []
    if config.cover != "":
        spine.append('cover')
    if config.nav:
        spine.append('nav')
    book.spine = spine + chapters
    # book.spine = ['nav'] + chapters
    book.guide = [
        {"type": "cover", "title": "封面", "href": "cover.xhtml"},
        # {"type": "toc", "title": "Table of Contents", "href": "nav.xhtml"},
        {"type": "text", "title": "开始", "href": f'ch_{index}.xhtml'},
        {"type": "title-page", "title": "title-page", "href": 'title_page.xhtml'},
    ]
    # create epub file
    if not os.path.exists("output"):
        os.mkdir("output")
    epub.write_epub(output_file, book, {'epub3_landmark': False})


if __name__ == '__main__':
    index = 13
    index_end = 15
    outputPath = f'output/{config.title}'
    output_file = f'output/{config.title}.epub'
    buildEpub(index, index_end, outputPath, output_file)
