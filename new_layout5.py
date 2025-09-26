#斥力
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import CheckButtons

# =============================================================================
# 1. レイアウト定義
# =============================================================================
SHELF_WIDTH = 3
SHELF_HEIGHT = 17.0
REGISTER_POSITIONS = np.array([[32, 8], [32, 9]])
EXIT_POS = np.array([50, 0])
ENTRANCE_POS = np.array([40, 0])
RETURN_BOX_POS = np.array([17, 17])
WATER_SERVER_POS = np.array([23.5, 18])
TRASH_BOX_POS = np.array([48.5, 0.5])
TERRACE_EXIT_POS = np.array([69.75, 13])

# 受け取り口の定義
CANDY_SHELVES_BASE = [np.array([0, 0])]
SHELF_COLOR = {(0, 0): 'royalblue'}

# 線分の定義
WALLS_LINE = [
    {"type": "line", "start": np.array([9, 3], dtype=float), "end": np.array([24, 3], dtype=float)},
    {"type": "line", "start": np.array([9, 6], dtype=float), "end": np.array([24, 6], dtype=float)},
    {"type": "line", "start": np.array([15, 11], dtype=float), "end": np.array([28, 11], dtype=float)},
    {"type": "line", "start": np.array([15, 14], dtype=float), "end": np.array([28, 14], dtype=float)},
    {"type": "line", "start": np.array([13, 16], dtype=float), "end": np.array([15, 14], dtype=float)}
]

# 矩形の定義
SPACES_RECT = [
    {"type": "rect", "pos": np.array([0, 17], dtype=float), "width": 23, "height": 13},
    {"type": "rect", "pos": np.array([45.5, 0], dtype=float), "width": 2, "height": 2},
    {"type": "rect", "pos": np.array([68, 0], dtype=float), "width": 2, "height": 2},
    {"type": "rect", "pos": np.array([12, 8], dtype=float), "width": 18, "height": 1},
    {"type": "rect", "pos": np.array([34, 7.75], dtype=float), "width": 2, "height": 1.5}
]

# テーブルの定義
TABLES = [ 
    {"type": "rect", "pos": np.array([30, 28], dtype=float), "width": 9, "height": 2}, 
    {"type": "rect", "pos": np.array([42, 28], dtype=float), "width": 6, "height": 2}, 
    {"type": "rect", "pos": np.array([51, 28], dtype=float), "width": 15, "height": 2}, 
    {"type": "rect", "pos": np.array([68, 18], dtype=float), "width": 2, "height": 9}, 
    {"type": "rect", "pos": np.array([68, 4], dtype=float), "width": 2, "height": 6}, 
    {"type": "rect", "pos": np.array([52, 0], dtype=float), "width": 12, "height": 2}, 
    {"type": "rect", "pos": np.array([55, 23], dtype=float), "width": 9, "height": 2}, 
    {"type": "rect", "pos": np.array([44, 23], dtype=float), "width": 9, "height": 2}, 
    {"type": "rect", "pos": np.array([33, 23], dtype=float), "width": 9, "height": 2}, 
    {"type": "rect", "pos": np.array([55, 18], dtype=float), "width": 9, "height": 2}, 
    {"type": "rect", "pos": np.array([44, 18], dtype=float), "width": 9, "height": 2}, 
    {"type": "rect", "pos": np.array([36, 18], dtype=float), "width": 6, "height": 2}, 
    {"type": "rect", "pos": np.array([55, 4], dtype=float), "width": 9, "height": 2}, 
    {"type": "rect", "pos": np.array([50, 4], dtype=float), "width": 3, "height": 2}, 
    {"type": "rect", "pos": np.array([55, 8], dtype=float), "width": 9, "height": 2}, 
    {"type": "rect", "pos": np.array([44, 8], dtype=float), "width": 9, "height": 2} 
]

# 座席の位置の定義
CHAIR_POSITIONS = []
CHAIR_CONFIG_1 = [
    {'y': 28, 'x_ranges': [np.linspace(31, 38, 6), np.linspace(43, 47, 4), np.linspace(52, 65, 10)]},
    {'y': 2, 'x_ranges': [np.linspace(52.5, 63.5, 8)]},
    {'x': 68, 'y_ranges': [np.linspace(4.5, 9.5, 4), np.linspace(18.5, 26.5, 6)]}
]
for config in CHAIR_CONFIG_1:
    if 'y' in config:
        for x_vals in config['x_ranges']:
            for x in x_vals: CHAIR_POSITIONS.append(np.array([x, config['y']]))
    elif 'x' in config:
        for y_vals in config['y_ranges']:
            for y in y_vals: CHAIR_POSITIONS.append(np.array([config['x'], y]))
