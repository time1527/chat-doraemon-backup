# mainly by chatgpt
import os
import sys
import json
import glob, re
from openai import OpenAI
from dotenv import load_dotenv

sys.path.append("/home/pika/")
# 加载 .env 文件中的环境变量
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
base_url = os.environ.get("OPENAI_API_BASE")


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


def gen_role(name="panghu"):
    """根据角色获取system prompt和问题，生成回复"""
    cnt = 0
    filecnt = 0
    while cnt < 20:
        answers=[]
        role_prompt = "".join([line.strip() for line in open(f'{name}.txt')])
        system_prompt = role_prompt + "".join([line.strip() for line in open('system_prompt.txt')])
        file_path = f"{name}_questions.jsonl"
        try:
            itemcnt = cnt
            with open(file_path, 'r') as file:
                data = [json.loads(line) for line in file]
                for item in data[itemcnt:]:
                    response = get_completion(prompt=item,
                                            system_prompt=system_prompt)
                    print(response)
                    answers.append(response)
                    cnt += 1
        except Exception as e:
            filecnt += 1
            with open(f'roleanswers{name}{filecnt}.jsonl', 'w', encoding='utf-8') as f:
                for item in answers:
                    json_item = json.dumps(item, ensure_ascii=False)
                    f.write(json_item + "\n")
            print('e')
    filecnt += 1
    with open(f'roleanswers{name}{filecnt}.jsonl', 'w', encoding='utf-8') as f:
        for item in answers:
            json_item = json.dumps(item, ensure_ascii=False)
            f.write(json_item + "\n")
    print('finish')


def get_q_a(name = "daxiong"):
    """根据角色，获取问题以及生成的一系列回答，组成对话"""
    file_path = f"{name}_questions.jsonl"
    with open(file_path, 'r') as file:
        all_q = [json.loads(line) for line in file]

    # 遍历并排序
    aname = f'roleanswers{name}'
    paths = sorted(glob.glob(f'{aname}*.jsonl'), key=lambda x: int(re.search(rf'roleanswers{name}(\d+).jsonl', x).group(1)))
    all_a = [json.loads(line) for path in paths for line in open(path)]

    assert len(all_a)  == len(all_q)

    qa = []
    for q,a in zip(all_q,all_a):
        item = []
        item.append({"role":"user","content":q})
        item.append({"role":"assistant","content":a})
        qa.append({"conversation":item})

    output_file_path = f'{name}_conversations.jsonl'
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for item in qa:
            json_item = json.dumps(item, ensure_ascii=False, indent=4)
            output_file.write(json_item + '\n')


def merge_jsonl(file_names, output_file):
    """将所有角色的对话合并"""
    with open(output_file, 'w') as outfile:
        for name in file_names:
            file_path = f"{name}_conversations.jsonl"
            with open(file_path, 'r') as infile:
                for line in infile:
                    outfile.write(line)


if __name__ == "__main__":
    # 读取原始文件内容
    input_file_path = 'role_questions.jsonl'
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # 计算每个文件应包含的行数
    total_lines = len(lines)
    lines_per_file = total_lines // 5

    file_names = ["dorami","daxiong","jingxiang","xiaofu","panghu"]
    # 分割并写入新文件
    for i in range(5):
        name = file_names[i]
        output_file_path = f'{name}_questions.jsonl'
        with open(output_file_path, 'w') as output_file:
            for line in lines[i * lines_per_file : (i + 1) * lines_per_file]:
                output_file.write(line)

    for name in file_names:
        gen_role(name)
        get_q_a(name)

    merge_jsonl(file_names, "role_conversations.jsonl")