# ref

## 模块

### 微调

数据集：

* 自我认知
* 基础数据：比如，你几岁，你喜欢什么，你讨厌什么
* 对话数据：
  * .mp4抽取
  * 根据经典语录生成问题
* 通过旁白/其他人的信息得到数据：比如，哆啦美为什么比你聪明
* 道具数据：比如任意门是干什么的

### agent

* 道具：
  * 动漫中原有的道具（名字需要和.mp4中对齐）：
    * [竹蜻蜓](https://doraemon.fandom.com/zh/wiki/%E7%AB%B9%E8%9C%BB%E8%9C%93)：动画电视统一
    * [时光机](https://doraemon.fandom.com/zh/wiki/%E6%99%82%E5%85%89%E6%A9%9F)
    * [任意门](https://doraemon.fandom.com/zh/wiki/%E4%BB%BB%E6%84%8F%E9%96%80)：漫画
    * [缩小灯](https://doraemon.fandom.com/zh/wiki/%E7%B8%AE%E5%B0%8F%E7%87%88)
    * [放大灯](https://doraemon.fandom.com/zh/wiki/%E6%94%BE%E5%A4%A7%E7%87%88)
    * [记忆吐司](https://doraemon.fandom.com/zh/wiki/%E8%A8%98%E6%86%B6%E5%90%90%E5%8F%B8)：1979年大山版
    
  * 辅助llm回答问题：例如在用户询问关于“哆啦美”时会检索本地存储的哆啦美资料/例如询问某道具是干嘛的（这个或许可以直接使用上面的道具？）
    * https://github.com/modelscope/agentscope/blob/main/src/agentscope/service/retrieval/retrieval_from_list.py
    * https://github.com/modelscope/modelscope-agent/blob/master/modelscope_agent/tools/similarity_search.py
    
  * 现代世界的道具：
    * 本地model加载：
    
    * api：
    
    * 其他：
      * metagpt相关：
        * OCR：paddleocr
          * https://github.com/geekan/MetaGPT/blob/main/metagpt/actions/invoice_ocr.py#L31
          * https://docs.deepwisdom.ai/main/zh/guide/use_cases/agent/receipt_assistant.html
        * [x用的模型是gpt-4-vision-preview]网页仿写：https://github.com/geekan/MetaGPT/blob/main/examples/di/imitate_webpage.py
        * 网页爬取：https://docs.deepwisdom.ai/main/zh/guide/use_cases/agent/interpreter/crawl_webpage.html
        * [x用的是api]文生图：https://docs.deepwisdom.ai/main/zh/guide/use_cases/agent/interpreter/text2image.html
        * [x需要登陆邮箱]邮件总结与回复：https://docs.deepwisdom.ai/main/zh/guide/use_cases/agent/interpreter/email_summary.html
        * github trending爬取：https://deepwisdom.feishu.cn/wiki/KhCcweQKmijXi6kDwnicM0qpnEf
        * 派生：huggingface papers爬取
      
      * agenscope相关：https://modelscope.github.io/agentscope/zh_CN/tutorial/204-service.html
        * [感觉应该是prompt的活]使用大型语言模型总结一段文字以突出其主要要点：https://github.com/modelscope/agentscope/blob/main/src/agentscope/service/text_processing/summarization.py
        * 爬取并解析指定的网页链接 （目前仅支持爬取 HTML 页面）：https://github.com/modelscope/agentscope/blob/main/src/agentscope/service/web/web_digest.py
        * 对已经爬取好的网页生成摘要信息（目前仅支持 HTML 页面：https://github.com/modelscope/agentscope/blob/main/src/agentscope/service/web/web_digest.py
        * [需要dblp api]在dblp数据库里搜索文献：https://github.com/modelscope/agentscope/blob/main/src/agentscope/service/web/dblp.py
        * [需要dblp api]在dblp数据库里搜索作者：https://github.com/modelscope/agentscope/blob/main/src/agentscope/service/web/dblp.py
        * [需要dblp api]在dblp数据库里搜索期刊，会议及研讨会：https://github.com/modelscope/agentscope/blob/main/src/agentscope/service/web/dblp.py
      
      * agentlogo：没怎么看
        * 一些本地加载模型的tools
          * https://github.com/InternLM/agentlego/tree/main/agentlego/tools
          * https://agentlego.readthedocs.io/zh-cn/latest/modules/tool.html
        * magicmaker：https://github.com/InternLM/Tutorial/blob/camp2/agent/agentlego.md
        * [或许可以调包？]翻译：https://github.com/InternLM/agentlego/blob/main/agentlego/tools/translation/translation.py
      
      * 网页截图：
      
        ```python
        """
        pip install playwright
        playwright install
        可能报错还要装一个什么dev的，记录一下装环境的过程，我这里history看不到了
        """
        
        from playwright.sync_api import sync_playwright
        def run(playwright):
             # launch the browser
             browser = playwright.chromium.launch()
             # opens a new browser page
             page = browser.new_page()
             # navigate to the website
             page.goto('https://rank.opencompass.org.cn/home')
             # take a full-page screenshot
             page.screenshot(path='example.png', full_page=True)
             # always close the browser
             browser.close()
        with sync_playwright() as playwright:
            run(playwright)
        ```

### 语音

* 提取清晰语音，去噪等，使得能够通过输入文本输出特定音色

### 前端

* 暂定gradio/streamlit：结合下已有成功项目的结果再定
* agentlego：https://github.com/InternLM/agentlego/blob/main/webui/app.py

## 资料收集

### 已有的成功roleplay repo

https://github.com/LC1332/Chat-Haruhi-Suzumiya：动漫视频数据抽取；其余各方面也很完善

https://github.com/Omelette-lab/chat-daiyu：数据处理+语音

https://github.com/SaaRaaS-1300/InternLM2_horowag：数据增强+语音

https://github.com/JimmyMa99/BaJie-Chat：基础数据

### agent

https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/Doraemon_Agent.ipynb：哆啦

A梦道具的实现

https://github.com/public-apis/public-apis：API大全

https://github.com/n0shake/Public-APIs：API大全

### Unity前端

https://github.com/zhangliwei7758/unity-AI-Chat-Toolkit

### 哆啦A梦一些信息

https://doraemon.fandom.com/zh/wiki/%E9%A6%96%E9%A0%81?utm_source=fandom-explore-zh：包含一些个人信息+工具信息

https://baike.baidu.com/item/%E5%93%86%E5%95%A6A%E6%A2%A6/185384：百度百科

https://duola.huijiwiki.com/wiki/Doraemon

https://duola.huijiwiki.com/wiki/%E8%A7%92%E8%89%B2%E5%88%97%E8%A1%A8：角色列表，人物细节（比如喜欢什么/擅长什么/讨厌什么）

## 环境

```bash
cd ~
git clone https://github.com/time1527/chat-doraemon.git
cd chat-doraemon/
# 考虑切分支
mkdir agent
cd agent
# 创建环境/已经有的话就别建了再
studio-conda -t agent -o pytorch-2.1.2
## 本地的话就：
#
# conda create -n agent python=3.10
# conda activate agent
# conda install pytorch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 pytorch-cuda=11.8 -c pytorch -c nvidia
#

conda activate agent
git clone https://github.com/InternLM/lagent.git
cd lagent
# main分支最新的一次commit
git checkout 64ddf7b0d8adf29c5f859e3d7ec7fd01760ba58f
pip install -e . 
pip install lmdeploy==0.4.1

# 起api服务
conda activate agent
lmdeploy serve api_server /root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-7b  --server-name 127.0.0.1  --model-name internlm2-chat-7b  --cache-max-entry-count 0.1
# 再开一个terminal起前端
streamlit run internlm2_agent_web_demo.py --server.address 127.0.0.1 --server.port 7860
# 本地映射一下：我本地vscode远程的，起完前端点击本地右下角跳出来的那个链接进去，会报错大概是什么string indices must be integers
ssh -CNg -L 7860:127.0.0.1:7860 -L 23333:127.0.0.1:23333 root@ssh.intern-ai.org.cn -p 你的 ssh 端口号
# 浏览器打开：http://localhost:7860
# 模型IP修改：127.0.0.1:23333
# 选tools
# 开始问
```

## tool举例+修改后怎么测试

```python
# 放在lagent/actions下面，文件名是movie.py

import json
import os
import requests
from typing import Optional, Type

from lagent.actions.base_action import BaseAction, tool_api
from lagent.actions.parser import BaseParser, JsonParser
from lagent.schema import ActionReturn, ActionStatusCode

class MovieQuery(BaseAction):
    def __init__(self,
                 key: Optional[str] = None,
                 description: Optional[dict] = None,
                 parser: Type[BaseParser] = JsonParser,
                 enable: bool = True) -> None:
        super().__init__(description, parser, enable)
        key = "31b004cb"#os.environ.get('OMDb_API_KEY', key)
        if key is None:
            raise ValueError(
                'Please set OMDb API key either in the environment '
                'as OMDb_API_KEY or pass it as `key`')
        self.key = key
        self.query_url = f'http://www.omdbapi.com/?apikey={key}&t='

    @tool_api
    def run(self, query: str) -> ActionReturn:
        """一个电影查询API。可以根据电影名查询电影信息。
        
        Args:
            query (:class:`str`): The movie name to query.
        """
        tool_return = ActionReturn(type=self.name)
        status_code, response = self._search(query)
        if status_code == -1:
            tool_return.errmsg = response
            tool_return.state = ActionStatusCode.HTTP_ERROR
        elif status_code == 200:
            parsed_res = self._parse_results(response)
            # ！！！！ 这个比较重要，不同的type会以不同的形式展示出来！！！
            if parsed_res[1] != None:
                tool_return.result = [dict(type='text', content=str(parsed_res[0])),
                dict(type='image', content=str(parsed_res[1]))]
            else:
                tool_return.result = [dict(type='text', content=str(parsed_res[0]))]
            tool_return.state = ActionStatusCode.SUCCESS
        else:
            tool_return.errmsg = str(status_code)
            tool_return.state = ActionStatusCode.API_ERROR
        return tool_return
    
    def _parse_results(self, movie_dict: dict) -> (str,str | None):
        """Parse the movie results from OMDb API.
        
        Args:
            movie_dict (dict): The movie content from OMDb API
                in json format.
        
        Returns:
            str: The parsed movie results.
        """
        data = [
            f'名称: {movie_dict["Title"]}',
            f'年份: {movie_dict["Year"]}',
            f'评级: {movie_dict["Rated"]}',
            f'上映日期: {movie_dict["Released"]}',
            f'时长: {movie_dict["Runtime"]}',
            f'类型: {movie_dict["Genre"]}',
            f'导演: {movie_dict["Director"]}',
            f'编剧: {movie_dict["Writer"]}',
            f'演员: {movie_dict["Actors"]}',
            f'剧情简介: {movie_dict["Plot"]}',
            f'语言: {movie_dict["Language"]}',
            f'国家/地区: {movie_dict["Country"]}',
            f'奖项: {movie_dict["Awards"]}',
            f'评分: {movie_dict["Metascore"]}',
            f'imdb评分: {movie_dict["imdbRating"]}',
            f'imdb投票数: {movie_dict["imdbVotes"]}',
            f'imdb ID: {movie_dict["imdbID"]}',
            f'类型: {movie_dict["Type"]}',
            f'DVD发布日期: {movie_dict["DVD"]}',
            f'票房: {movie_dict["BoxOffice"]}',
            f'制作公司: {movie_dict["Production"]}',
            f'网站: {movie_dict["Website"]}',]
        # 如果有海报就把网图下载到本地了不然open不出来啊咱
        if movie_dict["Poster"]:
            import requests
            res = requests.get(movie_dict["Poster"])
            with open('/root/test.jpg', 'wb') as f:
                f.write(res.content)
            return ('\n'.join(data),'/root/test.jpg')
        else: return ('\n'.join(data),None)

    def _search(self, query: str):
        try:
            response = requests.get(
                self.query_url,
                params={'t': query}
            )
        except Exception as e:
            return -1, str(e)
        return response.status_code, response.json()

```

```python
# internlm2_agent_web_demo.py的修改：

from lagent.actions.movie import MovieQuery

# 第24～26行附近，把这个tool添加到action_list
action_list = [
    ArxivSearch(),MovieQuery()
]

# 就可以跑啦～～
```

## git操作

```bash
cd ~
git clone https://github.com/time1527/chat-doraemon.git
cd chat-doraemon
git submodule update --init --recursive # 拉取chat-doraemon下的那个lagent commit-id
# 假设当前 chat 的 main 分支 track agent/lagent 的 test 分支上的 v1 commit
# 可通过 `git submodule status` 查看具体 commit-id
# 接下来我需要本地同时对 chat 和 agent/lagent 的文件进行修改、调试
# 一通操作，例如两边各创建一个文件，并且调试通过，此时需要同时更新两个 repo
touch a.py
touch agent/lagent/b.py
git add a.py
cd agent/lagent
git add b.py
git commit -m "add b.py"
# 下面这行是为了将 agent/lagent 更新反馈到 remote
git push origin HEAD:test
# cd回chat-doraemon
cd - # 自己看情况写，最后得回到chat-doraemon目录
git add agent/lagent
git commit -m "add a.py and update agent/lagent"
git push origin
```

https://git-scm.com/docs/git-submodule