CHAIR_CONFIG_2 = {
    (23, 25): [np.linspace(33.5, 41.5, 9), np.linspace(44.5, 52.5, 9), np.linspace(55.5, 63.5, 9)],
    (18, 20): [np.linspace(36.5, 41.5, 6), np.linspace(44.5, 52.5, 9), np.linspace(55.5, 63.5, 9)],
    (8, 10): [np.linspace(44.5, 52.5, 9), np.linspace(55.5, 63.5, 9)],
    (4, 6): [np.linspace(50.5, 52.5, 3), np.linspace(55.5, 63.5, 9)]
}
for ys, x_ranges in CHAIR_CONFIG_2.items():
    for y in ys:
        for x_vals in x_ranges:
            for x in x_vals: CHAIR_POSITIONS.append(np.array([x, y]))

# =============================================================================
# 2. 描画関数
# =============================================================================
def draw_shelves(ax, candy_shelves_data, shelf_color_map, width, height):
    for shelf in candy_shelves_data:
        color = shelf_color_map.get(tuple(shelf), 'sandybrown')
        rect = patches.Rectangle(shelf, width, height, linewidth=1,
                                 edgecolor='black', facecolor=color, alpha=0.8, zorder=2)
        ax.add_patch(rect)

def draw_registers(ax, register_positions_data):
    return ax.scatter(register_positions_data[:, 0], register_positions_data[:, 1],
                      color='blue', s=130, marker='*', zorder=4)

def draw_entrance(ax, entrance_pos):
    return ax.scatter(entrance_pos[0], entrance_pos[1], color='orange',
                      s=130, marker='*', zorder=4)

def draw_exit(ax, exit_pos):
    return ax.scatter(exit_pos[0], exit_pos[1], color='green',
                      s=130, marker='*', zorder=4)

def draw_return_box(ax, return_box_pos):
    return ax.scatter(return_box_pos[0], return_box_pos[1], color='purple',
                      s=130, marker='*', zorder=4)

def draw_water_server(ax, water_server_pos):
    return ax.scatter(water_server_pos[0], water_server_pos[1], color='deepskyblue',
                      s=130, marker='*', zorder=4)

def draw_trash_box(ax, trash_box_pos):
    return ax.scatter(trash_box_pos[0], trash_box_pos[1], color='brown',
                      s=130, marker='*', zorder=4)
    
def draw_terrace_exit(ax, terrace_exit_pos):
    return ax.scatter(terrace_exit_pos[0], terrace_exit_pos[1], color='orangered',
                      s=130, marker='*', zorder=4)

def draw_walls_and_rects(ax, obstacles_data, radius=0.25):
    wall_circles = []
    step = radius * 1.5  # 半径の1.5倍で重ねて描画
    for obs in obstacles_data:
        if obs.get("type") == "line":
            start, end = obs["start"], obs["end"]
            length = np.linalg.norm(end - start)
            steps = max(int(length / step), 1)
            for t in np.linspace(0, 1, steps):
                pos = (1 - t) * start + t * end
                circ = patches.Circle(pos, radius=radius, facecolor="black", edgecolor="black", zorder=2)
                ax.add_patch(circ)
                wall_circles.append(pos)
        elif obs.get("type") == "rect":
            x0, y0 = obs["pos"]
            w, h = obs["width"], obs["height"]
            for x in np.arange(x0, x0 + w + step, step):
                for y in [y0, y0 + h]:
                    wall_circles.append(np.array([x, y]))
                    ax.add_patch(patches.Circle((x, y), radius=radius, facecolor="black", edgecolor="black", zorder=2))
            for y in np.arange(y0, y0 + h + step, step):
                for x in [x0, x0 + w]:
                    wall_circles.append(np.array([x, y]))
                    ax.add_patch(patches.Circle((x, y), radius=radius, facecolor="black", edgecolor="black", zorder=2))
    return np.array(wall_circles)

def draw_tables(ax, tables_data):
    drawn_objects = []
    for table in tables_data:
        rect = patches.Rectangle(table["pos"], table["width"], table["height"],
                                 edgecolor='black', facecolor='lightblue', zorder=2)
        ax.add_patch(rect)
        drawn_objects.append(rect)
    return drawn_objects

def draw_chairs(ax, chair_positions_data, radius=0.3, color='black'):
    drawn_objects = []
    for pos in chair_positions_data:
        circle = patches.Circle(pos, radius=radius, facecolor=color,
                                edgecolor='black', zorder=3)
        ax.add_patch(circle)
        drawn_objects.append(circle)
    return drawn_objects

