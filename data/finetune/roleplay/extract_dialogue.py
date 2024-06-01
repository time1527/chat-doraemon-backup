# mainly by chatgpt
import re
import os
import json
import pandas as pd
from datetime import datetime


def time_difference(start_time, end_time):
    # 定义时间格式
    time_format = '%H:%M:%S.%f'
    
    # 将时间字符串解析为datetime对象
    start_dt = datetime.strptime(start_time, time_format)
    end_dt = datetime.strptime(end_time, time_format)
    
    # 计算时间差
    difference = end_dt - start_dt
    
    # 返回时间差的秒数
    return difference.total_seconds()


def extract_dialogue(csv_path,interval = 1):
    # 读取CSV文件
    df = pd.read_csv(csv_path)
    df = df.rename(columns=lambda x: x.strip().replace(" ", ""))

    # 初始化变量
    result = []
    current_speaker = None
    current_dialogue = ""
    prev_end_time = None

    for index, row in df.iterrows():
        if current_speaker == row['人物'] and time_difference(row['开始时间'],prev_end_time) <= interval:
            # 合并当前对话
            current_dialogue +=  "，" + re.sub(r'\s+', '，', row['人物台词'].replace(","," "))
            prev_end_time = row['结束时间']
        else:
            if current_dialogue:
                # 将之前合并的对话添加到结果中
                result.append([current_speaker, current_dialogue, current_start_time, prev_end_time])
            # 开始新的对话
            current_speaker = row['人物']
            current_dialogue = re.sub(r'\s+', '，', row['人物台词'].replace(","," "))
            current_start_time = row['开始时间']
            prev_end_time = row['结束时间']

    # 添加最后一个对话
    if current_dialogue:
        result.append([current_speaker, current_dialogue, current_start_time, prev_end_time])

    # 将结果转换为DataFrame
    result_df = pd.DataFrame(result, columns=['人物', '人物台词', '开始时间', '结束时间'])

    merged_df = result_df.copy()

    # 提取符合条件的多轮对话
    dialogue_list = []
    i = 0
    dialogue_round = []
    while i < len(merged_df) - 1:
        current_row = merged_df.iloc[i]
        # if i + 1 > len(merged_df) - 1:
            # [dialogue_round[i].update({"role": "user" if i % 2 == 0 else "assistant"}) for i in range(len(dialogue_round))]
            # dialogue_list.append({"conversation":dialogue_round})
            # break
        next_row = merged_df.iloc[i + 1]

        if (current_row['人物'] != '哆啦A梦'  
            and next_row['人物'] == '哆啦A梦' 
            and time_difference(current_row['结束时间'],next_row['开始时间']) <= interval
            ):
            
            # 初始化对话轮次
            dialogue_round = [{
                "role": current_row['人物'],
                "content": current_row['人物台词']
            }]
            
            # 记录非哆啦A梦的角色
            non_doraemon_role = current_row['人物']
            
            # 添加哆啦A梦的回复
            dialogue_round.append({
                "role": next_row['人物'],
                "content": next_row['人物台词']
            })
            
            # 继续检查下一对对话
            i += 2
            while i < len(merged_df) - 1:
                # next_row = merged_df.iloc[i]
                current_row = merged_df.iloc[i]
                if i + 1 > len(merged_df) - 1:
                    break
                next_row = merged_df.iloc[i + 1]
                if (next_row['人物'] == '哆啦A梦' 
                    and current_row['人物'] == non_doraemon_role
                    and time_difference(current_row['结束时间'],next_row['开始时间']) <= interval
                    and time_difference(merged_df.iloc[i-1]['结束时间'],current_row['开始时间']) <= interval
                    # and current_row['结束时间'] == next_row['开始时间'] 
                    # and current_row['开始时间'] == merged_df.iloc[i-1]['结束时间']
                    ):
                    
                    dialogue_round.append({
                        "role": current_row['人物'],
                        "content": current_row['人物台词']
                        })
                    # 添加哆啦A梦的回复
                    dialogue_round.append({
                        "role": next_row['人物'],
                        "content": next_row['人物台词']
                    })
                    i += 2
                else:
                    break
            [dialogue_round[i].update({"role": "user" if i % 2 == 0 else "assistant"}) for i in range(len(dialogue_round))]
            dialogue_list.append({"conversation":dialogue_round})
        else:
            i += 1

    # # 打印结果
    # for dialogue in dialogue_list:
    #     print(dialogue)
    return dialogue_list


def get_csv_paths(folder_path,l,r):
    paths = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # 提取文件名中的数字部分
            number_str = filename.split('.')[0]
            
            # 确保提取的部分是数字
            if number_str.isdigit():
                number = int(number_str)
                
                if number >= l and number < r:
                    paths.append(os.path.join(folder_path, filename))
    return paths


def gen_dialogue(dir,l,r,interval):
    csv_paths = get_csv_paths(dir,l,r)
    all = []
    for path in csv_paths:
        # print(path)
        all.extend(extract_dialogue(path,interval))
    output_file_path = f'{l}-{r}.jsonl'
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for item in all:
            json_item = json.dumps(item, ensure_ascii=False, indent=4)
            output_file.write(json_item + '\n')
    print(f"finish {len(all)}")

if __name__ == "__main__":
    gen_dialogue('/home/pika/Videos/final',374,384,5)