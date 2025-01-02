import pickle
import tqdm
import json

sentiment_choice = ["Anger","Sympathy", "Appreciation", "Sadness", "Surprise", "Confusion", "Amusement","Unable to Determine"]

def get_word(text):
    text = text.lower()
    res_lst = [i for i in sentiment_choice if i.lower().startswith(text)]
    assert len(res_lst)==1
    return res_lst[0]

# with open("output/output_new_cache4.pkl","rb") as f:
#     data = pickle.load(f)
with open("output/output_new10.json","r") as f:
    data = json.load(f)

dic = {}
diff_num = 0
for datai in data:
    dic[datai['tag']] = get_word(datai['output'])
with open("emotion_new_cache10.json","w") as f:
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