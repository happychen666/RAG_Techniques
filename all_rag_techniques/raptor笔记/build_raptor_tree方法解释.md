

def build_raptor_tree(texts: List[str], max_levels: int = 3) -> Dict[int, pd.DataFrame]:
    """Build the RAPTOR tree structure with level metadata and parent-child relationships."""
    results = {}
    current_texts = [extract_text(text) for text in texts]
    current_metadata = [{"level": 0, "origin": "original", "parent_id": None} for _ in texts]
    
    for level in range(1, max_levels + 1):
        logging.info(f"Processing level {level}")
        
        embeddings = embed_texts(current_texts)
        n_clusters = min(10, len(current_texts) // 2)
        cluster_labels = perform_clustering(np.array(embeddings), n_clusters)
        
        df = pd.DataFrame({
            'text': current_texts,
            'embedding': embeddings,
            'cluster': cluster_labels,
            'metadata': current_metadata
        })
        
        results[level-1] = df
        
        summaries = []
        new_metadata = []
        for cluster in df['cluster'].unique():
            cluster_docs = df[df['cluster'] == cluster]
            cluster_texts = cluster_docs['text'].tolist()
            cluster_metadata = cluster_docs['metadata'].tolist()
            summary = summarize_texts(cluster_texts)
            summaries.append(summary)
            new_metadata.append({
                "level": level,
                "origin": f"summary_of_cluster_{cluster}_level_{level-1}",
                "child_ids": [meta.get('id') for meta in cluster_metadata],
                "id": f"summary_{level}_{cluster}"
            })
        
        current_texts = summaries
        current_metadata = new_metadata
        
        if len(current_texts) <= 1:
            results[level] = pd.DataFrame({
                'text': current_texts,
                'embedding': embed_texts(current_texts),
                'cluster': [0],
                'metadata': current_metadata
            })
            logging.info(f"Stopping at level {level} as we have only one summary")
            break
    
    return results

解释这段代码的含义和作用，说人话，并举例说明


好的，这段代码实现了一个 **RAPTOR 树状摘要结构** 的构建逻辑。通俗来说，它就是把一大堆文本 **分层聚类、分层总结**，形成一个 “树形摘要” 的结构，每层的文本是上一层聚类的总结，直到最终得到一个或少量的高层总结。下面我来详细逐行解释，并配上例子。

---

## 1. 函数定义

```python
def build_raptor_tree(texts: List[str], max_levels: int = 3) -> Dict[int, pd.DataFrame]:
    """Build the RAPTOR tree structure with level metadata and parent-child relationships."""
```

* `texts`：输入的原始文本列表
* `max_levels`：最多生成多少层的树，默认 3 层
* 返回值：字典 `results`，每一层是一个 `DataFrame`，包含：

  * 文本（原文或总结）
  * embedding
  * 聚类标签
  * 元数据（记录层级、父子关系、来源等）

---

## 2. 初始化

```python
results = {}
current_texts = [extract_text(text) for text in texts]
current_metadata = [{"level": 0, "origin": "original", "parent_id": None} for _ in texts]
```

* `results`：存放每层的 DataFrame
* `current_texts`：保证输入文本都是字符串
* `current_metadata`：每条文本的元信息，初始都是第 0 层，来源是 “original”，没有父节点

**例子**：

```python
texts = ["苹果是水果", "香蕉是水果", "老虎是动物"]
current_metadata = [
  {"level":0, "origin":"original", "parent_id":None},
  {"level":0, "origin":"original", "parent_id":None},
  {"level":0, "origin":"original", "parent_id":None}
]
```

---

## 3. 遍历每一层

```python
for level in range(1, max_levels + 1):
    logging.info(f"Processing level {level}")
    
    embeddings = embed_texts(current_texts)
    n_clusters = min(10, len(current_texts) // 2)
    cluster_labels = perform_clustering(np.array(embeddings), n_clusters)
```

* 每一层：

  1. 对当前文本生成 embedding
  2. 根据文本数量决定聚类数（最多 10，或者文本数的一半）
  3. 执行聚类，得到每条文本的类别

**例子**：

```python
# 第1层
current_texts = ["苹果是水果", "香蕉是水果", "老虎是动物"]
# 聚类结果 labels 可能是 [0,0,1]
```

---

## 4. 构建 DataFrame 保存本层结果

```python
df = pd.DataFrame({
    'text': current_texts,
    'embedding': embeddings,
    'cluster': cluster_labels,
    'metadata': current_metadata
})
results[level-1] = df
```

* 每层都保存一个 DataFrame，方便后续分析或可视化
* `results[level-1]`：层数从 0 开始记录

---

## 5. 对每个聚类生成总结

```python
summaries = []
new_metadata = []
for cluster in df['cluster'].unique():
    cluster_docs = df[df['cluster'] == cluster]
    cluster_texts = cluster_docs['text'].tolist()
    cluster_metadata = cluster_docs['metadata'].tolist()
    summary = summarize_texts(cluster_texts)
    summaries.append(summary)
    new_metadata.append({
        "level": level,
        "origin": f"summary_of_cluster_{cluster}_level_{level-1}",
        "child_ids": [meta.get('id') for meta in cluster_metadata],
        "id": f"summary_{level}_{cluster}"
    })
```

* 对每个聚类：

  1. 找出属于这个聚类的文本
  2. 生成总结
  3. 保存新的元数据，包括：

     * 层级
     * 来源（哪一层的哪个聚类总结的）
     * 子节点 ID
     * 当前 summary 的 ID

**例子**：

```python
cluster 0 -> ["苹果是水果", "香蕉是水果"]  
summary -> "这些都是水果"
new_metadata -> {"level":1, "origin":"summary_of_cluster_0_level_0", "child_ids":[None,None], "id":"summary_1_0"}

cluster 1 -> ["老虎是动物"]
summary -> "老虎是动物"
new_metadata -> {"level":1, "origin":"summary_of_cluster_1_level_0", "child_ids":[None], "id":"summary_1_1"}
```

---

## 6. 更新当前文本和元数据

```python
current_texts = summaries
current_metadata = new_metadata
```

* 下一层用当前聚类的总结作为输入文本
* 元数据也更新为当前 summary 的元信息

---

## 7. 停止条件

```python
if len(current_texts) <= 1:
    results[level] = pd.DataFrame({
        'text': current_texts,
        'embedding': embed_texts(current_texts),
        'cluster': [0],
        'metadata': current_metadata
    })
    logging.info(f"Stopping at level {level} as we have only one summary")
    break
```

* 如果当前层只剩一条文本（已经是顶层总结），就停止
* 也会保存最后一层的 DataFrame

---

## 8. 返回结果

```python
return results
```

* 返回一个字典 `results`，每层是一个 DataFrame
* 每层文本都有 embedding、聚类标签和元数据
* 形成 **树状结构**，可以追溯每条 summary 的来源和子节点

---

## 🌟 总结

这个函数做的事情就是：

1. 将原始文本分组聚类
2. 对每个聚类生成总结
3. 把这些总结作为下一层的文本继续聚类
4. 形成一个多层的 **RAPTOR 树**
5. 每条 summary 都保存了父子关系信息

---

## 一个完整例子

```python
texts = [
    "苹果是水果", "香蕉是水果", "老虎是动物", "狮子是动物", "中国是国家", "美国是国家"
]

tree = build_raptor_tree(texts, max_levels=3)
```

* **第0层**：原始文本
* **第1层**：水果类、动物类、国家类总结
* **第2层**：把三类总结再总结成一句话：
  `"这些文本涵盖水果、动物和国家信息"`
* 每条 summary 都有元数据，可以追溯来源

---

如果你愿意，我可以画一张 **RAPTOR 树示意图**，把每层聚类和总结可视化，看起来更直观。

你想让我画吗？

---


df['cluster'].unique()为什么要这么处理一下？

好问题 👍，我们来拆解一下

---

### 1. 背景代码

在你的函数里，有这么一段：

```python
for cluster in df['cluster'].unique():
    cluster_docs = df[df['cluster'] == cluster]
    ...
```

---

### 2. `df['cluster']` 是啥？

* 这是 DataFrame 中的一列，存的是每条文本所属的 **聚类标签**（比如 0,1,2...）。
* 举个例子：

```python
text           cluster
苹果是水果       0
香蕉是水果       0
老虎是动物       1
```

这里 `df['cluster'] = [0, 0, 1]`

---

### 3. `unique()` 的作用

* `.unique()` 会提取这一列中 **所有不重复的值**
* 上例：

```python
df['cluster'].unique()
# 输出 array([0, 1])
```

也就是说，我们得到了“有多少个簇”以及“簇的编号”。

---

### 4. 为什么要这么做？

因为我们要 **按簇循环处理**，否则就没法区分每个簇里的文本。

举个例子：

```python
for cluster in df['cluster'].unique():
    cluster_docs = df[df['cluster'] == cluster]
    print(f"簇 {cluster} 包含的文本：", cluster_docs['text'].tolist())
```

输出可能是：

```
簇 0 包含的文本： ['苹果是水果', '香蕉是水果']
簇 1 包含的文本： ['老虎是动物']
```

这样就能对每个簇单独总结、生成新 metadata。

---

### 5. 如果不 `.unique()` 会怎样？

* 假设直接：

```python
for cluster in df['cluster']:
    ...
```

那循环会遍历每一行的 cluster 值，比如 `[0,0,1]`，结果是会重复处理簇 0 两次。
最后你会重复生成 **簇 0 的摘要**，逻辑就乱了。

---

✅ **总结一句人话**：
`.unique()` 就是为了 **去重**，只拿“每个簇的编号一次”，从而能对簇做一次总结。否则就会重复处理。

---

要不要我给你写个小实验，展示 `.unique()` 和不用 `.unique()` 的区别？

---

        for cluster in df['cluster'].unique():
            cluster_docs = df[df['cluster'] == cluster]
            cluster_texts = cluster_docs['text'].tolist()
            cluster_metadata = cluster_docs['metadata'].tolist()
            summary = summarize_texts(cluster_texts)
            summaries.append(summary)
            new_metadata.append({
                "level": level,
                "origin": f"summary_of_cluster_{cluster}_level_{level-1}",
                "child_ids": [meta.get('id') for meta in cluster_metadata],
                "id": f"summary_{level}_{cluster}"
            })

这里面df[df['cluster'] == cluster]这么取值不就可以取到重复的值了么，下面的取值结果是什么样的？举例说明


👌 你提的点非常关键，我们来仔细拆解：

---

### 1. `df[df['cluster'] == cluster]` 是啥意思？

这是 **布尔索引**：

* `df['cluster'] == cluster` 会生成一个布尔数组，标记哪些行属于这个簇。
* 然后 `df[...]` 就会筛选出这些行。

---

### 2. 举个例子

假设我们有一个小 DataFrame：

```python
import pandas as pd

df = pd.DataFrame({
    "text": ["苹果是水果", "香蕉是水果", "老虎是动物", "西瓜是水果"],
    "cluster": [0, 0, 1, 0],
    "metadata": [
        {"id": "t1"}, {"id": "t2"}, {"id": "t3"}, {"id": "t4"}
    ]
})
print(df)
```

表格长这样：

| index | text  | cluster | metadata    |
| ----- | ----- | ------- | ----------- |
| 0     | 苹果是水果 | 0       | {"id":"t1"} |
| 1     | 香蕉是水果 | 0       | {"id":"t2"} |
| 2     | 老虎是动物 | 1       | {"id":"t3"} |
| 3     | 西瓜是水果 | 0       | {"id":"t4"} |

---

### 3. 循环逻辑

先取 `df['cluster'].unique()` → `[0, 1]`
所以只会循环两次：一次 `cluster=0`，一次 `cluster=1`。

#### 第一次循环（`cluster=0`）

```python
cluster_docs = df[df['cluster'] == 0]
```

得到：

| index | text  | cluster | metadata    |
| ----- | ----- | ------- | ----------- |
| 0     | 苹果是水果 | 0       | {"id":"t1"} |
| 1     | 香蕉是水果 | 0       | {"id":"t2"} |
| 3     | 西瓜是水果 | 0       | {"id":"t4"} |

然后：

```python
cluster_texts = ["苹果是水果", "香蕉是水果", "西瓜是水果"]
cluster_metadata = [{"id":"t1"}, {"id":"t2"}, {"id":"t4"}]
```

#### 第二次循环（`cluster=1`）

```python
cluster_docs = df[df['cluster'] == 1]
```

得到：

| index | text  | cluster | metadata    |
| ----- | ----- | ------- | ----------- |
| 2     | 老虎是动物 | 1       | {"id":"t3"} |

然后：

```python
cluster_texts = ["老虎是动物"]
cluster_metadata = [{"id":"t3"}]
```

---

### 4. 那“会不会重复取值”？

不会。
因为外层循环是 `for cluster in df['cluster'].unique():`，
每个 `cluster` 只会出现一次（0 和 1 各一次）。

虽然 `df[df['cluster'] == cluster]` 会取到多个行（比如 cluster=0 有三条），
但这是我们想要的效果：**把同一个簇的所有文本收集在一起**，而不是重复生成摘要。

---

✅ **总结人话版**：
`df[df['cluster'] == cluster]` 就是“把所有属于这个簇的行都筛出来”。

* 如果 cluster=0 → 得到所有 cluster=0 的文本（可能好几条）。
* 如果 cluster=1 → 得到所有 cluster=1 的文本（可能只有一条）。
  然后对每个簇做一次总结，避免重复处理。

---

要不要我写一段真实 Python 代码，把 `cluster_texts` 和 `cluster_metadata` 的结果打印出来给你看？


运行结果出来了 ✅

循环时：

* **簇 0**

  ```python
  cluster_texts = ['苹果是水果', '香蕉是水果', '西瓜是水果']
  cluster_metadata = [{'id': 't1'}, {'id': 't2'}, {'id': 't4'}]
  ```

* **簇 1**

  ```python
  cluster_texts = ['老虎是动物']
  cluster_metadata = [{'id': 't3'}]
  ```

---

所以 `df[df['cluster'] == cluster]` 的结果是：
👉 把属于某个簇的所有行筛出来，得到该簇对应的文本和 metadata 列表。

要不要我再帮你画个图，把 **原始表格 → 按 cluster 分组 → 得到 cluster\_texts & cluster\_metadata** 的过程画出来？
