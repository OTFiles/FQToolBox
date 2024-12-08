import threading
import os
from tqdm import tqdm
import re
from API import book_id_inquire, item_id_inquire

def get_content(title, item_id):
    data = item_id_inquire(item_id)
    title = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", title)  # 去掉非法字符
    with open(f'./output/{name}/{title}.txt', mode='w', encoding='utf-8') as f:
        f.write(title)
        f.write('\n')
        f.write(data[0])
        f.write('\n')
        f.close()
    # print(title + '爬取成功')

def crawl_book(book_id):
    data = book_id_inquire(book_id)
    item_id_list = data[0]
    title_list = data[1]
    name = data[2]
    author = data[3]
    abstract = data[4]

    if not os.path.exists(f'./output/{name}'):
        os.makedirs(f'./output/{name}')

    c = input('1.爬取全文\n2.爬取单章\nNext:')
    if c == '1':
        c1 = input('1.全文爬取\n2.更新爬取(只会爬取未爬取的章节):')
        if c1 == '1':
            threads = []
            for title, item_id in zip(title_list, item_id_list):
                thread = threading.Thread(target=get_content, args=(title, item_id))
                threads.append(thread)
            for thread in tqdm(threads):
                thread.start()
            for thread in threads:
                thread.join()

            print('开始效验')
            threads_1 = []
            for title, item_id in zip(title_list, item_id_list):
                title = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", title)  # 去掉非法字符
                if os.path.exists(f'./output/{name}/{title}.txt'):
                    pass
                else:
                    print(f'提示:{title}没有被创建')
                    thread = threading.Thread(target=get_content, args=(title, item_id))
                    threads_1.append(thread)
            if threads_1:
                for thread in tqdm(threads_1):
                    thread.start()
                for thread in threads_1:
                    thread.join()
            print('效验完成')

            if input('是否合并TXT?(y/n):') == 'y':
                content = ""
                for title in title_list:
                    title = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", title)  # 去掉非法字符
                    txt_file = f'./output/{name}.txt'
                    with open(txt_file, 'w', encoding='utf-8') as files:
                        files.write(f'书名:{name}\n')
                        files.write(f'作者:{author}\n')
                        files.write(f'简介:{abstract}\n——————————————\n')
                        with open(f'./output/{name}/{title}.txt', 'r', encoding='utf-8') as file:
                            content += file.read()
                            file.close()
                        files.write(content)
                        files.close()
                print(f'合并完成,已添加到{txt_file}')
        elif c1 == '2':
            threads_1 = []
            for title, item_id in zip(title_list, item_id_list):
                title = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", title)  # 去掉非法字符
                if os.path.exists(f'./output/{name}/{title}.txt'):
                    print(f"{title}已创建")
                else:
                    print(f'提示:{title}没有被创建')
                    thread = threading.Thread(target=get_content, args=(title, item_id))
                    threads_1.append(thread)
            if threads_1:
                for thread in tqdm(threads_1):
                    thread.start()
                for thread in threads_1:
                    thread.join()
    elif c == '2':
        for r in range(len(title_list)):
            print(f'章节 {r + 1} :{title_list[r]}')
        c1 = int(input('选择:'))
        get_content(title_list[c1 - 1], item_id_list[c1 - 1])
    else:
        print('unknown')

# 示例调用
if __name__ == "__main__":
    book_id = input('book_id:')
    crawl_book(book_id)
