import asyncio
import time

async def task(id, delay):
    print(f"任务{id}开始，预计耗时{delay}秒")
    await asyncio.sleep(delay)
    print(f"任务{id}完成")
    return f"任务{id}结果"

# 并发执行
async def run_concurrent():
    print("\n=== 并发执行（asyncio.gather） ===")
    start = time.time()

    results = await asyncio.gather(
        task(1, 2),
        task(2, 3),
        task(3, 1),
    )

    end = time.time()
    print(f"所有任务结果: {results}")
    print(f"总耗时: {end - start:.2f} 秒")

# 顺序执行
async def run_sequential():
    print("\n=== 顺序执行（逐个 await） ===")
    start = time.time()

    # results = []
    # results.append(await task(1, 2))
    # results.append(await task(2, 3))
    # results.append(await task(3, 1))
    # print(f"所有任务结果: {results}")

    await task(1, 2)
    await task(2, 3)
    await task(3, 1)
    end = time.time()
    print(f"总耗时: {end - start:.2f} 秒")

async def main():
    # await run_concurrent()
    await run_sequential()

asyncio.run(main())
