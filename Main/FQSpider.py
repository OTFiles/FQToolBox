import threading
import os
from tqdm import tqdm
import re
from API import book_id_inquire, item_id_inquire

def get_content(title, item_id, name):
    data = item_id_inquire(item_id)
    title = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", title)  # 去掉非法字符
    with open(f'./output/{name}/{title}.txt', mode='w', encoding='utf-8') as f:
        f.write(title)
        f.write('\n')
        f.write(data[0])
        f.write('\n')
        f.close()
    # print(title + '爬取成功')

def crawl_book(book_id, choice, full_crawl_choice=None):
    data = book_id_inquire(book_id)
    item_id_list = data[0]
    title_list = data[1]
    name = data[2]
    author = data[3]
    abstract = data[4]

    if not os.path.exists(f'./output/{name}'):
        os.makedirs(f'./output/{name}')

    if choice == '1':
        if full_crawl_choice == '1':
            threads = []
            for title, item_id in zip(title_list, item_id_list):
                thread = threading.Thread(target=get_content, args=(title, item_id, name))
                threads.append(thread)
            for thread in tqdm(threads):
                thread.start()
            for thread in threads:
                thread.join()

            verify_and_merge(title_list, item_id_list, name, author, abstract)
        elif full_crawl_choice == '2':
            threads_1 = []
            for title, item_id in zip(title_list, item_id_list):
                title = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", title)  # 去掉非法字符
                if os.path.exists(f'./output/{name}/{title}.txt'):
                    print(f"{title}已创建")
                else:
                    print(f'提示:{title}没有被创建')
                    thread = threading.Thread(target=get_content, args=(title, item_id, name))
                    threads_1.append(thread)
            if threads_1:
                for thread in tqdm(threads_1):
                    thread.start()
                for thread in threads_1:
                    thread.join()
    elif choice == '2':
        for r in range(len(title_list)):
            print(f'章节 {r + 1} :{title_list[r]}')
        c1 = int(input('选择:'))
        get_content(title_list[c1 - 1], item_id_list[c1 - 1], name)
    else:
        print('unknown')

def verify_and_merge(title_list, item_id_list, name, author, abstract):
    print('开始效验')
    threads_1 = []
    for title, item_id in zip(title_list, item_id_list):
        title = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", title)  # 去掉非法字符
        if os.path.exists(f'./output/{name}/{title}.txt'):
            pass
        else:
            print(f'提示:{title}没有被创建')
            thread = threading.Thread(target=get_content, args=(title, item_id, name))
            threads_1.append(thread)
    if threads_1:
        for thread in tqdm(threads_1):
            thread.start()
        for thread in threads_1:
            thread.join()
    print('效验完成')

# 删除 show_merge_menu 函数
# def show_merge_menu():
#     choices = ["y. 合并TXT", "n. 不合并TXT"]
#     current_row = 0
#
#     while True:
#         print("\n".join(choices))
#         key = input("选择: ")
#
#         if key == 'y':
#             return 'y'
#         elif key == 'n':
#             return 'n'
