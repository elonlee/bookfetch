# coding=utf-8

from ebooklib import epub
import os
import epubconfig as config

index = 13
index_end = 1052
output_file = f'output/output.epub'

if __name__ == '__main__':
    book = epub.EpubBook()

    # add metadata
    book.set_title(config.title)
    book.add_author(config.author)
    book.set_identifier(config.identifier)
    book.set_language(config.language)

    # add cover image
    if config.cover != "":
        book.set_cover("image.jpg", open(config.cover, 'rb').read())

    # intro chapter
    if config.intro != "":
        c1 = epub.EpubHtml(title='Introduction',
                           file_name='intro.xhtml', lang='zh')
        c1.content = f'<html><head></head><body><h1>前言</h1><p>{config.intro}</p></body></html>'
        book.add_item(c1)

    # defube style
    style = '''BODY { text-align: justify;}'''
    default_css = epub.EpubItem(
        uid="style_default", file_name="style/default.css", media_type="text/css", content=style)
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
    nav_css = epub.EpubItem(
        uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    # add chapters to the book

    chapters = []
    for i in range(index, index_end+1):
        src = f'output/{i}.txt'
        print(src)
        with open(src, 'r', encoding='utf-8') as fsrc:
            title = fsrc.readline()
            content = ""
            for line in fsrc.readlines():
                line = line.strip()
                if len(line) > 0:
                    content += f'<p>{line}</p>'
            print(f'title={title}')
        # chapter
        ch = epub.EpubHtml(title=title, file_name=f'ch_{i}.xhtml')
        ch.content = f'<h1>{title}</h1><div>{content}</div>'
        ch.add_item(default_css)

        book.add_item(ch)
        chapters.append(ch)

    # create table of contents
    # - add manual link
    # - add section
    # - add auto created links to chapters
    book.toc = []
    if config.intro != "":
        book.toc += [epub.Link('intro.xhtml', '前言', 'intro')]
    book.toc += chapters

    # add navigation files
    book.add_item(epub.EpubNcx())
    nav = epub.EpubNav()
    nav.add_item(nav_css)
    book.add_item(nav)

    # create spin, add cover page as first page
    if config.cover != "":
        book.spine = ['cover', 'nav'] + chapters
    else:
        book.spine = ['nav'] + chapters
    # book.spine = ['nav'] + chapters

    # create epub file
    if not os.path.exists("output"):
        os.mkdir("output")
    epub.write_epub(output_file, book, {})
