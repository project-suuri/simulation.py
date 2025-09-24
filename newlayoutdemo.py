# coding: utf-8
import matplotlib.pyplot as plt
import newlayout  # あなたの layout.py を import



def draw_cafeteria():
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 70)
    ax.set_ylim(0, 30)
    ax.set_aspect("equal")
    ax.grid(True, linestyle="--", alpha=0.3)

    # ==== 食堂のオブジェクトを描画 ====
    newlayout.draw_shelves(ax, newlayout.CANDY_SHELVES_BASE,
                        newlayout.SHELF_COLOR,
                        newlayout.SHELF_WIDTH,
                        newlayout.SHELF_HEIGHT)
    newlayout.draw_registers(ax, newlayout.REGISTER_POSITIONS)
    newlayout.draw_exit(ax, newlayout.EXIT_POS)
    newlayout.draw_salad_bar(ax, newlayout.SALAD_BAR)
    newlayout.draw_walls(ax, newlayout.OBSTACLES)
    newlayout.draw_return_box(ax, newlayout.RETURN_BOX_POS)
    newlayout.draw_water_server(ax, newlayout.WATER_SERVER_POS)
    newlayout.draw_trash_box(ax, newlayout.TRASH_BOX_POS)
    newlayout.draw_chairs(ax, newlayout.CHAIR_POSITIONS)

    ax.set_title("University Cafeteria Layout", fontsize=14)
    ax.legend(loc="upper right")
    plt.show()

if __name__ == "__main__":
    draw_cafeteria()