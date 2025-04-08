from alive_progress import alive_bar
import time
import random

# 定义不同任务
tasks = [
    "🔄 正在连接服务器...",
    "📡 正在下载数据包...",
    "📂 正在解析文件...",
    "🛠 正在处理数据...",
    "🚀 AI 计算中...",
    "💾 正在保存结果...",
    "✅ 任务完成！"
]

total_steps = 100  # 进度条总步数

with alive_bar(total_steps, title="🌈 终极炫酷进度条", bar="filling", spinner="twirls") as bar:
    for i in range(total_steps):
        time.sleep(random.uniform(0.05, 0.15))  # 模拟任务执行时间

        # 每隔 20% 随机更新任务状态
        if i % (total_steps // len(tasks)) == 0:
            print(f"\n🎯 {random.choice(tasks)}")

        bar()  # 更新进度条
