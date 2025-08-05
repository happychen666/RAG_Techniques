你的问题非常好！  
在代码里确实看到 `QUESTION_GENERATION = QuestionGeneration.DOCUMENT_LEVEL` 是写死的常量，所以貌似后面的 `if QUESTION_GENERATION == QuestionGeneration.FRAGMENT_LEVEL` 和 `if QUESTION_GENERATION == QuestionGeneration.DOCUMENT_LEVEL` 判断就显得没有意义了，因为值不会变。

**为什么还要写成这样？原因如下：**

1. **方便后续切换和扩展**  
   把 `QUESTION_GENERATION` 作为参数写出来，可以让用户很容易地修改为 `FRAGMENT_LEVEL`，比如在实验不同的增广粒度时，只需改成：
   ```python
   QUESTION_GENERATION = QuestionGeneration.FRAGMENT_LEVEL
   ```
   这样，后面的 `if` 判断就会生效，切换不同的处理逻辑。

2. **代码可复用性和清晰性**  
   这种模式让代码在不同场景下都能用，而不用每次都去删改大段逻辑。实际上，如果你把这个参数变成输入参数（比如函数参数、配置文件读取），就可以灵活控制增广的层级。

3. **兼容未来自动化或外部配置**  
   很多 notebook 或脚本一开始会把参数写死，后面逐步改成从外部读取或交互式设置，这样判断分支就有实际意义了。

**总结**：  
现在代码里确实是写死的，如果你不改参数，`if` 分支只会走一个。但这个结构是为了让代码更易扩展和灵活，随时能切换不同增广策略。如果只是单一用法，可以精简掉分支，但实际工程/实验场景下这样写更好。

需要举例说明怎样切换吗？或者你想了解如何把它做成可配置参数？    