import requests
import json
import time

def book_id_inquire(book_id):
    """
    获取指定书籍ID的书籍信息，包括章节标题列表等。
    
    :param book_id: 书籍ID
    :return: 包含章节ID列表、章节标题列表、书籍名称、作者、简介、标签、评分、字数、阅读次数、创作状态和缩略图URL的元组
    """
    book_info_url = f'https://api5-normal-sinfonlinec.fqnovel.com/reading/user/share/info/v/?group_id={book_id}&aid=1967&version_code=513'
    chapter_list_url = f'https://fanqienovel.com/api/reader/directory/detail?bookId={book_id}'
    
    book_info_response = requests.get(url=book_info_url).text
    chapter_list_response = requests.get(url=chapter_list_url).text
    
    book_info_data = json.loads(book_info_response)
    chapter_list_data = json.loads(chapter_list_response)
    
    title_list = []
    for volume in chapter_list_data['data']['chapterListWithVolume']:
        for chapter in volume:
            title_list.append(chapter['title'])
    
    item_id_list = chapter_list_data['data']['allItemIds']
    book_name = book_info_data['data']['book_info']['book_name']
    author = book_info_data['data']['book_info']['author']
    abstract = book_info_data['data']['book_info']['abstract']
    tags = book_info_data['data']['book_info']['tags']
    score = book_info_data['data']['book_info']['score']
    word_number = book_info_data['data']['book_info']['word_number']
    read_count = book_info_data['data']['book_info']['read_count']
    creation_status = book_info_data['data']['book_info']['creation_status']
    thumb_url = book_info_data['data']['book_info']['thumb_url']
    
    if creation_status == '0':
        print('状态:完结')
    elif creation_status == '1':
        print('状态:连载')
    elif creation_status == '4':
        print('状态:断更')
    else:
        print(creation_status)
    
    return item_id_list, title_list, book_name, author, abstract, tags, score, word_number, read_count, creation_status, thumb_url

def item_id_inquire(item_id):
    """
    获取指定章节ID的章节内容。
    
    :param item_id: 章节ID
    :return: 包含章节内容、章节标题、作者、书籍ID、书籍名称、下一章节ID和上一章节ID的元组
    """
    chapter_content_url = f'https://novel.snssdk.com/api/novel/reader/full/v1/?item_id={item_id}'
    chapter_content_response = requests.get(url=chapter_content_url).text
    chapter_content_data = json.loads(chapter_content_response)

    # 处理章节内容中的HTML标签
    content = chapter_content_data['data']['content'].replace('</p><p>', '\n').replace('</p>', '\n').replace('<p>', '\n')
    title = chapter_content_data['data']['novel_data']['title']
    author = chapter_content_data['data']['novel_data']['author']
    book_id = chapter_content_data['data']['novel_data']['book_id']
    book_name = chapter_content_data['data']['novel_data']['book_name']
    next_item_id = chapter_content_data['data']['novel_data']['next_item_id']
    pre_item_id = chapter_content_data['data']['novel_data']['pre_item_id']
    
    return content, title, author, book_id, book_name, next_item_id, pre_item_id

def user_inquire(cookie):
    """
    根据用户cookie获取用户信息。
    
    :param cookie: 用户cookie
    :return: 包含用户名、用户头像URL、用户ID和用户描述的元组，如果cookie无效则返回'false'
    """
    user_info_url = 'https://fanqienovel.com/api/user/info/v2'
    headers = {'Cookie': cookie}
    user_info_response = requests.get(url=user_info_url, headers=headers).text
    user_info_data = json.loads(user_info_response)

    if user_info_data['code'] == -1:
        return 'false'
    else:
        user_avatar_url = user_info_data['data']['avatar']
        user_name = user_info_data['data']['name']
        user_id = user_info_data['data']['id']
        user_desc = user_info_data['data']['desc']
        return user_name, user_avatar_url, user_id, user_desc

def user_bookshelf(cookie):
    """
    根据用户cookie获取用户书架上的书籍信息。
    
    :param cookie: 用户cookie
    :return: 包含书籍ID列表、章节ID列表和阅读时间戳列表的元组
    """
    bookshelf_url = 'https://fanqienovel.com/api/reader/book/progress'
    book_detail_url = 'https://api5-normal-sinfonlineb.fqnovel.com/reading/bookapi/multi-detail/v/?aid=1967&iid=1&version_code=999&book_id='

    headers = {'Cookie': cookie}
    bookshelf_response = requests.get(url=bookshelf_url, headers=headers).text
    bookshelf_data = json.loads(bookshelf_response)

    book_id_list = []
    item_id_list = []
    read_timestamp_list = []
    for book in bookshelf_data['data']:
        book_id_list.append(book['book_id'])
        item_id_list.append(book['item_id'])
        read_timestamp_list.append(book['read_timestamp'])

    return book_id_list, item_id_list, read_timestamp_list

