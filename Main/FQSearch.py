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

                x = 0
                y = idx
                if idx == current_row:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, x, f"{book_name} - {author}")
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, f"{book_name} - {author}")

            stdscr.addstr(len(books) + 1, 0, f"当前页: {page}  (按 'n' 下一页, 'p' 上一页, 'q' 退出)")
            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(books) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                # 显示书本详情
                book_data = books[current_row]['book_data'][0]
                book_name = book_data['book_name']
                author = book_data['author']
                abstract = book_data['abstract']
                category = book_data['category']
                score = book_data['score']
                sub_info = book_data['sub_info']

                stdscr.clear()
                stdscr.addstr(0, 0, f"书名: {book_name}")
                stdscr.addstr(1, 0, f"作者: {author}")
                stdscr.addstr(2, 0, f"类型: {category}")
                stdscr.addstr(3, 0, f"分数: {score}")
                stdscr.addstr(4, 0, f"Sub_info: {sub_info}")

                # 自动换行简介
                stdscr.addstr(5, 0, "简介:")
                abstract_lines = wrap_text(abstract, w)
                for i, line in enumerate(abstract_lines):
                    stdscr.addstr(6 + i, 0, line)

                stdscr.refresh()
                stdscr.getch()

            elif key == ord('q'):
                return
            elif key == ord('n'):  # 下一页
                page += 1
                break
            elif key == ord('p') and page > 1:  # 上一页
                page -= 1
                break

def wrap_text(text, width):
    """自动换行文本"""
    lines = []
    while len(text) > width:
        line = text[:width]
        first_newline = line.find('\n')
        if first_newline != -1:
            lines.append(line[:first_newline])
            text = text[first_newline + 1:]
        else:
            lines.append(line)
            text = text[width:]
    lines.append(text)
    return lines

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
