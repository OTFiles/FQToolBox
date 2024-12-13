import os
import edge_tts
import asyncio
import curses
from API import update_progres, user_bookshelf, book_id_inquire, item_id_inquire

def thread(p, stdscr):
    global content, voice, rate_count, volume_count, executable, title_list, item_id_list, name, output_files, count
    stdscr.addstr(10, 0, '正在爬取并生成音频')
    stdscr.refresh()
    if p > len(title_list):
        stdscr.addstr(11, 0, '没有更多章节可供播放')
        stdscr.refresh()
        stdscr.getch()
        return
    else:
        content = item_id_inquire(item_id_list[p - 1])[0]
        stdscr.addstr(11, 0, f'文字数:{len(content)}')
        stdscr.refresh()
        asyncio.run(run_tts(title_list[p - 1] + content, voice, rate_count, volume_count, stdscr))
        if executable == 'False':
            executable = 'True'

async def run_tts(text: str, voice: str, rate: str, volume: str, stdscr) -> None:
    global title_list, output_files, count
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, volume=volume)
    await communicate.save(output_files + item_id_list[p - 1 + count] + '_TEMP.mp3')
    stdscr.addstr(12, 0, '音频已生成')
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
    for r in range(len(title_list)):
        stdscr.addstr(r + 2, 0, f'章节 {r + 1} :{title_list[r]}')
    stdscr.refresh()

    p = int(get_input('选择:', stdscr)) - 1  # curses的输入从0开始输出，所以选择-1

    count = 0
    content = None
    output_files = './TEMP/' + book_id + '_ceche/'
    if not os.path.exists(output_files):
        os.makedirs(output_files)

    voice = get_input('请选择音色(默认zh-CN-XiaoxiaoNeural):', stdscr)
    rate_count = get_input('语速大小(默认+0%):', stdscr)
    volume_count = get_input('音量大小(默认+0%):', stdscr)

    if voice == '':
        voice = 'zh-CN-XiaoxiaoNeural'
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

if __name__ == "__main__":
    curses.wrapper(main)
