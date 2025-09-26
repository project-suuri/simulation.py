# 食堂レイアウトを実装
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 定数
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


# 描画の定義

def draw_shelves(ax, candy_shelves_data, shelf_color_map, width, height):
    for shelf in candy_shelves_data:
        color = shelf_color_map.get(tuple(shelf), 'sandybrown')
        rect = patches.Rectangle(shelf, width, height, linewidth=1,
                                 edgecolor='black', facecolor=color, alpha=0.8, zorder=2)
        ax.add_patch(rect)

def draw_registers(ax, register_positions_data):
    ax.scatter(register_positions_data[:, 0], register_positions_data[:, 1],
               color='blue', s=130, marker='*', zorder=4)

def draw_entrance(ax, entrance_pos):
    ax.scatter(entrance_pos[0], entrance_pos[1], color='orange',
               s=150, marker='*', zorder=4)

def draw_exit(ax, exit_pos):
    ax.scatter(exit_pos[0], exit_pos[1], color='green',
               s=150, marker='*', zorder=4)

def draw_salad_bar(ax, salad_bar_data):
    rect = patches.Rectangle(salad_bar_data["pos"], salad_bar_data["width"], salad_bar_data["height"],
                             linewidth=1, edgecolor='black', facecolor='lightgreen', alpha=0.8, zorder=2)
    ax.add_patch(rect)

def draw_return_box(ax, return_box_pos):
    ax.scatter(return_box_pos[0], return_box_pos[1], color='purple',
               s=150, marker='*', zorder=4)

def draw_water_server(ax, water_server_pos):
    ax.scatter(water_server_pos[0], water_server_pos[1], color='deepskyblue',
               s=100, marker='*', zorder=4)

def draw_trash_box(ax, trash_box_pos):
    ax.scatter(trash_box_pos[0], trash_box_pos[1], color='brown',
               s=100, marker='*', zorder=4)
    
def draw_terrace_exit(ax, terrace_exit_pos):
    ax.scatter(terrace_exit_pos[0], terrace_exit_pos[1], color='red',
               s=150, marker='*', zorder=4)

def draw_walls(ax, obstacles_data):
    for obs in obstacles_data:
        if obs.get("type") == "line":
            x_vals = [obs["start"][0], obs["end"][0]]
            y_vals = [obs["start"][1], obs["end"][1]]
            ax.plot(x_vals, y_vals, color='black', linewidth=2, zorder=1)
        elif obs.get("type") == "rect":
            rect = patches.Rectangle(obs["pos"], obs["width"], obs["height"],
                                     linewidth=2, edgecolor='black', facecolor='dimgray',
                                     alpha=0.8, zorder=1)
            ax.add_patch(rect)

def draw_tables(ax, tables_data):
    for table in tables_data:
        rect = patches.Rectangle(table["pos"], table["width"], table["height"],
                                 edgecolor='black', facecolor='lightblue', zorder=2)
        ax.add_patch(rect)

def draw_chairs(ax, chair_positions_data, radius=0.3, color='black'):
    for pos in chair_positions_data:
        circle = patches.Circle(pos, radius=radius, facecolor=color,
                                edgecolor='black', zorder=3)
        ax.add_patch(circle)
        
        
# メイン関数

def main():
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_aspect('equal')
    ax.set_xlim(0, 70)
    ax.set_ylim(0, 30)
    ax.set_title("LAYOUT")
    ax.grid(True, linestyle='--', alpha=0.6)

    draw_shelves(ax, CANDY_SHELVES_BASE, SHELF_COLOR, SHELF_WIDTH, SHELF_HEIGHT)
    draw_walls(ax, WALLS_LINE + SPACES_RECT) 
    draw_tables(ax, TABLES)
    draw_chairs(ax, CHAIR_POSITIONS)
    draw_registers(ax, REGISTER_POSITIONS)
    draw_entrance(ax, ENTRANCE_POS)
    draw_exit(ax, EXIT_POS)
    draw_return_box(ax, RETURN_BOX_POS)
    draw_water_server(ax, WATER_SERVER_POS)
    draw_trash_box(ax, TRASH_BOX_POS)
    draw_terrace_exit(ax, TERRACE_EXIT_POS)

    plt.show()

if __name__ == '__main__':
    main()