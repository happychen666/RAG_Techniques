import asyncio

async def work(name, delay):
    print(f"{name} 开始，耗时 {delay}s")
    await asyncio.sleep(delay)
    print(f"{name} 完成")
    return f"{name}结果"


# 示例一：
# async def main():
#     # 启动任务，但不阻塞当前协程
#     task1 = asyncio.create_task(work("任务1", 5))
#     task2 = asyncio.create_task(work("任务2", 3))

#     print("我这边可以继续干别的事情，不会卡住！")

#     # 等待任务完成
#     res1 = await task1
#     res2 = await task2
#     print("结果:", res1, res2)

# 示例二：
async def main():
    task = asyncio.create_task(work("任务A", 5))
    result = await task
    print("最终结果:", result)

    print("先处理一些别的逻辑...")
    await asyncio.sleep(2)
    print("2 秒过去了，继续处理其他逻辑...")

# 示例三：
async def main():
    task = asyncio.create_task(work("任务A", 5))

    
    print("先处理一些别的逻辑...")
    await asyncio.sleep(2)
    print("2 秒过去了，继续处理其他逻辑...")

    result = await task
    print("最终结果:", result)


# 注意：示例二和示例三代码顺序不一样，结果差别很大，要理解

asyncio.run(main())
