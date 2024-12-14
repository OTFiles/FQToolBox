import os
import json
import requests
import curses
from Main.API import user_inquire
from Main.FQRead import main as fqread_main

def show_menu(stdscr, menu_items, init_messages_count):
    curses.curs_set(0)  # 隐藏光标
    current_row = init_messages_count  # 设置起始行在菜单选项开始的地方

    max_len = max(len(item) for item in menu_items)  # 计算最长的菜单项长度

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        for idx, item in enumerate(menu_items):
            x = w // 2 - max_len // 2  # 使用最长长度来计算 x 坐标
            y = h // 2 - (len(menu_items) - init_messages_count) // 2 + idx  # 计算 y 坐标，使菜单选项居中
            if idx == current_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, item)

        stdscr.refresh()  # 修正这里

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > init_messages_count:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            choice = menu_items[current_row].split('.')[0]
            if choice == 'q':
                try:
                    curses.endwin()  # 确保在退出时结束 curses 模式
                except curses.error as e:
                    stdscr.addstr(0, 0, f'错误: {e}')
                    stdscr.refresh()
                    stdscr.getch()
                finally:
                    os.system('stty sane')  # 恢复终端设置
                break
            elif choice == '1':
                curses.def_prog_mode()  # 保存当前 curses 状态
                os.system('python ./Main/FQSearch.py')
                curses.reset_prog_mode()  # 恢复 curses 状态
                stdscr.refresh()  # 修正这里
            elif choice == '2':
                fqread_main(stdscr)  # 传递stdscr对象到FQRead.py
            elif choice == '3':
                os.system('python ./Main/FQSpider.py')
            elif choice == '4':
                os.system('python ./Main/FQ推荐.py')
            elif choice == '5':
                set_cookie(stdscr, menu_items, init_messages_count)
            elif choice == '6':
                debug_menu(stdscr, menu_items, init_messages_count)

def set_cookie(stdscr, menu_items, init_messages_count):
    curses.curs_set(0)
    stdscr.clear()
    for idx, message in enumerate(menu_items[:init_messages_count]):
        stdscr.addstr(idx, 0, message)
    stdscr.addstr(init_messages_count, 0, '设置Cookie')
    stdscr.addstr(init_messages_count + 1, 0, '1. 设置Cookie')
    stdscr.refresh()
    curses.echo()
    choice = stdscr.getstr(init_messages_count + 2, 0).decode('utf-8')
    curses.noecho()

    if choice == '1':
        while True:
            stdscr.clear()
            for idx, message in enumerate(menu_items[:init_messages_count]):
                stdscr.addstr(idx, 0, message)
            stdscr.addstr(init_messages_count, 0, 'Cookie:')
            stdscr.refresh()
            curses.echo()
            cookie = stdscr.getstr(init_messages_count + 1, 0).decode('utf-8')
            curses.noecho()

            data = user_inquire(cookie)
            if data == 'false':
                stdscr.clear()
                for idx, message in enumerate(menu_items[:init_messages_count]):
                    stdscr.addstr(idx, 0, message)
                stdscr.addstr(init_messages_count, 0, 'Cookie无效,请重新设置')
                stdscr.refresh()
                stdscr.getch()
            else:
                with open('cookie.ini', 'w', encoding='utf-8') as f:
                    f.write(cookie)
                stdscr.clear()
                for idx, message in enumerate(menu_items[:init_messages_count]):
                    stdscr.addstr(idx, 0, message)
                stdscr.addstr(init_messages_count, 0, f'用户名称:{data[0]}')
                stdscr.addstr(init_messages_count + 1, 0, f'用户头像URL:{data[1]}')
                stdscr.addstr(init_messages_count + 2, 0, f'用户id:{data[2]}')
                stdscr.addstr(init_messages_count + 3, 0, f'用户简介:{data[3]}')
                stdscr.refresh()
                stdscr.getch()
                break

def debug_menu(stdscr, menu_items, init_messages_count):
    curses.curs_set(0)
    stdscr.clear()
    for idx, message in enumerate(menu_items[:init_messages_count]):
        stdscr.addstr(idx, 0, message)
    stdscr.addstr(init_messages_count, 0, 'DEBUG菜单')
    stdscr.addstr(init_messages_count + 1, 0, '1. api测试')
    stdscr.addstr(init_messages_count + 2, 0, '2. 番茄听书')
    stdscr.refresh()
    curses.echo()
    choice = stdscr.getstr(init_messages_count + 3, 0).decode('utf-8')
    curses.noecho()

    if choice == '1':
        os.system('python ./Main/Test.py')
    elif choice == '2':
        os.system('python ./Main/Test2.py')

def main(stdscr):
    # 初始化
    curses.curs_set(0)  # 隐藏光标
    stdscr.clear()

    # 获取初始化信息
    init_messages = [
        "欢迎使用",
        "一言:" + json.loads(requests.get(url='https://v1.hitokoto.cn').text)['hitokoto'],
        "---------------"
    ]

    if not os.path.exists('cookie.ini'):
        with open('cookie.ini', 'w', encoding='utf-8') as ce:
            ce.close()

    with open('cookie.ini', 'r', encoding='utf-8') as data:
        login_data = user_inquire(data.read())
        if login_data == 'false':
            init_messages.extend([
                "登录失败,部分功能无法使用，请配置cookie",
                "---------------"
            ])
        else:
            init_messages.extend([
                f"用户名称:{login_data[0]}",
                f"用户头像URL:{login_data[1]}",
                f"用户id:{login_data[2]}",
                f"用户简介:{login_data[3]}",
                "---------------"
            ])

    # 定义菜单选项
    menu_options = [
        "1. 搜索书籍",
        "2. 朗读书籍",
        "3. 爬取书籍",
        "4. 推荐榜",
        "5. 设置",
        "6. DEBUG",
        "q. 退出"
    ]

    # 合并初始化信息和菜单选项
    menu_items = init_messages + menu_options

    # 初始化信息的数量
    init_messages_count = len(init_messages)

    try:
        show_menu(stdscr, menu_items, init_messages_count)
    finally:
        try:
            curses.endwin()  # 确保在任何情况下都结束 curses 模式
        except curses.error as e:
            stdscr.addstr(0, 0, f'错误: {e}')
            stdscr.refresh()
            stdscr.getch()
        os.system('stty sane')  # 恢复终端设置

if __name__ == "__main__":
    curses.wrapper(main)
