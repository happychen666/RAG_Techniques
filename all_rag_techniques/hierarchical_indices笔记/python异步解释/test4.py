import asyncio
import random
import time

async def process_item(item):
    process_time = random.uniform(0.5, 2.0)
    try:
        # 设置1秒超时
        await asyncio.wait_for(
            asyncio.sleep(process_time),
            timeout=1.0
        )
        return f"处理完成：{item}，耗时 {process_time:.2f} 秒"
    except asyncio.TimeoutError:
        return f"处理超时：{item}"

async def main():
    items = ["任务A", "任务B", "任务C", "任务D"]
    tasks = [
        asyncio.create_task(process_item(item))
        for item in items
    ]
    
    start = time.time()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    end = time.time()
    
    print("\n".join(results))
    print(f"总耗时：{end - start:.2f} 秒")

if __name__ == "__main__":
    asyncio.run(main())
