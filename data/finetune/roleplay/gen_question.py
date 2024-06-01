# mainly by chatgpt
import os
import sys
import time
import json
from openai import OpenAI
from dotenv import load_dotenv

sys.path.append("/home/pika/")
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
base_url = os.environ.get("OPENAI_API_BASE")


# kimi网页对话生成：
topic_list = [
    "个人信息","教育经历","工作经历","兴趣爱好",
    "擅长的技能","专业领域","对某个话题的看法",
    "人生目标","道德和伦理观念","日常习惯",
    "饮食偏好","休闲活动","家庭状况",
    "亲密关系","社交圈子",
    "工作挑战","成就和失败","健康状况",
    "运动习惯","情绪管理","压力来源",
    "心理支持需求","对当前政治事件的看法",
    "社会问题的观点","旅行和探险","未来规划"
]

role_list = ["哆啦美","大雄","静香","小夫","胖虎"]

# kimi网页对话生成：
knowledge_list = [
    '物理学', '化学', '生物学', '地质学', '天文学',
    '社会学', '心理学', '经济学', '政治学', '人类学',
    '机械工程', '电子工程', '土木工程', '化学工程',
    '临床医学', '基础医学', '公共卫生', '护理学', '药学',
    '纯数学', '应用数学', '统计学', '数学物理',
    '数据结构', '算法', '人工智能', '机器学习', '软件工程',
    '音乐学', '美术学', '表演艺术', '设计学', '文化研究',
    '历史学', '文学', '语言学', '哲学', '宗教学',
    '法律学', '国际法', '商法', '刑法', '民法',
    '教育心理学', '课程与教学', '教育管理', '特殊教育',
    '管理学', '市场营销', '会计学', '金融学', '人力资源管理',
    '农学', '林学', '动物科学', '农业经济学',
    '生态学', '环境工程', '可持续发展', '气候学',
    '战略学', '战术学', '军事历史', '军事技术',
    '认知科学', '生物信息学', '纳米技术', '材料科学'
]


def get_completion(prompt,system_prompt=None):
    client = OpenAI(api_key=api_key,base_url=base_url)
    messages = []
    if system_prompt != None:
        messages.append({'role':'system','content':system_prompt})
    messages.append({'role': 'user', 'content': prompt})

    completion = client.chat.completions.create(
         model='gpt-3.5-turbo',
         messages=messages,
         temperature=0.8)
    return completion.choices[0].message.content


if __name__ == "__main__":
    # 1. topic_list
    self_questions=[]
    try:
        for topic in topic_list:
            response = get_completion(f"请提出20个关于{topic}的不重复的问题，问题之间使用换行符分割")
            print(response)
            self_questions.extend(response.split("\n"))
    except Exception as e:
        with open('self_questions.jsonl', 'w', encoding='utf-8') as f:
            for item in self_questions:
                json_item = json.dumps(item.split(".")[-1].strip(), ensure_ascii=False)
                f.write(json_item + "\n")
        print('e')
    with open('self_questions.jsonl', 'w', encoding='utf-8') as f:
        for item in self_questions:
            json_item = json.dumps(item.split(".")[-1].strip(), ensure_ascii=False)
            f.write(json_item + "\n")

    # 2. role_list
    role_questions = []
    try:
        for topic in role_list:
            response = get_completion(f"请向哆啦A梦提出20个关于{topic}的不重复的问题，注意问题必须与{topic}相关，问题中的“你”表示“哆啦A梦”，问题之间使用换行符分割")
            print(response)
            role_questions.extend(response.split("\n"))
    except Exception as e:
        with open('role_questions.jsonl', 'w', encoding='utf-8') as f:
            for item in role_questions:
                json_item = json.dumps(item.split(".")[-1].strip().replace("哆啦A梦","你"), ensure_ascii=False)
                f.write(json_item + "\n")
        print('e')
    with open('role_questions.jsonl', 'w', encoding='utf-8') as f:
        for item in role_questions:
            json_item = json.dumps(item.split(".")[-1].strip().replace("哆啦A梦","你"), ensure_ascii=False)
            f.write(json_item + "\n")

    # 3. knowledge_list
    knowledge_questions=[]
    try:
        for topic in knowledge_list:
            time.sleep(30)
            response = get_completion(f"请提出5个关于{topic}的不重复的深层次的问题，问题之间使用换行符分割")
            print(response)
            knowledge_questions.extend(response.split("\n"))
    except Exception as e:
        with open('knowledge_questions.jsonl', 'w', encoding='utf-8') as f:
            for item in knowledge_questions:
                json_item = json.dumps(item.split(".")[-1].strip(), ensure_ascii=False)
                f.write(json_item + "\n")
        print('e')
    with open('knowledge_questions.jsonl', 'w', encoding='utf-8') as f:
        for item in knowledge_questions:
            json_item = json.dumps(item.split(".")[-1].strip(), ensure_ascii=False)
            f.write(json_item + "\n")