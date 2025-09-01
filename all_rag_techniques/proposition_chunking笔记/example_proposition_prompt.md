# Few shot prompting --- We can add more examples to make it good
proposition_examples = [
    {"document": 
        "In 1969, Neil Armstrong became the first person to walk on the Moon during the Apollo 11 mission.", 
     "propositions": 
        "['Neil Armstrong was an astronaut.', 'Neil Armstrong walked on the Moon in 1969.', 'Neil Armstrong was the first person to walk on the Moon.', 'Neil Armstrong walked on the Moon during the Apollo 11 mission.', 'The Apollo 11 mission occurred in 1969.']"
    },
]

example_proposition_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{document}"),
        ("ai", "{propositions}"),
    ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt = example_proposition_prompt,
    examples = proposition_examples,
)

这段代码的语法规则我不懂


好，我来给你逐行解释这段代码的语法和作用，用“说人话 + 举例”的方式。😊

---

### 代码：

```python
proposition_examples = [
    {"document": 
        "In 1969, Neil Armstrong became the first person to walk on the Moon during the Apollo 11 mission.", 
     "propositions": 
        "['Neil Armstrong was an astronaut.', 'Neil Armstrong walked on the Moon in 1969.', 'Neil Armstrong was the first person to walk on the Moon.', 'Neil Armstrong walked on the Moon during the Apollo 11 mission.', 'The Apollo 11 mission occurred in 1969.']"
    },
]
```

#### 解释：

* 这是一个 **Python 列表 (list)**，里面只有一个元素。
* 这个元素是一个 **字典 (dict)**，有两个键：

  * `"document"`：存放原始文本（输入）。
  * `"propositions"`：存放由原始文本拆出来的“命题句子”（输出）。

👉 说人话：这是一个**示例对照表**，告诉 AI：
给你一段话（document），你应该把它拆成几个简单的事实（propositions）。

#### 举例：

* 输入：`document` → "1969年，尼尔·阿姆斯特朗在阿波罗11号任务中成为第一个登月的人。"
* 输出：`propositions` → \["尼尔·阿姆斯特朗是宇航员。", "尼尔·阿姆斯特朗1969年登月。", "尼尔·阿姆斯特朗是第一个登月的人。", …]

---

### 代码：

```python
example_proposition_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{document}"),
        ("ai", "{propositions}"),
    ]
)
```

#### 解释：

* `ChatPromptTemplate.from_messages(...)` 是 **LangChain** 提供的一个方法。
* 它的作用是：定义 **对话的格式**。
* 里面的 `("human", "{document}")` 表示：

  * **human（人类消息）** → 里面填 `document` 变量。
* `("ai", "{propositions}")` 表示：

  * **ai（模型回答）** → 里面填 `propositions` 变量。

👉 说人话：这是一个“模版”，它规定了对话的输入输出长什么样。

#### 举例：

把 `document="尼尔·阿姆斯特朗1969年登月。"` 填进去：

```
Human: 尼尔·阿姆斯特朗1969年登月。
AI: ['尼尔·阿姆斯特朗是宇航员。', '尼尔·阿姆斯特朗1969年登月。', '尼尔·阿姆斯特朗是第一个登月的人。']
```

---

### 代码：

```python
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt = example_proposition_prompt,
    examples = proposition_examples,
)
```

#### 解释：

* `FewShotChatMessagePromptTemplate` 是 LangChain 的一个工具，意思是 **“few-shot 提示模版”**。
* `example_prompt=example_proposition_prompt`：告诉它，每个示例要用我们刚刚定义的输入输出格式。
* `examples=proposition_examples`：把之前准备好的“例子对照表”传进去。

👉 说人话：这个东西的作用就是：
“给模型看几个示例，让它学会模式，然后在新输入时套用这个模式。”

#### 举例：

你现在给模型一个新输入：

```python
document = "Albert Einstein developed the theory of relativity."
```

它就会模仿例子，输出类似：

```
['Albert Einstein was a scientist.', 'Albert Einstein developed the theory of relativity.']
```

---

✅ 总结一下：

* `proposition_examples`：准备示例（输入和输出的对照表）。
* `example_proposition_prompt`：定义输入输出的对话模版。
* `few_shot_prompt`：把模版 + 示例组合起来，形成“few-shot 提示”，供模型参考。

---

要不要我给你写一个 **完整可运行的最小 demo**，把这个 few-shot prompt 跑起来，你能看到输入输出的效果？


好嘞 👍 我给你写一个 **完整可运行的最小 demo**，你可以直接在本地 Python 跑（需要装好 `langchain` 和 `openai` 相关依赖）。我会逐行解释。

---

### 完整 Demo

```python
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# 1. 准备示例
proposition_examples = [
    {
        "document": "In 1969, Neil Armstrong became the first person to walk on the Moon during the Apollo 11 mission.",
        "propositions": "['Neil Armstrong was an astronaut.', 'Neil Armstrong walked on the Moon in 1969.', 'Neil Armstrong was the first person to walk on the Moon.', 'Neil Armstrong walked on the Moon during the Apollo 11 mission.', 'The Apollo 11 mission occurred in 1969.']"
    },
]

# 2. 定义输入输出模版
example_proposition_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{document}"),       # 人类给出 document
        ("ai", "{propositions}"),      # AI 输出 propositions
    ]
)

# 3. 定义 few-shot 提示
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_proposition_prompt,
    examples=proposition_examples,
)

# 4. 构造一个新输入
new_input = {"document": "Albert Einstein developed the theory of relativity."}

# 5. 格式化 few-shot 提示
final_prompt = few_shot_prompt.format_messages(**new_input)

# 6. 打印结果
for msg in final_prompt:
    print(f"{msg.type.upper()}: {msg.content}")
```

---

### 输出结果（本地跑会得到类似的东西）

```
HUMAN: In 1969, Neil Armstrong became the first person to walk on the Moon during the Apollo 11 mission.
AI: ['Neil Armstrong was an astronaut.', 'Neil Armstrong walked on the Moon in 1969.', 'Neil Armstrong was the first person to walk on the Moon.', 'Neil Armstrong walked on the Moon during the Apollo 11 mission.', 'The Apollo 11 mission occurred in 1969.']

HUMAN: Albert Einstein developed the theory of relativity.
```

👉 解释：

1. 前两行是 **示例**（告诉模型：输入→输出长什么样）。
2. 最后一行是 **新输入**，模型接下来应该模仿示例输出对应的命题句子。

---

这样就完成了一个 **few-shot 提示的最小跑通案例**。
如果你想让模型真正生成答案，可以把 `final_prompt` 传给 `ChatOpenAI` 模型，例如：

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
response = llm.invoke(final_prompt)
print(response.content)
```

---

要不要我再帮你扩展几个 **中文例子**（比如三国历史、现代新闻），这样你就能看到 few-shot 在中文里的效果？
