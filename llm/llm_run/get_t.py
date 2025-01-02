import pickle
import tqdm
import json

sentiment_choice = ["姜萍", "王闰秋", "阿里巴巴", "新闻媒体", "教育制度", "其他评论者", "无法判断"]

def get_word(text):
    text = text.lower()
    res_lst = [i for i in sentiment_choice if i.lower().startswith(text)]
    assert len(res_lst)==1, f"{breakpoint()}"
    return res_lst[0]

# with open("output/output_new_cache4.pkl","rb") as f:
#     data = pickle.load(f)
with open("output/t_output_0.json","r") as f:
    data = json.load(f)

dic = {}
diff_num = 0
statistic_dic = {}
for datai in data:
    tar_id = get_word(datai['output'])
    dic[datai['tag']] = tar_id
    statistic_dic[tar_id] = statistic_dic.get(tar_id,0) + 1
print(statistic_dic)
with open("target0.json","w") as f:
    json.dump(dic,f,indent=4, ensure_ascii=False)



# with open("emotion1.json","r") as f:
#     data = json.load(f)

# with open("emotion.json","r") as f:
#     data2 = json.load(f)

# diff_num = 0
# for key in data:
#     if data[key] != data2[key]:
#         diff_num += 1

# print(diff_num)