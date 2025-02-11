import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt  # 导入 pyplot，用于绘制图形
matplotlib.use('Agg')  # 设置无图形界面的后端

# 生成一个简单的数据集（475个数据）
data = {
    'No': np.arange(1, 476),  # 1 到 475 的编号
    'Score': np.random.uniform(8.4, 9.7, 475)  # 随机生成 475 个分数
}

df = pd.DataFrame(data)

# 统计分析：描述性统计
print("描述性统计：")
print(df['Score'].describe())

# 简单的数据可视化：直方图和箱线图

# 1. 直方图：分数分布
plt.figure(figsize=(8, 6))
plt.hist(df['Score'], bins=20, color='skyblue', edgecolor='black')
plt.title('Score Distribution')
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.grid(True)
plt.tight_layout()

# 保存直方图
plt.savefig('score_histogram.png')
plt.close()  # 关闭图形，避免后台显示问题

# 2. 箱线图：分数分布
plt.figure(figsize=(8, 6))
plt.boxplot(df['Score'], vert=False, patch_artist=True, boxprops=dict(facecolor='skyblue', color='black'), medianprops=dict(color='red'))
plt.title('Score Boxplot')
plt.xlabel('Score')
plt.grid(True)
plt.tight_layout()

# 保存箱线图
plt.savefig('score_boxplot.png')
plt.close()  # 关闭图形，避免后台显示问题
