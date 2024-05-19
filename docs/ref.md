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



