import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import random

positions = ["right", "left", "up", "down"]

x, y = 0, 0
Xs = [x]
Ys = [y]
count = {(x, y) : 1}
n = 100
steps = np.arange(1, n+2)

for _ in range(n):
    pos = random.choice(positions)
    if pos == "right":
        Ys.append(Ys[-1])
        Xs.append(Xs[-1] + 1)
    elif pos == "left":
        Xs.append(Xs[-1] - 1)
        Ys.append(Ys[-1])
    elif pos == "up":
        Xs.append(Xs[-1])
        Ys.append(Ys[-1] + 1)
    else:
        Xs.append(Xs[-1])
        Ys.append(Ys[-1] - 1)

    if (Xs[-1], Ys[-1]) in count:
        count[(Xs[-1], Ys[-1])] += 1
    else:
        count[(Xs[-1], Ys[-1])] = 1

min_x, max_x = min(Xs), max(Xs)
min_y, max_y = min(Ys), max(Ys)
width = max_x - min_x + 1
height = max_y - min_y + 1
heatmap = np.zeros((height, width), dtype=int)
distances = np.hypot(Xs, Ys)
max_distance = np.maximum.accumulate(distances)

unique_locations = np.zeros(n + 1, dtype=int)
origin_returns = np.zeros(n + 1, dtype=int)
revisit_percentage = np.zeros(n + 1)

visited = set()
returns = 0

for i, point in enumerate(zip(Xs, Ys)):
    visited.add(point)

    if i > 0 and point == (0, 0):
        returns += 1

    unique_locations[i] = len(visited)
    origin_returns[i] = returns

    if i > 0:
        revisit_percentage[i] = (
            100 * (i + 1 - len(visited)) / i
        )

unique_locations_m = len(count)
origin_returns_m = count[(0, 0)] - 1
revisit_percentage_m = 100 * (n + 1 - unique_locations_m) / n
squared_displacement = np.array(Xs) ** 2 + np.array(Ys) ** 2

x = np.array(Xs)
y = np.array(Ys)

lags = np.arange(1, min(100, n) + 1)

msd = []

for lag in lags:
    dx = x[lag:] - x[:-lag]
    dy = y[lag:] - y[:-lag]
    msd.append(np.mean(dx ** 2 + dy ** 2))


for (x, y), cnt in count.items():
    row = y - min_y
    col = x - min_x
    heatmap[row, col] = cnt

fig = plt.figure(figsize = (18, 9), constrained_layout=True)
gs = gridspec.GridSpec(2, 4, hspace = 0.6, wspace = 0.4)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
ax3 = fig.add_subplot(gs[2])
ax4 = fig.add_subplot(gs[3])
ax5 = fig.add_subplot(gs[4])
ax6 = fig.add_subplot(gs[5])
ax7 = fig.add_subplot(gs[6])
ax8 = fig.add_subplot(gs[7])

ax1.spines['left'].set_position('zero')
ax1.spines['bottom'].set_position('zero')
ax1.spines['right'].set_color('none')
ax1.spines['top'].set_color('none')

sc1 = ax1.scatter([Xs[0]], [Ys[0]], marker = "o", edgecolors = "black", color = "red")
ax1.annotate("Start", (Xs[0], Ys[0]), color = "black")

sc2 = ax1.scatter([Xs[-1]], [Ys[-1]], marker = "o", edgecolors = "black", color = "red")
end_label = ax1.annotate("End", (Xs[-1], Ys[-1]), color = "black")

line1, = ax1.plot(Xs, Ys)

ax1.grid(True, linestyle='--', alpha=0.6)
ax1.set_aspect("equal")

animated_heatmap = np.zeros_like(heatmap)

im = ax2.imshow(
    animated_heatmap,
    cmap="hot",
    origin="lower",
    extent=[
        min_x - 0.5, max_x + 0.5,
        min_y - 0.5, max_y + 0.5
    ],
    vmin=0,
    vmax=heatmap.max()
)

cbar = fig.colorbar(im, ax=ax2)
cbar.set_label("Visit Count")

line1.set_marker("o")
line1.set_markerfacecolor("red")
line1.set_markeredgecolor("black")
line1.set_markevery([-1])

rows = np.array(Ys) - min_y
cols = np.array(Xs) - min_x

line2, = ax3.plot(steps, distances)

line3, = ax4.plot(steps, max_distance)

line4, = ax5.plot(steps, unique_locations)

line5, = ax6.plot(steps, origin_returns)

line6, = ax7.plot(steps, revisit_percentage)

line7, = ax8.plot(steps, squared_displacement)

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    line4.set_data([], [])
    line5.set_data([], [])
    line6.set_data([], [])
    line7.set_data([], [])

    sc2.set_visible(False)
    end_label.set_visible(False)

    animated_heatmap.fill(0)
    im.set_data(animated_heatmap)

    return line1, line2, line3, line4, line5, line6, line7, sc2, end_label, im

def update(frame):
    line1.set_data(Xs[:frame + 1], Ys[:frame + 1])
    line2.set_data(steps[:frame + 1], distances[:frame + 1])
    line3.set_data(steps[:frame + 1], max_distance[:frame + 1])
    line4.set_data(steps[:frame + 1], unique_locations[:frame + 1])
    line5.set_data(steps[:frame + 1], origin_returns[:frame + 1])
    line6.set_data(steps[:frame + 1], revisit_percentage[:frame + 1])
    line7.set_data(steps[:frame + 1], squared_displacement[:frame + 1])

    finished = frame == len(Xs) - 1
    sc2.set_visible(finished)
    end_label.set_visible(finished)

    animated_heatmap.fill(0)
    np.add.at(
        animated_heatmap,
        (rows[:frame + 1], cols[:frame + 1]),
        1
    )
    im.set_data(animated_heatmap)

    return line1, line2, line3, line4, line5, line6, line7, sc2, end_label, im

axes = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]

titles = [
    "2D Random Walk",
    "Visit Frequency",
    "Distance from Origin",
    "Maximum Distance Reached",
    "Unique Sites Visited",
    "Returns to Origin",
    "Revisit Percentage",
    "Squared Displacement"
]

for ax, title in zip(axes, titles):
    ax.set_title(title, fontsize=11, fontweight="bold", pad=12)
    ax.tick_params(axis="both", labelsize=9)

for ax in [ax1, ax2]:
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

ylabels = [
    "Distance",
    "Distance",
    "Unique sites",
    "Returns",
    "Revisits (%)",
    "Squared distance"
]

for ax, ylabel in zip(axes[2:], ylabels):
    ax.set_xlabel("Number of steps", fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

fig.suptitle(
    f"2D Random Walk — {n:,} Steps",
    fontsize=18,
    fontweight="bold"
)

ani = animation.FuncAnimation(
    fig,
    update,
    frames=len(Xs),
    init_func=init,
    interval=100,
    blit=True,
    repeat=False
)

plt.show()