# =============================================================================
# 3. エージェント(SFM)
# =============================================================================
INITIAL_POSITION = np.array([40.0, 0.0])
GOAL_POS = np.array([50.0, 0.0])
SPEED = 0.3
WAYPOINTS = [
    {"pos": np.array([30, 1]), "wait": 0},
    {"pos": np.array([3.5, 1]), "wait": 0.5},
    {"pos": np.array([3.5, 2.5]), "wait": 1.5},
    {"pos": np.array([9.5, 7.5]), "wait": 0},
    {"pos": np.array([32, 7]), "wait": 1.5},
    {"pos": np.array([35, 7]), "wait": 0.5},
    {"pos": np.array([37, 7.5]), "wait": 0},
    {"pos": np.array([50, 15]), "wait": 0},
    {"pos": np.array([17, 16]), "wait": 1},
    {"pos": np.array([33, 15]), "wait": 0},
    {"pos": np.array([47, 5]), "wait": 0},
]

class Customer:
    def __init__(self, start_pos, waypoints, goal, anim_interval, walls):
        self.pos = np.array(start_pos, dtype=float)
        self.targets = waypoints + [{"pos": goal, "wait": 0}]
        self.anim_interval = anim_interval
        self.target_index = 0
        self.reached_goal = False
        self.is_waiting = False
        self.wait_timer = 0
        self.walls = walls

    def update(self):
        if self.reached_goal: return False
        if self.is_waiting:
            self.wait_timer -= 1
            if self.wait_timer <= 0: self.is_waiting = False
            return True

        current_target_info = self.targets[self.target_index]
        target_pos = current_target_info["pos"]

        # SFM: 目標への力
        desired_direction = target_pos - self.pos
        dist_to_target = np.linalg.norm(desired_direction)
        if dist_to_target > 0:
            desired_direction /= dist_to_target
        F_goal = SPEED * desired_direction

        # SFM: 壁との斥力
        F_rep = np.zeros(2)
        A = 3.5  # 強さ
        B = 0.5  # 距離減衰
        for wall in self.walls:
            diff = self.pos - wall
            d = np.linalg.norm(diff)
            if d < 2.0 and d > 1e-4:
                F_rep += A * np.exp(-d / B) * diff / d

        # 速度更新
        self.pos += F_goal + F_rep * 0.1  # 斥力のスケール

        # 中継点到達判定
        if dist_to_target < 0.2:
            is_final_goal = (self.target_index == len(self.targets) - 1)
            if is_final_goal:
                self.reached_goal = True
                return False
            wait_seconds = current_target_info["wait"]
            self.target_index += 1
            if wait_seconds > 0:
                self.is_waiting = True
                self.wait_timer = int(wait_seconds * 1000 / self.anim_interval)
        return True

# =============================================================================
# 4. メイン関数
# =============================================================================
fig, ax = plt.subplots(figsize=(16, 7))
fig.subplots_adjust(right=0.85)
ax.set_xlim(0, 70)
ax.set_ylim(0, 30)
ax.set_aspect("equal")
ax.grid(True, linestyle="--", alpha=0.3)
ax.set_title("SFM Cafeteria Simulation")

draw_shelves(ax, CANDY_SHELVES_BASE, SHELF_COLOR, SHELF_WIDTH, SHELF_HEIGHT)
wall_positions = draw_walls_and_rects(ax, WALLS_LINE + SPACES_RECT)

waypoints_np = np.array([wp["pos"] for wp in WAYPOINTS])
ax.scatter(waypoints_np[:, 0], waypoints_np[:, 1], color="orange", s=80, zorder=5)
table_objects = draw_tables(ax, TABLES)
chair_objects = draw_chairs(ax, CHAIR_POSITIONS)
facility_objects = [
        draw_registers(ax, REGISTER_POSITIONS),
        draw_entrance(ax, ENTRANCE_POS),
        draw_exit(ax, EXIT_POS),
        draw_return_box(ax, RETURN_BOX_POS),
        draw_water_server(ax, WATER_SERVER_POS),
        draw_trash_box(ax, TRASH_BOX_POS),
        draw_terrace_exit(ax, TERRACE_EXIT_POS)
    ]

rax = fig.add_axes([0.87, 0.4, 0.1, 0.2])
labels = ['table', 'chair', 'object']
visibility = [True, True, True]
check = CheckButtons(rax, labels, visibility)

def update_visibility(label):
        object_map = {'table': table_objects, 'chair': chair_objects, 'object': facility_objects}
        for obj in object_map[label]:
            obj.set_visible(not obj.get_visible())
        fig.canvas.draw_idle()

check.on_clicked(update_visibility)

ANIMATION_INTERVAL = 25
customer = Customer(INITIAL_POSITION, WAYPOINTS, GOAL_POS, ANIMATION_INTERVAL, wall_positions)
point, = ax.plot([], [], 'o', color='crimson', markersize=8, zorder=10)

def init():
    point.set_data([], [])
    return point,

def update(frame):
    moving = customer.update()
    if moving:
        pos = customer.pos
        point.set_data([pos[0]], [pos[1]])
    else:
        point.set_data([], [])
        ani.event_source.stop()
    return point,

ani = FuncAnimation(fig, update, frames=1000,
                    init_func=init, interval=ANIMATION_INTERVAL, blit=False)

plt.show()
