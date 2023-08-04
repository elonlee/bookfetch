# coding=utf-8

from ebooklib import epub
import os

index = 13
index_end = 123
output_file = f'output/output.epub'

if __name__ == '__main__':
    book = epub.EpubBook()

    # add metadata
    book.set_identifier('sample123456')
    book.set_title('测试名字')
    book.set_language('zh-cn')

    book.add_author('测试作者')
    
    # add cover image
    # book.set_cover("image.jpg", open('cover.jpg', 'rb').read())

    # intro chapter
    c1 = epub.EpubHtml(title='Introduction', file_name='intro.xhtml', lang='zh')
    c1.content=u'<html><head></head><body><h1>Introduction</h1><p>Introduction paragraph where i explain what is happening.</p></body></html>'

    # defube style
    style = '''BODY { text-align: justify;}'''
    default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css", content=style)
    book.add_item(default_css)
    # define css style
    style = '''
@namespace epub "http://www.idpf.org/2007/ops";

body {
    font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
}

h2 {
     text-align: left;
     text-transform: uppercase;
     font-weight: 200;     
}

ol {
        list-style-type: none;
}

ol > li:first-child {
        margin-top: 0.3em;
}


nav[epub|type~='toc'] > ol > li > ol  {
    list-style-type:square;
}


nav[epub|type~='toc'] > ol > li > ol > li {
        margin-top: 0.3em;
}

'''

    # add css file
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    # add chapters to the book
    book.add_item(c1)
    chapters = []
    for i in range(index, index_end+1):
        src = f'output/{i}.txt'
        print(src)
        with open(src, 'r', encoding='utf-8') as fsrc:
            title = fsrc.readline()
            content = fsrc.read(-1)
            print(f'title={title}')
        # chapter
        ch = epub.EpubHtml(title=title, file_name=f'ch_{i}.xhtml')
        ch.content=f'<h1>{title}</h1><p>{content}</p>'
        ch.add_item(default_css)

        book.add_item(ch)
        chapters.append(ch)
    
    # create table of contents
    # - add manual link
    # - add section
    # - add auto created links to chapters

    book.toc = (epub.Link('intro.xhtml', '前言', 'intro'),
                (epub.Section('正文'), tuple(chapters))
                )

    # add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())


    
    # create spin, add cover page as first page
    # book.spine = ['cover', 'nav'] + chapters
    book.spine = ['nav'] + chapters

    # create epub file
    if not os.path.exists("output"):
        os.mkdir("output")
    epub.write_epub(output_file, book, {})



