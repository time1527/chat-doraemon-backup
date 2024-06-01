# learn from:https://github.com/Omelette-lab/chat-daiyu/tree/main
# mainly by chatgpt
import os
import sys
import re
import json
import glob
from openai import OpenAI
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from kor import create_extraction_chain, Object, Text

sys.path.append("/home/pika/")
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
base_url = os.environ.get("OPENAI_API_BASE")

# 角色映射
role_mapping = {
    '对话人': 'user',
    '哆啦A梦': 'assistant'
}

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    openai_api_base=base_url,
    openai_api_key=api_key,
    temperature=0.8,
    # max_tokens=2000,
    # model_kwargs = {
    #     'frequency_penalty':0,
    #     'presence_penalty':0,
    #     'top_p':1.0
    # }
)


schema = Object(
    id="script",
    description="接下来你会收到哆啦A梦的语录，请你根据收到的语录生成相应的上一句对话人说的话（3-5）个，并按照示例给的格式输出",
    attributes=[
        Text(
            id="role",
            description="正在说话的角色(对话人和哆啦A梦轮流)",
        ),
        Text(
            id="dialogue",
            description="角色说话的内容",
        )
    ],
    examples=[
        (
            '''
            大人真可怜，没有能让自己依靠、撒娇和骂自己的人。
            ''',
            [
                {"role": "对话人", "dialogue": "爸爸看起来好辛苦啊！"},
                {"role": "哆啦A梦", "dialogue": "大人真可怜，没有能让自己依靠、撒娇和骂自己的人。"},
                {"role": "对话人", "dialogue": "是呀！大人的世界好像也没想象中那么好！"},
                {"role": "哆啦A梦", "dialogue": "大人真可怜，没有能让自己依靠、撒娇和骂自己的人。"},
                {"role": "对话人", "dialogue": "长大了一点都不开心！"},
                {"role": "哆啦A梦", "dialogue": "大人真可怜，没有能让自己依靠、撒娇和骂自己的人。"},
            ],
        ),
        (
            '''
            别人有的东西你就想要，这是你的坏习惯。
            ''',
            [
                {"role": "对话人", "dialogue": "好想要小夫的望远镜！"},
                {"role": "哆啦A梦", "dialogue": "别人有的东西你就想要，这是你的坏习惯。"},
                {"role": "对话人", "dialogue": "他们都有新玩具，就我没有，我也要！我也要！"},
                {"role": "哆啦A梦", "dialogue": "别人有的东西你就想要，这是你的坏习惯。"},
                {"role": "对话人", "dialogue": "好羡慕小夫啊！他爸爸给他买了遥控汽车！威风得很，为什么我没有？"},
                {"role": "哆啦A梦", "dialogue": "别人有的东西你就想要，这是你的坏习惯。"},
            ],
        )
    ],
    many=True,
)


