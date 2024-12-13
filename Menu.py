import os
import json
import requests
import curses
from Main.API import user_inquire
from Main.FQRead import main as fqread_main

def show_menu(stdscr):
    curses.curs_set(0)  # 隐藏光标
    menu_items = [
        "1. 搜索书籍",
        "2. 阅读书籍",
        "3. 爬取书籍",
        "4. 推荐榜",
        "5. 设置",
        "6. DEBUG",
        "q. 退出"
    ]
    current_row = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        for idx, item in enumerate(menu_items):
            x = w // 2 - len(item) // 2
            y = h // 2 - len(menu_items) // 2 + idx
            if idx == current_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, item)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            choice = menu_items[current_row].split('.')[0]
            if choice == 'q':
                break
            elif choice == '1':
                # 调用 FQSearch.py 并保持 curses 状态
                curses.def_prog_mode()  # 保存当前 curses 状态
                os.system('python ./Main/FQSearch.py')
                curses.reset_prog_mode()  # 恢复 curses 状态
                stdscr.clear()
                stdscr.refresh()
            elif choice == '2':
                fqread_main(stdscr)  # 传递stdscr对象到FQRead.py
            elif choice == '3':
                os.system('python ./Main/FQSpider.py')
            elif choice == '4':
                os.system('python ./Main/FQ推荐.py')
            elif choice == '5':
                set_cookie(stdscr)
            elif choice == '6':
                debug_menu(stdscr)

def set_cookie(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, '设置Cookie')
    stdscr.addstr(1, 0, '1. 设置Cookie')
    stdscr.refresh()
    curses.echo()
    choice = stdscr.getstr(2, 0).decode('utf-8')
    curses.noecho()

    if choice == '1':
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, 'Cookie:')
            stdscr.refresh()
            curses.echo()
            cookie = stdscr.getstr(1, 0).decode('utf-8')
            curses.noecho()

            data = user_inquire(cookie)
            if data == 'false':
                stdscr.clear()
                stdscr.addstr(0, 0, 'Cookie无效,请重新设置')
                stdscr.refresh()
                stdscr.getch()
            else:
                with open('cookie.ini', 'w', encoding='utf-8') as f:
                    f.write(cookie)
                stdscr.clear()
                stdscr.addstr(0, 0, f'用户名称:{data[0]}')
                stdscr.addstr(1, 0, f'用户头像URL:{data[1]}')
                stdscr.addstr(2, 0, f'用户id:{data[2]}')
                stdscr.addstr(3, 0, f'用户简介:{data[3]}')
                stdscr.refresh()
                stdscr.getch()
                break

def debug_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, 'DEBUG菜单')
    stdscr.addstr(1, 0, '1. api测试')
    stdscr.addstr(2, 0, '2. 番茄听书')
    stdscr.refresh()
    curses.echo()
    choice = stdscr.getstr(3, 0).decode('utf-8')
    curses.noecho()

    if choice == '1':
        os.system('python ./Main/Test.py')
    elif choice == '2':
        os.system('python ./Main/Test2.py')

def main(stdscr):
    # 初始化
    curses.curs_set(0)  # 隐藏光标
    stdscr.clear()
    stdscr.addstr(0, 0, '欢迎使用')
    stdscr.addstr(1, 0, '一言:' + json.loads(requests.get(url='https://v1.hitokoto.cn').text)['hitokoto'])
    stdscr.addstr(2, 0, '---------------')
    stdscr.refresh()

    if not os.path.exists('cookie.ini'):
        with open('cookie.ini', 'w', encoding='utf-8') as ce:
            ce.close()

    with open('cookie.ini', 'r', encoding='utf-8') as data:
        login_data = user_inquire(data.read())
        if login_data == 'false':
            stdscr.addstr(3, 0, '登录失败,部分功能无法使用，请配置cookie')
        else:
            stdscr.addstr(3, 0, f'用户名称:{login_data[0]}')
            stdscr.addstr(4, 0, f'用户头像URL:{login_data[1]}')
            stdscr.addstr(5, 0, f'用户id:{login_data[2]}')
            stdscr.addstr(6, 0, f'用户简介:{login_data[3]}')
        stdscr.addstr(7, 0, '---------------')
        stdscr.refresh()

    show_menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
