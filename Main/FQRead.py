import os
import edge_tts
import asyncio
import _thread
import curses
from Main.API import update_progres, user_bookshelf, book_id_inquire, item_id_inquire

# 预设一些中文音色供选择
preset_voices = ['zh-CN-XiaoxiaoNeural', 'zh-CN-YunyangNeural', 'zh-CN-YunxiNeural', 'zh-CN-LinglingNeural']

def thread(p, stdscr):
    global content, voice, rate_count, volume_count, executable, title_list, item_id_list, name, output_files, count
    stdscr.addstr(10, 0, '正在爬取并生成音频')
    stdscr.refresh()
    if p >= len(title_list):
        stdscr.addstr(11, 0, '没有更多章节可供播放')
        stdscr.refresh()
        stdscr.getch()
        return
    else:
        content = item_id_inquire(item_id_list[p])[0]
        stdscr.addstr(11, 0, f'文字数:{len(content)}')
        stdscr.refresh()
        asyncio.run(run_tts(title_list[p] + content, voice, rate_count, volume_count, stdscr))
        if executable == 'False':
            executable = 'True'

async def run_tts(text: str, voice: str, rate: str, volume: str, stdscr) -> None:
    global title_list, output_files, count
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, volume=volume)
    await communicate.save(output_files + item_id_list[p + count] + '_TEMP.mp3')
    stdscr.addstr(12, 0, '音频已生成')
    stdscr.refresh()

def show_menu(stdscr, items, prompt):
    active_row = 0
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, prompt)
        for idx, row in enumerate(items):
            x = w // 2 - len(row) // 2
            y = h // 2 - len(items) // 2 + idx
            if y < 0 or y >= h:
                continue
            if idx == active_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and active_row > 0:
            active_row -= 1
        elif key == curses.KEY_UP and current_page > 0:
            active_row = page_size - 1
            current_page -= 1
        elif key == curses.KEY_DOWN and active_row < len(items) - 1:
            active_row += 1
        elif key == curses.KEY_DOWN and end_idx < len(items):
            active_row = 0
            current_page += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return items[start_idx + active_row]

def show_paginated_menu(stdscr, items, prompt, page_size=10):
    active_row = 0
    current_page = 0
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, prompt)
        start_idx = current_page * page_size
        end_idx = start_idx + page_size
        visible_items = items[start_idx:end_idx]

        for idx, row in enumerate(visible_items):
            x = w // 2 - len(row) // 2
            y = h // 2 - len(visible_items) // 2 + idx
            if y < 0 or y >= h:
                continue
            if idx == active_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and active_row > 0:
            active_row -= 1
        elif key == curses.KEY_UP and current_page > 0:
            active_row = page_size - 1
            current_page -= 1
        elif key == curses.KEY_DOWN and active_row < len(visible_items) - 1:
            active_row += 1
        elif key == curses.KEY_DOWN and end_idx < len(items):
            active_row = 0
            current_page += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return items[start_idx + active_row]

def main(stdscr):
    global content, voice, rate_count, volume_count, executable, title_list, item_id_list, name, output_files, count
    cookie = open('cookie.ini', 'r').read()
    executable = 'False'
    url = 'https://novel.snssdk.com/api/novel/reader/full/v1/?item_id='

    stdscr.clear()
    stdscr.addstr(0, 0, '欢迎使用阅读器')
    stdscr.refresh()

    book_id = get_input('book_id(输入空则使用最近播放):', stdscr)
    if book_id == '':
        book_id = user_bookshelf(cookie)[0][0]
    data = book_id_inquire(book_id)
    title_list = data[1]
    item_id_list = data[0]
    name = data[2]

    # 使用分页菜单选择章节
    p = show_paginated_menu(stdscr, title_list, '请选择章节：')
    p = title_list.index(p)

    # 使用普通菜单选择音色
    voice = show_menu(stdscr, preset_voices, '请选择音色：')

    rate_count = get_input('语速大小(默认+0%):', stdscr)
    volume_count = get_input('音量大小(默认+0%):', stdscr)

    if rate_count == '':
        rate_count = '+0%'
    if volume_count == '':
        volume_count = '+0%'

    stdscr.addstr(10, 0, '初始化完成，开始播放')
    stdscr.refresh()

    _thread.start_new_thread(thread, (p + count, stdscr))
    while True:
        if executable == 'True':
            if len(title_list) <= p + count:
                stdscr.addstr(11, 0, '章节播放完毕 感谢使用')
                stdscr.refresh()
                stdscr.getch()
                break
            else:
                executable = 'False'
                title = title_list[p + count]
                item_id = item_id_list[p + count]
                count += 1
                stdscr.addstr(11, 0, f'即将播放:{name}:{title}')
                stdscr.refresh()
                _thread.start_new_thread(update_progres, (cookie, item_id))
                _thread.start_new_thread(thread, (p + count, stdscr))
                os.system('mpv ' + '"' + output_files + item_id + '_TEMP.mp3' + '"')
                os.remove(output_files + item_id + '_TEMP.mp3')

    # 确保在返回main.py之前恢复光标
    curses.curs_set(1)
    stdscr.clear()
    stdscr.refresh()

def get_input(prompt, stdscr):
    stdscr.addstr(8, 0, prompt)
    stdscr.refresh()
    curses.echo()
    user_input = stdscr.getstr(9, 0).decode('utf-8')
    curses.noecho()
    stdscr.addstr(8, 0, ' ' * len(prompt))  # 清除提示
    stdscr.addstr(9, 0, ' ' * len(user_input))  # 清除输入
    stdscr.refresh()
    return user_input

# 将main函数暴露给main.py调用
if __name__ == "__main__":
    curses.wrapper(main)
