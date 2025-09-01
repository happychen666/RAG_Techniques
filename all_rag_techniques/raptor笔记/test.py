import pandas as pd
import matplotlib.pyplot as plt

# 构造一个模拟 DataFrame
data = {
    "text": ["苹果是水果", "香蕉是水果", "老虎是动物"],
    "metadata": [
        {"level": 0, "origin": "original", "id": "t1"},
        {"level": 0, "origin": "original", "id": "t2"},
        {"level": 0, "origin": "original", "id": "t3"},
    ]
}
df = pd.DataFrame(data)

# 提取 Series 和 List
series_metadata = df["metadata"]
list_metadata = df["metadata"].tolist()

# 准备绘制图示文字
df_str = "DataFrame (df)\n----------------\nindex | text       | metadata\n0     | 苹果是水果  | {...}\n1     | 香蕉是水果  | {...}\n2     | 老虎是动物  | {...}"
series_str = "Series (df['metadata'])\n------------------------\n0    {...}\n1    {...}\n2    {...}"
list_str = "List (df['metadata'].tolist())\n-------------------------------\n[\n  {'level':0,'origin':'original','id':'t1'},\n  {'level':0,'origin':'original','id':'t2'},\n  {'level':0,'origin':'original','id':'t3'}\n]"

# 画一个流程图示意
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis("off")

ax.text(0.1, 0.7, df_str, fontsize=10, family="monospace", bbox=dict(facecolor="lightyellow", edgecolor="black"))
ax.text(0.5, 0.7, series_str, fontsize=10, family="monospace", bbox=dict(facecolor="lightblue", edgecolor="black"))
ax.text(0.5, 0.3, list_str, fontsize=10, family="monospace", bbox=dict(facecolor="lightgreen", edgecolor="black"))

# 画箭头
ax.annotate("", xy=(0.45, 0.7), xytext=(0.3, 0.7),
            arrowprops=dict(arrowstyle="->", lw=2))
ax.annotate("", xy=(0.55, 0.55), xytext=(0.55, 0.65),
            arrowprops=dict(arrowstyle="->", lw=2))
plt.show()
