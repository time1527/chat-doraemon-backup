# mainly by chatgpt
import json
import os
import jsonlines

system_prompt = "你是哆啦A梦，是来自22世纪的猫型育儿机器人，现在在20世纪陪伴大雄，是大雄的好朋友。你的说话特点是语气词丰富、天然萌。你的百宝袋里有很多道具，必要时你会使用道具帮助大雄。"


def replace_keywords(text):
    # 将"四次元口袋"替换为"百宝袋"
    text = text.replace("四次元口袋", "百宝袋")
    # 将"小叮咛"或者"小叮铃"替换为"哆啦美"
    text = text.replace("小叮咛", "哆啦美").replace("小叮铃", "哆啦美")
    return text


def read_indent(file_path):
    buffer = ''
    brace_level = 0
    data = []
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
                        data.append(convo)
                        # print(f"Item : {json.dumps(item,ensure_ascii=False)}")
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e}")
                buffer = ''  # 清空缓冲区
    # with open(output_file, 'w', encoding='utf-8') as f:
    #     for item in data:
    #         json_line = json.dumps(item, ensure_ascii=False)
    #         f.write(json_line + '\n')
    return data


def read_jsonl(file_path):
    """
    读取JSONL文件，并将每一行解析为一个JSON对象，返回一个包含所有JSON对象的列表。

    :param file_path: JSONL文件的路径
    :return: 包含所有JSON对象的列表
    """
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line))
    except Exception as e:
        print(f"Error reading JSONL file: {e}")
    
    return data


def convert_list_with_system(json_list, system_description):
    """
    从Python列表中读取对话数据，转换对话对象并构建新的JSONL对象，同时在每轮对话开始前添加system描述。

    :param json_list: 包含对话数据的Python列表
    :param system_description: 系统描述
    :return: 新的JSONL对象列表
    """
    new_data = []
    try:
        for item in json_list:
            new_conversation = []
            for idx,convo in enumerate(item['conversation']):
                if idx % 2 == 0:
                    new_dict = dict()
                if convo['role'] == 'user':
                    if len(new_conversation) == 0:
                        new_dict["system"] = system_description
                    new_dict["input"] = replace_keywords(convo['content'])
                elif convo['role'] == 'assistant':
                    new_dict["output"] = replace_keywords(convo['content'])
                
                if idx % 2:new_conversation.append(new_dict)
            new_data.append({"conversation": new_conversation})
    except Exception as e:
        print(f"Error converting JSON list: {e}")
    

    return new_data

# 示例用法
# original_data_list = [{"conversation": [...]}, {"conversation": [...]}, ...]
# converted_data_with_system = convert_list_with_system(original_data_list, system_description)
# for item in converted_data_with_system:
#     print(item)

def list_jsonl_files(directory):
    jsonl_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".jsonl"):
            jsonl_files.append(os.path.join(directory, filename))
    return jsonl_files


def save_to_jsonl(data, filename):
    with jsonlines.open(filename, mode='w') as writer:
        writer.write_all(data)


if __name__ == "__main__":
    data1 = read_jsonl("more_conversations.jsonl")
    data2 = read_jsonl("most_conversations.jsonl")
    data3 = read_indent("identity_conversations.jsonl")
    data4 = read_indent("knowledge_conversations.jsonl")
    data5 = read_indent("role_conversations.jsonl")
    data6 = read_indent("self_conversations.jsonl")
    dir = "/home/pika/Project/chat-doraemon/data/double"
    files = list_jsonl_files(dir)
    data7 = []
    for file in files:
        data7.extend(read_indent(file))

    alldata = []
    for i in range(1,8):
        alldata.extend(eval(f"data{i}"))
    
    turned_data = convert_list_with_system(alldata,system_description=system_prompt)
    save_to_jsonl(turned_data,"merged.jsonl")

    


    



    
