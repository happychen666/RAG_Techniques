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

这段语法我不懂
  ("human", "{document}"),
        ("ai", "{propositions}"),
这个是啥，怎么用

你问的这段代码：

```python
("human", "{document}"),
("ai", "{propositions}"),
```

是在使用 **LangChain** 中的 **`ChatPromptTemplate.from_messages`** 方法，用于定义 **对话格式的提示模版**。这语法是 LangChain 的一种“对话模板构建方式”，看起来像是一个聊天记录的抽象表示。

---

## 🔍 我来详细解释每一部分，帮你“说人话”理解：

---

### ✅ 1. 什么是 `(“human”, “…”), (“ai”, “…”)` ？

它代表了一段**人类和 AI 的对话记录格式**，通常用于“提示模板”构造。

你可以理解成这样一个对话：

```text
人类说：{document}
AI 回复：{propositions}
```

这对 LangChain 来说，就是在构造 few-shot 的对话例子。

---

### ✅ 2. 这些变量 `{document}` 和 `{propositions}` 是干嘛的？

它们是 **占位符变量**（也叫模板变量），会在后续被你实际的输入数据替换掉。

你设置一个样板，等后面使用的时候，把数据喂进去，LangChain 会自动替换成你给的真实内容。

---

### ✅ 3. 举个完整例子帮你理解（模拟执行）

#### 定义的示例（proposition\_examples）是这样的：

```python
{
  "document": "In 1969, Neil Armstrong became the first person to walk on the Moon during the Apollo 11 mission.",
  "propositions": [
    "Neil Armstrong was an astronaut.",
    "Neil Armstrong walked on the Moon in 1969.",
    "Neil Armstrong was the first person to walk on the Moon.",
    "Neil Armstrong walked on the Moon during the Apollo 11 mission.",
    "The Apollo 11 mission occurred in 1969."
  ]
}
```

LangChain会把这个样本自动转换为这样的 prompt 模板示例：

```text
人类（human）：
In 1969, Neil Armstrong became the first person to walk on the Moon during the Apollo 11 mission.

AI（ai）：
- Neil Armstrong was an astronaut.
- Neil Armstrong walked on the Moon in 1969.
- Neil Armstrong was the first person to walk on the Moon.
- Neil Armstrong walked on the Moon during the Apollo 11 mission.
- The Apollo 11 mission occurred in 1969.
```

这个“人类提问 + AI 回复”的对话例子，就是用来做 **few-shot prompt 提示的样本**。

---

### ✅ 4. 所以 `FewShotChatMessagePromptTemplate` 是干嘛的？

它把上面的示例对话**包装成一个 few-shot 提示集**，你可以用这个提示来引导 GPT 继续按这个风格回答：

```python
few_shot_prompt.format(
    document="The Eiffel Tower is located in Paris and was completed in 1889."
)
```

最终提示内容会像这样传给模型👇：

```text
人类：
In 1969, Neil Armstrong became the first person to walk on the Moon during the Apollo 11 mission.
AI：
- Neil Armstrong was an astronaut.
- Neil Armstrong walked on the Moon in 1969.
- ...

人类：
The Eiffel Tower is located in Paris and was completed in 1889.
AI：
...
```

也就是告诉模型：**“请你模仿我上面的示例，把下面这个文本转成简洁、自包含的命题。”**

---

## 🧠 总结一句话

```python
("human", "{document}"),
("ai", "{propositions}")
```

就是定义了一种“对话格式”的 few-shot 示例模板：

* `human` 表示输入文档
* `ai` 表示输出的命题
* `{}` 是占位符，用于后续填充内容

你在给模型构建提示的时候，用这种方式能模拟“人类和 AI 的对话逻辑”，从而实现更高质量的输出。

---

如果你想我帮你写一个完整可运行的版本，来跑一个新的 document -> proposition 的例子，也可以告诉我要用哪种模型（OpenAI、Mistral、Qwen等等），我可以帮你补上代码。

---

我理解的是把proposition_examples 中的document和propositions放到example_proposition_prompt 中构成一个few_shot_prompt 么？？那few_shot_prompt 最终的数据是什么样的？？

你理解得\*\*非常对！\*\*👏

是的，你的理解可以这样表述：

> 👉 **把 `proposition_examples` 中的每一组 `{document, propositions}` 用 `example_proposition_prompt` 格式包装起来，构成多个示例对话，然后一起组成 `few_shot_prompt`，作为提示给语言模型做 few-shot learning。**

---

## ✅ 那么你问的重点：

> ❓“`few_shot_prompt` 最终的数据是什么样的？”

我来 **非常详细地告诉你：它是一个**“模拟的多轮对话记录”，每一轮是一组 Few-Shot 示例，格式大概如下👇

---

## 📦 最终结构样例（用 `format_messages()` 展开后）：

假设你定义了这样一个 `proposition_examples`：

```python
proposition_examples = [
    {
        "document": "In 1969, Neil Armstrong became the first person to walk on the Moon during the Apollo 11 mission.",
        "propositions": [
            "Neil Armstrong walked on the Moon in 1969.",
            "Neil Armstrong was the first person to walk on the Moon.",
            "Neil Armstrong participated in the Apollo 11 mission.",
            "The Apollo 11 mission took place in 1969."
        ]
    }
]
```

执行这个：

```python
few_shot_prompt.format_messages()
```

你会得到一个这样的结构（LangChain 的消息格式）：

```python
[
  HumanMessage(content="In 1969, Neil Armstrong became the first person to walk on the Moon during the Apollo 11 mission."),
  AIMessage(content="Neil Armstrong walked on the Moon in 1969.\nNeil Armstrong was the first person to walk on the Moon.\nNeil Armstrong participated in the Apollo 11 mission.\nThe Apollo 11 mission took place in 1969."),
]
```

你可以把它想象成：

---

### 🧠 模型接收到的提示内容：

```text
【示例对话 1】
人类说：
In 1969, Neil Armstrong became the first person to walk on the Moon during the Apollo 11 mission.

AI 回复：
- Neil Armstrong walked on the Moon in 1969.
- Neil Armstrong was the first person to walk on the Moon.
- Neil Armstrong participated in the Apollo 11 mission.
- The Apollo 11 mission took place in 1969.

【现在你来回答】
人类说：
The Eiffel Tower is located in Paris and was completed in 1889.

AI 回复：
???
```

---

## 📌 总结一句话：

| 变量名                                 | 作用                          |
| ----------------------------------- | --------------------------- |
| `proposition_examples`              | 示例数据（你希望模型模仿的风格）            |
| `example_proposition_prompt`        | 定义单个示例对话长什么样（人类说什么、AI 回应什么） |
| `few_shot_prompt`                   | 把多个示例拼成一个 prompt 列表，供模型学习模仿 |
| `few_shot_prompt.format_messages()` | 最终生成的多轮“人类说 + AI 回答”的对话列表   |

---

### ✅ 想查看 `few_shot_prompt` 最终结果，可以手动打印：

```python
for msg in few_shot_prompt.format_messages():
    print(f"{msg.type.upper()}: {msg.content}")
```

输出如下：

```text
HUMAN: In 1969, Neil Armstrong became the first person to walk on the Moon during the Apollo 11 mission.
AI: Neil Armstrong walked on the Moon in 1969.
    Neil Armstrong was the first person to walk on the Moon.
    Neil Armstrong participated in the Apollo 11 mission.
    The Apollo 11 mission took place in 1969.
```

---

需要我帮你加多个 few-shot 示例、自动化加载文件、或可视化输出也可以继续说！
