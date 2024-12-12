# FQToolBox
一款基于Python的番茄小说工具箱
## 此工具可以做什么？
### 1.搜索小说
快速获取搜索小说并获取book_id
### 2.阅读小说
可使用~~windows内置语音引擎~~(已弃用)或使用[edge-tts](https://github.com/rany2/edge-tts)阅读小说
### 3.爬取小说
多线程一键爬取小说为txt文本
## 如何使用
运行以下代码以安装所需运行库
```bash
pip install requests edge-tts asyncio tqdm
```
且还需要安装[mpv](https://mpv.io/)用以播放小说
##修改了什么
###Menu
添加了一个退出选项
添加了一个TUI菜单，由此，一些功能现在并不兼容，需要等待修复，请稍等
###搜索
为搜索功能添加了一个TUI菜单，同时可以在搜索快速爬取小说
###爬虫
修改了爬虫脚本的名字，并且打包为几个函数方便调用
~~为了省事还删掉了合并TXT的功能~~(划掉)