def load_jsonl(file_path):
    """加载 JSONL 文件并返回一个包含所有记录的列表"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [json.loads(line) for line in file]
    

def remove_duplicate_conversations(conversations):
    # 用于存储去重后的对话列表
    unique_conversations = []
    # 用于跟踪已经见过的 'user' 内容
    seen_contents = set()

    # 遍历原始对话列表
    for convo in conversations:
        user_content = convo['conversation'][0]['content']
        # 如果内容未见过，则添加到去重后的列表，并标记为已见过
        if user_content not in seen_contents:
            unique_conversations.append(convo)
            seen_contents.add(user_content)

    return unique_conversations


def save_conversations_to_jsonl(conversations, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for convo in conversations:
            json_line = json.dumps(convo, ensure_ascii=False)
            f.write(json_line + '\n')


def gen_idx(data,idx,prefix="more"):
    chain = create_extraction_chain(llm, schema, encoder_or_encoder_class='json')
    
    all_qa = []
    res = chain.invoke(data[idx])
    conversations = res["text"]['data']['script']

    # 转换后的对话列表
    converted_conversations = []

    # 遍历原始对话列表，转换格式
    for i in range(0, len(conversations), 2):
        user_dialogue = conversations[i]['dialogue']
        if i +1 > len(conversations)-1:break
        assistant_dialogue = conversations[i + 1]['dialogue']
        converted_conversations.append({
            "conversation": [
                {
                    "role": role_mapping[conversations[i]['role']],
                    "content": user_dialogue
                },
                {
                    "role": role_mapping[conversations[i + 1]['role']],
                    "content": assistant_dialogue
                }
            ]
        })

    # # 打印转换后的对话列表
    # print(json.dumps(converted_conversations, ensure_ascii=False, indent=4))
    all_qa.extend(converted_conversations)

    # 去重
    dedup = remove_duplicate_conversations(all_qa)
    # 保存
    save_conversations_to_jsonl(dedup,f"{prefix}_{idx}.jsonl")
    print(f"finish {idx}")


def merge_jsonl_files(input_pattern, output_file):
    # 获取匹配指定模式的文件列表
    input_files = glob.glob(input_pattern)

    # 用于保存合并后的内容
    merged_content = []

    # 遍历每个输入文件
    for file_path in input_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 逐行读取内容并加入到合并后的列表中
            for line in f:
                merged_content.append(json.loads(line))

    # 将合并后的内容写入到输出文件中
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in merged_content:
            json_line = json.dumps(item, ensure_ascii=False,indent=4)
            f.write(json_line + '\n')


def merge_and_deduplicate_jsonl_files(input_pattern, output_file):
    # 获取匹配指定模式的文件列表
    input_files = glob.glob(input_pattern)

    # 用于存储合并和去重后的内容
    unique_conversations = []
    # 用于跟踪已见过的 'user' 内容
    seen_contents = set()

    # 遍历每个输入文件
    for file_path in input_files:
        buffer = ''
        brace_level = 0
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                convo = {}
                buffer += line
                brace_level += line.count('{') - line.count('}')
                # 检查缓冲区中的大括号是否平衡
                if brace_level == 0 and buffer.strip():
                    try:
                        item = json.loads(buffer)

                        if 'conversation' in item:
                            convo = eval(json.dumps(item,ensure_ascii=False))
                            # print(f"Item : {json.dumps(item,ensure_ascii=False)}")
                    except json.JSONDecodeError as e:
                        print(f"JSONDecodeError: {e}")
                    buffer = ''  # 清空缓冲区
                if 'conversation' in convo:
                    user_content = convo['conversation'][0]['content']
                    # 如果内容未见过，则添加到去重后的列表，并标记为已见过
                    if user_content and user_content not in seen_contents:
                        unique_conversations.append(convo)
                        seen_contents.add(user_content)
    # print(unique_conversations)
    # 将去重后的内容写入到输出文件中
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in unique_conversations:
            json_line = json.dumps(item, ensure_ascii=False)
            f.write(json_line + '\n')


if __name__ == "__main__":
    most = load_jsonl("most.jsonl")
    # 重复生成10次，取并集
    for cnt in range(10):
        ne = []
        for idx in range(len(most)):
            try:
                # 生成f"most{cnt}_{idx}.jsonl"
                gen_idx(most,idx,f"most{cnt}")
            except Exception as e:
                print(f"Fail {idx}!")
                ne.append(idx)

        nene = []
        for idx in ne:
            try:
                gen_idx(most,idx,f"most{cnt}")
            except Exception as e:
                print(f"Fail {idx}!")
                nene.append(idx)

        # 示例：合并所有名字匹配 "most1_*.jsonl" 的文件到 "most1_merged.jsonl" 中
        merge_jsonl_files(f'most{cnt}_*.jsonl', f'most{cnt}_merged.jsonl')
        # 人工检查

    # 最后合并
    merge_and_deduplicate_jsonl_files('most*_merged.jsonl','most_conversations.jsonl')