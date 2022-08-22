from concurrent.futures import ProcessPoolExecutor
import time
from concurrent.futures import ThreadPoolExecutor
import random
from concurrent.futures._base import Future

# max_workers表示工人数量,也就是线程池里面的线程数量
# pool = ThreadPoolExecutor(max_workers=10) # 多线程
pool = ProcessPoolExecutor(max_workers=10) # 多进程
# 任务列表
task_list = ["任务1", "任务2", "任务3", "任务4", "任务5", "任务6", "任务7", "任务8", "任务9", "任务10"]


def handler(task_name):
    # 随机睡眠,模仿任务执行时间不确定性
    n = random.randrange(5)
    time.sleep(n)
    print(f"任务内容:{task_name}")
    print(f"进程ID：{os.getpid()}")
    print(f"线程ID：{threading.currentThread().ident}")
    return f"任务内容:{task_name}"


def done(res: Future):
    print("done拿到的返回值:", res.result())


if __name__ == '__main__':
    # 遍历任务,
    for task in task_list:
        futrue = pool.submit(handler, task)  # type:Future
        futrue.add_done_callback(done)
    pool.shutdown()
    print("main执行完毕")
