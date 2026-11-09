from bs4 import BeautifulSoup
import re

MAX_CHAR_COUNT_BOOKMARKS = 105

#identify all offending bookmark elements and curtail their text content
def fix_bookmarks(soup):
    bookmarks = soup.find_all('div', class_=['bookmark-title', 'bookmark-description', 'bookmark-href'])
    for bookmark in bookmarks:
        for text in bookmark.stripped_strings:
            if len(text) > MAX_CHAR_COUNT_BOOKMARKS:
                bookmark.contents.remove(text)
                bookmark.insert(1, soup.new_string(text[0:MAX_CHAR_COUNT_BOOKMARKS]+'...'))

#add style formatting which will wrap text content in 'code' tags
def fix_code_snippets(soup):
    code_elements = soup.find_all('code')
    for code_element in code_elements:
        code_element['style'] = "white-space:pre-wrap;word-break:break-all"

#replace the lame clickable link with an actual embedded YouTube video
def fix_youtube_links(soup):
    youtube_regex = r'^(https?:\/\/)?(www\.)?((youtube\.com\/(?:watch\?v=|embed\/|v\/|playlist\?list=)|youtu\.be\/))([a-zA-Z0-9_-]{11}|\w+(\.\w+)+)$'
    youtube_links = soup.find_all('div', class_="source")
    for youtube_link in youtube_links:
        if re.match(youtube_regex, youtube_link.string):
            embeded_element = soup.new_tag('center')
            embed_url = youtube_link.string.replace('watch?v=', 'embed/')
            iframe = BeautifulSoup("<iframe width='700' height='400' src='{0}' title='YouTube video player' frameborder='0' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share' referrerpolicy='strict-origin-when-cross-origin' allowfullscreen></iframe><figcaption></figcaption>".format(embed_url), features="html.parser")
            embeded_element.append(iframe)
            youtube_link.replace_with(embeded_element)


filename = input('Name of your Notion HTML file: ')
f = open(filename, 'r')
html = f.read()
f.close()

soup = BeautifulSoup(html, features="html.parser")


fix_bookmarks(soup)
fix_code_snippets(soup)
fix_youtube_links(soup)


newfilename = filename.replace('.html','')+'-fixed.html'

f = open(newfilename, 'w')
f.write(str(soup))
f.close()

print('Fixed file created: ' + newfilename)
