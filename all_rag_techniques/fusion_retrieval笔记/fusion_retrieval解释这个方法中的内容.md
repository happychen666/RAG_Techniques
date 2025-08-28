`fusion_retrieval` 是一个用于文档检索的方法，核心思想是将**语义向量检索**（如 OpenAI Embeddings + FAISS）和**关键词检索**（如 BM25）进行融合，从而兼顾语义相关性和关键词匹配，提高检索效果和鲁棒性。

下面详细解释方法内容：

---

### 方法签名
```python
def fusion_retrieval(vectorstore, bm25, query: str, k: int = 5, alpha: float = 0.5) -> List[Document]:
```
- **vectorstore**：基于向量的文档检索对象（比如 FAISS）。
- **bm25**：关键词检索对象（BM25Okapi）。
- **query**：查询字符串（用户输入的问题或关键词）。
- **k**：返回的文档数量（Top K）。
- **alpha**：融合参数，控制语义检索和关键词检索的权重分配（0.5 时两者等权）。

---

### 步骤详解

1. **获取所有文档**  
   ```python
   all_docs = vectorstore.similarity_search("", k=vectorstore.index.ntotal)
   ```
   - 获取所有文档（chunks），用于后续排序和打分。

2. **BM25 关键词检索**  
   ```python
   bm25_scores = bm25.get_scores(query.split())
   ```
   - 用 BM25 算法计算每个文档和查询的关键词相关性分数。

3. **语义向量检索**  
   ```python
   vector_results = vectorstore.similarity_search_with_score(query, k=len(all_docs))
   vector_scores = np.array([score for _, score in vector_results])
   ```
   - 用向量检索方法计算每个文档与查询的语义相关性分数。

4. **归一化分数**  
   - 将两种分数归一化到相同的尺度，便于融合：
   ```python
   vector_scores = 1 - (vector_scores - np.min(vector_scores)) / (np.max(vector_scores) - np.min(vector_scores) + epsilon)
   bm25_scores = (bm25_scores - np.min(bm25_scores)) / (np.max(bm25_scores) -  np.min(bm25_scores) + epsilon)
   ```
   - `vector_scores` 归一化后越大表示相关性越高。

5. **分数加权融合**  
   ```python
   combined_scores = alpha * vector_scores + (1 - alpha) * bm25_scores
   ```
   - 用 `alpha` 参数控制两者权重，得到每个文档的融合分数。

6. **排序与返回**  
   ```python
   sorted_indices = np.argsort(combined_scores)[::-1]
   return [all_docs[i] for i in sorted_indices[:k]]
   ```
   - 按融合分数降序排序，返回分数最高的 `k` 个文档。

---

### 总结
- **优势**：融合了语义检索和关键词检索，适应多样化查询场景。
- **定制性**：可通过 `alpha` 灵活配置两者权重，满足不同需求。
- **应用场景**：适用于对语义和关键词都敏感的文档检索系统，提升检索全面性和准确性。

如果你还想进一步了解每一步的原理或代码细节，可以继续问！

--- 
 
 
    # Step 2: Perform BM25 search
    bm25_scores = bm25.get_scores(query.split())

    # Step 3: Perform vector search
    vector_results = vectorstore.similarity_search_with_score(query, k=len(all_docs))

这两行代码像一个黑盒子一样，我不懂，都没有检索结果，是如何计算每个文档与查询的相关性分数的？
# 第 2 步：执行 BM25 搜索
    bm25_scores = bm25.get_scores(query.split())

    # 第 3 步：执行向量搜索
    vector_results = vectorstore.similarity_search_with_score(query, k=len(all_docs))

这两行代码像一个黑盒子一样，我不懂，都没有检索结果，是如何计算每个文档与查询的相关性分数的？


你的疑问非常好！这两行代码确实是检索系统的核心，但它们用的是“黑盒”方式调用了两个检索引擎，下面我具体解释它们**如何计算每个文档和查询的相关性分数**：

---

## 1. BM25 检索（关键词相关性）

```python
bm25_scores = bm25.get_scores(query.split())
```
**原理：**
- BM25 是一种改进的 TF-IDF（词频-逆文档频率）算法。
- 它会把你的查询（query）分词，然后统计查询词在每个文档中的出现频率，并结合文档长度、词在整个语料中的出现情况，计算一个相关性分数。
- 得到的 `bm25_scores` 是一个列表，每个元素表示对应文档与查询的 BM25 相关性分数，分数越高说明关键词匹配越好。

**举例：**
- 查询为 "climate change impact"
- 如果某个文档多次出现这些词，并且词不是所有文档都常见，分数就高。

---

## 2. 向量检索（语义相关性）

```python
vector_results = vectorstore.similarity_search_with_score(query, k=len(all_docs))
```
**原理：**
- 向量检索是用 OpenAI Embeddings 把查询和所有文档都转成高维向量（比如 1536 维）。
- 然后用距离度量（如余弦距离）比较查询向量和每个文档向量的距离（通常距离越近相关性越高）。
- `similarity_search_with_score` 方法会返回每个文档和查询之间的相似度分数（通常分数越低距离越近，相关性越强）。

**举例：**
- 查询 "effects of climate change on environment"
- 如果某文档和查询在语义空间里距离最近，它的分数就高。

---

## 为什么没有直接“检索结果”而是分数？

- 这些分数是用来排序的，分数越高/距离越近，相关性越强。
- 最终会根据分数排序，选出 top k（比如 5）条相关性最高的文档作为检索结果。

---

## 总结
- **BM25**：计算关键词匹配相关性分数。
- **向量检索**：计算语义空间里的相关性分数。
- 这两个分数本质都是“文档和查询的相关性”，不过一个偏向“关键词”，一个偏向“语义”。

如果你想看**BM25 或向量检索的底层实现原理或公式**，也可以告诉我！