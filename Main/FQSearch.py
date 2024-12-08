import requests
import json
import curses

def search_books(query, stdscr):
    page = 1
    while True:
        url = f'https://api5-normal-lf.fqnovel.com/reading/bookapi/search/page/v/?query={query}&aid=1967&channel=0&os_version=0&device_type=0&device_platform=0&iid=466614321180296&passback={(page-1)*10}&version_code=999'
        response = requests.get(url=url)
        data = json.loads(response.text)
        
        books = data['data']
        if not books:
            stdscr.clear()
            stdscr.addstr(0, 0, "没有找到相关书籍。")
            stdscr.refresh()
            stdscr.getch()
            break

        current_row = 0
        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()

            for idx, book in enumerate(books):
                book_data = book['book_data'][0]
                book_name = book_data['book_name']
                author = book_data['author']
                abstract = book_data['abstract']
                category = book_data['category']
                score = book_data['score']
                sub_info = book_data['sub_info']

                x = 0
                y = idx
                if idx == current_row:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, x, f"{book_name} - {author}")
                    stdscr.attroff(curses.A_REVERSE)
                    stdscr.addstr(y + 1, x, f"简介: {abstract}")
                    stdscr.addstr(y + 2, x, f"类型: {category}")
                    stdscr.addstr(y + 3, x, f"分数: {score}")
                    stdscr.addstr(y + 4, x, f"Sub_info: {sub_info}")
                else:
                    stdscr.addstr(y, x, f"{book_name} - {author}")

            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(books) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                # 执行函数a
                book_id = books[current_row]['book_data'][0]['book_id']
                stdscr.clear()
                stdscr.addstr(0, 0, f"你选择了: {books[current_row]['book_data'][0]['book_name']}")
                stdscr.addstr(1, 0, f"执行函数a，book_id: {book_id}")
                stdscr.refresh()
                stdscr.getch()
                # 这里可以调用函数a(book_id)

            elif key == ord('q'):
                return

        stdscr.clear()
        stdscr.addstr(0, 0, 'page(不输入退出):')
        stdscr.refresh()
        curses.echo()  # 启用输入回显
        p = stdscr.getstr(1, 0).decode('utf-8')  # 获取用户输入
        curses.noecho()  # 禁用输入回显
        if p == '':
            break
        else:
            page = int(p)

def main(stdscr):
    curses.curs_set(0)  # 隐藏光标
    stdscr.clear()
    stdscr.addstr(0, 0, '搜索内容:')
    stdscr.refresh()
    curses.echo()  # 启用输入回显
    query = stdscr.getstr(1, 0).decode('utf-8')  # 获取用户输入
    curses.noecho()  # 禁用输入回显
    search_books(query, stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
