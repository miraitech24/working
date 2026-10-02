#!/usr/bin/env python3
"""
【WH-01 / WH-02】第4話: カシミール負エネルギー喉半径保持 & 幾何重力崩壊
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def run_simulation(out_dir="./sim_assets"):
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. 安定時: 0.5nm 微小ワームホール喉保持 (WH-01)
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_title("Task WH-01: Casimir Throat Radius (0.5nm)", color='#f8fafc')
    ax.tick_params(colors='#94a3b8')

    theta = np.linspace(0, 2*np.pi, 100)
    line, = ax.plot([], [], color='#38bdf8', lw=2.5)

    def update_wh(frame):
        r = 0.5 + 0.02 * np.sin(frame * 0.3)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        line.set_data(x, y)
        return line,

    ani_s = animation.FuncAnimation(fig, update_wh, frames=40, interval=60)
    ani_s.save(os.path.join(out_dir, "sim_ep4_casimir_wormhole_stable.gif"), writer='pillow')
    plt.close()

    # 2. 失敗時: 重力崩壊 (WH-02)
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_title("Task WH-02: Gravitational Collapse", color='#f8fafc')
    ax.tick_params(colors='#94a3b8')

    line_col, = ax.plot([], [], color='#f87171', lw=2)

    def update_col(frame):
        r = max(0.01, 1.5 - frame * 0.05)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        line_col.set_data(x, y)
        return line_col,

    ani_e = animation.FuncAnimation(fig, update_col, frames=30, interval=50)
    ani_e.save(os.path.join(out_dir, "sim_ep4_gravitational_collapse.gif"), writer='pillow')
    plt.close()

if __name__ == "__main__":
    run_simulation()
