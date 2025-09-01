这个问题问得特别好 👍。
表面看 `build_raptor_tree` 里的 `results` 确实就是一个字典：

```python
{
  0: DataFrame(level=0的原始文本),
  1: DataFrame(level=1的摘要),
  2: DataFrame(level=2的摘要),
  ...
}
```

好像只是“层号 → DataFrame”，确实不长得像一棵“树 🌲”。
但为什么作者说它是树结构呢？我们来剖开看看。

---

## 1. 树的本质是什么？

一棵树的关键不在于**存储形式长得像树**，而在于：

* 节点（node）：就是一条文本/摘要。
* 边（edge）：表示父子关系。

只要能描述“某个节点的孩子是谁”，那就是一棵树。

---

## 2. `build_raptor_tree` 怎么体现父子关系？

在这段代码里，父子关系藏在 **metadata** 里：

```python
new_metadata.append({
    "level": level,
    "origin": f"summary_of_cluster_{cluster}_level_{level-1}",
    "child_ids": [meta.get('id') for meta in cluster_metadata],  # 👈 孩子是谁
    "id": f"summary_{level}_{cluster}"
})
```

* `id`：给当前摘要生成唯一标识，比如 `"summary_1_0"`。
* `child_ids`：指向这个摘要对应的孩子节点们（上层的原始文本或者下层的摘要）。

所以虽然 `results` 表面只是字典，但每个 DataFrame 的 `metadata` 字段里其实“指针”式地把树结构链接起来了。

---

## 3. 举个例子 📖

假设原始文本有 3 条：

```python
Level 0
t1 = "苹果是水果"
t2 = "香蕉是水果"
t3 = "老虎是动物"
```

分簇后 Level 1 可能是：

```python
summary_1_0 = "水果类总结"
metadata={"id":"summary_1_0", "child_ids":["t1","t2"]}

summary_1_1 = "动物类总结"
metadata={"id":"summary_1_1", "child_ids":["t3"]}
```

如果继续往上合并成 Level 2：

```python
summary_2_0 = "全部内容总结"
metadata={"id":"summary_2_0", "child_ids":["summary_1_0","summary_1_1"]}
```

结果 `results` 就是：

```python
{
  0: df(level=0, texts=[t1, t2, t3]),
  1: df(level=1, texts=[summary_1_0, summary_1_1]),
  2: df(level=2, texts=[summary_2_0])
}
```

**虽然是字典，但通过 metadata 的 `child_ids`，你可以还原出一个树状结构**：

```
            summary_2_0
           /            \
  summary_1_0          summary_1_1
   /     \                   |
  t1     t2                  t3
```

---

## 4. 总结人话版

* `results` 看起来只是“层号 → DataFrame”，确实不像树。
* 但树的“父子关系”信息都藏在每条记录的 **metadata** 里（特别是 `child_ids` 字段）。
* 你要画树，只需要递归地顺着 `id` 和 `child_ids` 往下走，就能还原成真正的树结构。

---

要不要我帮你写一段小代码，把 `results` 转成一个真正的树状 JSON（父节点带孩子列表），这样你就能直观看到“字典 → 树”的转化？
