import asyncio
import time

async def task(id, delay):
    print(f"任务{id}开始，预计耗时{delay}秒")
    await asyncio.sleep(delay)  # 模拟耗时操作
    print(f"任务{id}完成")
    return f"任务{id}结果"

async def main():
    start = time.time()  # 记录开始时间

    results = await asyncio.gather(
        task(1, 2),
        task(2, 3),
        task(3, 1),
    )

    end = time.time()  # 记录结束时间
    print(f"\n所有任务结果: {results}")
    print(f"总耗时: {end - start:.2f} 秒")

asyncio.run(main())
