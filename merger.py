import os
from config import ORDER_FILE, METADATA_FILE


XML_TEMPLATE = None
with open('templates/book.xml', 'r') as file:
    XML_TEMPLATE = file.read()


# -- Chapter-merging methods -- #
def simple_walk():
    body = ""
    with os.scandir('chapters/') as directory:
        for dir_entry in directory:
            if not dir_entry.is_file():
                continue
            if not dir_entry.name.split('.')[-1] == 'xml':
                continue

            with open(dir_entry, 'r', encoding='utf-8') as file:
                body += file.read()
    
    return body

def order_walk():
    chapters_list = None
    with open(f'chapters/{ORDER_FILE}', 'r', encoding='utf-8') as order_file:
        chapters_list = order_file.readlines()

    body = ""
    for chapter in chapters_list:
        chapter_filename = chapter.strip('\n').strip() + '.xml'
        with open(f'chapters/{chapter_filename}', 'r', encoding='utf-8') as file:
            body += file.read()

    return body


# -- Reading metadata -- #
with open(METADATA_FILE, 'r', encoding='utf-8') as file:
    metadata = file.readlines()


# -- Forming final xml -- #
body = order_walk()  # change to simple_walk() if desired
book_title = metadata[0]
date = metadata[1]
annotation = metadata[2]

content = XML_TEMPLATE.replace('Chapters', body)
content = content.replace('BookTitle', book_title)
content = content.replace('Date', date)
content = content.replace('Annotation', annotation)

with open('book.fb2', 'w', encoding='utf-8') as file:
    file.write(content)