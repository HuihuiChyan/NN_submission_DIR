import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FormatStrFormatter
import numpy as np

# ==========================================
# 1. 准备数据
# ==========================================
iterations = np.array([1, 2, 3, 4, 5])
iter_labels = ['Iter 1', 'Iter 2', 'Iter 3', 'Iter 4', 'Iter 5']

# CFBench
cfbench_csr = [0.65, 0.67, 0.68, 0.68, 0.69]
cfbench_isr = [0.27, 0.26, 0.28, 0.28, 0.30]
cfbench_psr = [0.36, 0.37, 0.39, 0.39, 0.40]

# FollowBench
hsr = [49.75, 53.82, 54.46, 53.97, 53.30]
ssr = [64.78, 67.55, 67.54, 67.09, 67.91]

# Token Numbers
input_tokens = [1882, 3351, 4844, 6361, 7902]
output_tokens = [1869, 2562, 3275, 4008, 4761]

# AlpacaEval2
lc_win_rate = [21.63, 21.01, 20.69, 22.50, 20.78]
avg_length = [1994, 1829, 1722, 1672, 1599]

# ==========================================
# 2. 全局样式设置
# ==========================================
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14

# 创建画布
fig = plt.figure(figsize=(10, 16))

# 使用 GridSpec 管理 4 个主要图表的布局
gs_main = gridspec.GridSpec(4, 1, height_ratios=[1.2, 1, 1, 1], hspace=0.35)

# ==========================================
# 图 1: CFBench Performance (使用截断Y轴)
# ==========================================
# 在第一个 GridSpec 位置再嵌套一个 GridSpec 用于上下分割
gs_cf = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs_main[0], hspace=0.08)
ax_cf_top = fig.add_subplot(gs_cf[0])
ax_cf_bot = fig.add_subplot(gs_cf[1])

# 将相同的数据画在两个子图上
for ax in [ax_cf_top, ax_cf_bot]:
    ax.plot(iterations, cfbench_csr, marker='o', linestyle='-', linewidth=2, markersize=6, color='tab:blue', label='CSR')
    ax.plot(iterations, cfbench_isr, marker='s', linestyle='-', linewidth=2, markersize=6, color='tab:orange', label='ISR')
    ax.plot(iterations, cfbench_psr, marker='^', linestyle='-', linewidth=2, markersize=6, color='tab:green', label='PSR')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xticks(iterations)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

# 设置截断范围 (跳过 0.42 到 0.62 之间的空白部分)
ax_cf_top.set_ylim(0.63, 0.70)
ax_cf_bot.set_ylim(0.24, 0.41)

# 隐藏相邻的边框线并调整刻度
ax_cf_top.spines['bottom'].set_visible(False)
ax_cf_bot.spines['top'].set_visible(False)
ax_cf_top.tick_params(labelbottom=False, bottom=False)  # 顶部图不显示X轴刻度
ax_cf_bot.set_xticklabels(iter_labels)

# 绘制截断标记斜线 (//)
d = 0.015  # 斜线大小
kwargs = dict(transform=ax_cf_top.transAxes, color='gray', clip_on=False, linewidth=1.5)
ax_cf_top.plot((-d, +d), (-d, +d), **kwargs)        # 左上
ax_cf_top.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # 右上

kwargs.update(transform=ax_cf_bot.transAxes)  
ax_cf_bot.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # 左下
ax_cf_bot.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs) # 右下

# 标题和图例
ax_cf_top.set_title('CFBench Performance', fontweight='bold', pad=15)
ax_cf_top.set_ylabel('Score', loc='bottom') 
ax_cf_top.legend() # 将图例放在顶部图表

# ==========================================
# 图 2: FollowBench Performance
# ==========================================
ax1 = fig.add_subplot(gs_main[1])
ax1.plot(iterations, hsr, marker='o', linestyle='-', linewidth=2, markersize=6, color='tab:blue', label='HSR')
ax1.plot(iterations, ssr, marker='s', linestyle='-', linewidth=2, markersize=6, color='tab:orange', label='SSR')

ax1.set_title('FollowBench Performance', fontweight='bold', pad=15)
ax1.set_ylabel('Score (%)')
ax1.set_xticks(iterations)
ax1.set_xticklabels(iter_labels)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend()

# ==========================================
# 图 3: Token Usage Statistics
# ==========================================
ax2 = fig.add_subplot(gs_main[2])
ax2.plot(iterations, input_tokens, marker='o', linestyle='-', linewidth=2, markersize=6, color='tab:purple', label='Input Tokens')
ax2.plot(iterations, output_tokens, marker='s', linestyle='-', linewidth=2, markersize=6, color='tab:red', label='Output Tokens')

ax2.set_title('Token Usage Statistics', fontweight='bold', pad=15)
ax2.set_ylabel('Count')
ax2.set_xticks(iterations)
ax2.set_xticklabels(iter_labels)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend()

# ==========================================
# 图 4: AlpacaEval2: Win Rate & Length (双Y轴)
# ==========================================
ax3 = fig.add_subplot(gs_main[3])
ax3_twin = ax3.twinx()

line1 = ax3.plot(iterations, lc_win_rate, marker='o', linestyle='-', linewidth=2, markersize=6, color='tab:green', label='LC. Win Rate')
line2 = ax3_twin.plot(iterations, avg_length, marker='D', linestyle='--', linewidth=2, markersize=6, color='tab:brown', label='Average Length')

ax3.set_title('AlpacaEval2: Win Rate & Length', fontweight='bold', pad=15)
ax3.set_xlabel('Rejected Iterations', fontsize=16)
ax3.set_ylabel('Win Rate (%)', color='tab:green', fontsize=16)
ax3_twin.set_ylabel('Average Length', color='tab:brown', fontsize=16)

ax3.set_xticks(iterations)
ax3.set_xticklabels(iter_labels)
ax3.grid(True, linestyle='--', alpha=0.5)

ax3.tick_params(axis='y', labelcolor='tab:green')
ax3_twin.tick_params(axis='y', labelcolor='tab:brown')

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax3.legend(lines, labels, loc='center right')

# ==========================================
# 3. 渲染出图
# ==========================================
plt.tight_layout()


plt.savefig('sft_multi_turn.pdf', bbox_inches='tight', pad_inches=0.1)

# plt.show()