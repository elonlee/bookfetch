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

    chapters = []
    # intro chapter
    if config.intro != "":
        c1 = epub.EpubHtml(title='前言', file_name='intro.xhtml', lang='zh')
        c1.content = f'<html><head></head><body><h1>前言</h1><p>{config.intro}</p></body></html>'
        book.add_item(c1)
        chapters.append(c1)

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
        ch.content = f'<h1>{title}</h1><div>{content}</div>'
        ch.add_item(default_css)
        book.add_item(ch)
        chapters.append(ch)

    # create table of contents
    # - add manual link
    # - add section
    # - add auto created links to chapters
    book.toc = [epub.Link('intro.xhtml', '前言', 'intro')] + chapters

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


if __name__ == '__main__':
    index = 13
    index_end = 575
    outputPath = f'output/{config.title}'
    output_file = f'output/{config.title}.epub'
    buildEpub(index, index_end, outputPath, output_file)
