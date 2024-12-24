import json
import matplotlib.pyplot as plt

with open(r"F:\图片\sp\2024_fall\信息内容安全\大作业\bilibili\processed_data\json\没有做的代价.json","r",encoding="utf-8") as f:
    data = json.load(f)

time_data = []
for i in data:
    time_data.append(data[i]['time'])

print(time_data)
plt.hist(time_data, bins=10, density=True)

# 设置图表标题和坐标轴标签
plt.title('Frequency Distribution Histogram')
plt.xlabel('Value')
plt.ylabel('Probability Density')

# 显示图表
plt.show()