def update_progres(cookie, item_id):
    """
    更新用户的阅读进度。
    
    :param cookie: 用户cookie
    :param item_id: 章节ID
    """
    chapter_content_url = f'https://novel.snssdk.com/api/novel/reader/full/v1/?item_id={item_id}'
    reading_progress_url = 'https://fanqienovel.com/api/reader/book/update_progress'
    
    chapter_content_response = requests.get(url=chapter_content_url).text
    chapter_content_data = json.loads(chapter_content_response)
    book_id = chapter_content_data['data']['novel_data']['book_id']

    headers = {'Cookie': cookie}
    update_payload = {
        "book_id": book_id,
        "item_id": item_id,
        "read_progress": 0,
        "index": 4,
        "read_timestamp": int(time.time()),
        "genre_type": 0
    }

    update_response = requests.post(url=reading_progress_url, headers=headers, json=update_payload).text
    print(update_response)

def add_bookshelf(cookie, book_id):
    """
    根据书籍ID将书籍添加到用户的书架。
    
    :param cookie: 用户cookie
    :param book_id: 书籍ID
    """
    book_detail_url = 'https://fanqienovel.com/api/book/simple/info'
    user_bookshelf_url = 'https://fanqienovel.com/api/reader/book/progress'
    
    headers = {'Cookie': cookie}
    user_bookshelf_response = requests.get(url=user_bookshelf_url, headers=headers).text
    user_bookshelf_data = json.loads(user_bookshelf_response)

    # 获取已有的书籍ID列表
    existing_book_ids = [book['book_id'] for book in user_bookshelf_data['data']]

    # 添加新的书籍ID
    if book_id not in existing_book_ids:
        existing_book_ids.append(book_id)
    
    add_book_payload = {"book_ids": existing_book_ids}
    add_book_response = requests.post(url=book_detail_url, headers=headers, data=json.dumps(add_book_payload)).text
    print(add_book_response)

def paragraph_comments(item_id, paragraph_index):
    """
    获取指定章节指定段落的评论。
    
    :param item_id: 章节ID
    :param paragraph_index: 段落索引
    :return: 包含用户名和评论内容的字典
    """
    chapter_content_url = f'https://novel.snssdk.com/api/novel/reader/full/v1/?item_id={item_id}'
    paragraph_comments_url = f"https://api5-normal-sinfonlinec.fqnovel.com/reading/ugc/idea/comment_list/v/?item_version=3add812e2984c508c71ce1361c31cf5f_1_v5&item_id={item_id}&para_index={paragraph_index}&book_id={json.loads(requests.get(url=chapter_content_url).text)['data']['novel_data']['book_id']}&aid=1967&version_code=513"
    
    paragraph_comments_response = requests.get(url=paragraph_comments_url).text
    paragraph_comments_data = json.loads(paragraph_comments_response)

    comments_dict = {}
    for comment in paragraph_comments_data['data']['comments']:
        comments_dict[comment['user_info']['user_name']] = comment['text']
    
    return comments_dict

def book_comments(book_id):
    """
    获取指定书籍ID的评论。
    
    :param book_id: 书籍ID
    :return: 包含用户名和评论内容的字典
    """
    book_comments_url = f"https://api5-normal-sinfonlinec.fqnovel.com/reading/ugc/novel_comment/book/v/?&book_id={book_id}&aid=1967&version_code=513"

    headers = {
        "X-Argus": "2DhmtvR3uHS92+jiPSDiYpHKrADwLYuLOuGVmZZGzZQeFwLkCbSb+J3TLiIwUlbaKG6NMydM7LCm5EwzMmK0sJSQh2uoxdwTXSpOSk0U+na16DbbxUaHw0N+ylcp81dhOSfGd4foaifno6KBCahJtNKb0OpMYqpvguhVlXDhKdGPr21vBEcv63xMzvXJTwsxDb/9gaDl1cDEZWqK2Pl3xmabBKQb+koFFZeD01LY0YSmLKJuHHOEdAvQj1Mz2nUiSiKTyk8TivHxlS+3AdQWp3GG"
    }
    
    book_comments_response = requests.get(url=book_comments_url, headers=headers).text
    book_comments_data = json.loads(book_comments_response)

    comments_dict = {}
    for comment in book_comments_data['data']['comment']:
        comments_dict[comment['user_info']['user_name']] = comment['text']

    return comments_dict

def recommended_list():
    """
    获取推荐书籍列表。
    
    :return: 包含书籍ID、书籍名称、简介、作者、创建时间、阅读次数和评分的字典列表
    """
    recommended_books_url = "https://api5-normal-sinfonlinec.fqnovel.com/reading/bookapi/bookmall/tab/v/?aid=1967"
    recommended_books_response = requests.get(url=recommended_books_url).text
    recommended_books_data = json.loads(recommended_books_response)

    recommended_books_list = []
    for book in recommended_books_data['data']['tab_item'][0]['cell_data'][0]['cell_data'][0]['book_data']:
        book_info = {
            'book_id': book['book_id'],
            'book_name': book['book_name'],
            'abstract': book['abstract'],
            'author': book['author'],
            'create_time': book['create_time'],
            'read_count': book['read_count'],
            'score': book['score']
        }
        recommended_books_list.append(book_info)

    return recommended_books_list
