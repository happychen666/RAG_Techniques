这段 Python 代码的作用是：

---

## ✅ 用通俗人话解释

> 它会**遍历一个 PDF 文件的每一页**，然后：

1. **提取该页的文字内容**，保存在一个 `text_data` 列表中；
2. **提取该页上的所有图片**，把它们**保存到本地文件夹 `extracted_images/`** 中；
3. 图片会以命名规则：`image_页码_编号.格式` 保存，比如：`image_2_1.png` 表示第 2 页第 1 张图。

你可以用它来**批量抽取一篇 PDF 论文或文档的所有文本和插图**，方便后续做 NLP 分析、OCR、图文分离、数据库存储等。

---

## 📦 每段代码详细拆解 + 举例

```python
text_data = []
img_data = []
```

* `text_data`: 用来保存每一页的文本内容（比如正文、标题、段落）。
* `img_data`: 虽然这里没用到，但可以用来保存提取的图像元数据或引用。

---

```python
with fitz.open('attention_is_all_you_need.pdf') as pdf_file:
```

* `fitz` 是 `PyMuPDF` 的别名，这是一个处理 PDF 文档的库。
* 这行代码打开 PDF 文件《Attention Is All You Need》（Transformer 论文）。

---

```python
if not os.path.exists("extracted_images"):
    os.makedirs("extracted_images")
```

* 如果还没创建目录 `extracted_images/`，就新建一个；
* 所有提取的图片都会保存到这个文件夹下。

---

```python
for page_number in range(len(pdf_file)):
    page = pdf_file[page_number]
```

* 遍历 PDF 的每一页（0 开始编号）；
* `page` 是当前页的内容。

---

```python
text = page.get_text().strip()
text_data.append({"response": text, "name": page_number+1})
```

* 从这一页中提取出 **纯文本内容**，去掉前后空格；
* 保存到 `text_data` 中，结构如下：

  ```python
  {"response": "这页的文字", "name": 1}
  ```

---

```python
images = page.get_images(full=True)
```

* 得到当前页中所有的图片列表；
* 每张图片是一个元组，包含它在 PDF 中的资源编号、尺寸等信息。

---

```python
for image_index, img in enumerate(images, start=0):
    xref = img[0]
```

* 遍历当前页的所有图片；
* `xref` 是这张图片在 PDF 中的唯一 ID（资源编号），后续可以用它提取图像。

---

```python
base_image = pdf_file.extract_image(xref)
image_bytes = base_image["image"]
image_ext = base_image["ext"]
```

* 用 `xref` 把图片从 PDF 中提取出来；
* `image_bytes` 是图像的二进制数据；
* `image_ext` 是图片的格式，比如 `'png'`、`'jpeg'`。

---

```python
image = Image.open(io.BytesIO(image_bytes))
image.save(f"extracted_images/image_{page_number+1}_{image_index+1}.{image_ext}")
```

* 用 PIL 把二进制图像转成图片对象；
* 然后保存到 `extracted_images` 目录下；
* 文件名规则：第几页第几张图，例如：

  * 第 1 页第 1 张图：`image_1_1.png`
  * 第 3 页第 2 张图：`image_3_2.jpeg`

---

## 🧪 举个真实例子

假设你的 PDF 是经典 Transformer 论文 `attention_is_all_you_need.pdf`，它总共有 12 页，包含以下内容：

* 第 1 页是摘要 + 作者；
* 第 2 页有模型图（会被提取为 `image_2_1.png`）；
* 第 4 页有注意力权重的可视化图（提取为 `image_4_1.jpeg`）；

运行后效果如下：

✅ `text_data` 内容示例（第1页）：

```python
[{"response": "Attention Is All You Need\nAshish Vaswani, ...", "name": 1}, ...]
```

✅ 本地生成图片文件：

```
extracted_images/
├── image_2_1.png
├── image_4_1.jpeg
...
```

---

## 📌 总结表格

| 功能        | 说明                       |
| --------- | ------------------------ |
| 提取 PDF 文本 | 每页内容存入 `text_data`       |
| 提取 PDF 图像 | 每页图片提取并保存为文件             |
| 自动命名图片文件  | `image_页码_编号.扩展名`        |
| 创建保存目录    | 自动创建 `extracted_images/` |
| 适用场景      | 批量提取论文图文、文档分离、图文分析       |

---

如果你需要：

* 提取特定页范围（比如第3到7页）
* 只提图片不提文字
* 图片提取后转为 base64、数据库存储
  我可以继续帮你改进这段代码。是否要我帮你加上？
