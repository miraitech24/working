#!/usr/bin/env python3
"""
【HZC-13 / MER-03】第2話: 3.2T超電導磁場ローレンツ力プラズマ偏向散乱 & 塵アブレーション
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def run_simulation(out_dir="./sim_assets"):
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. 安定時: ローレンツ力偏向散乱 (HZC-13)
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_title("Task HZC-13: 3.2T Lorentz Plasma Deflection", color='#f8fafc')
    ax.tick_params(colors='#94a3b8')

    circle = plt.Circle((0,0), 0.5, color='#38bdf8', fill=False, lw=2)
    ax.add_patch(circle)

    lines = [ax.plot([], [], color='#4ade80', alpha=0.7)[0] for _ in range(5)]

    def update_l(frame):
        for i, line in enumerate(lines):
            y0 = -1.5 + i * 0.75
            x = np.linspace(-2, 2, 50)
            y = y0 + 0.3 * np.exp(-x**2) * np.sin(frame*0.2 + i)
            line.set_data(x[:frame], y[:frame])
        return lines

    ani_s = animation.FuncAnimation(fig, update_l, frames=50, interval=50)
    ani_s.save(os.path.join(out_dir, "sim_ep2_lorentz_plasma_deflection.gif"), writer='pillow')
    plt.close()

    # 2. 失敗時: 塵アブレーション (MER-03)
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_title("Task MER-03: Micro-dust Particle Impact", color='#f8fafc')
    ax.tick_params(colors='#94a3b8')

    p, = ax.plot([], [], 'ro', ms=8)
    spark, = ax.plot([], [], 'y*', ms=12)

    def update_dust(frame):
        x = 2.0 - frame * 0.15
        p.set_data([x], [0])
        if x <= 0:
            spark.set_data([0], [0])
        else:
            spark.set_data([], [])
        return p, spark

    ani_e = animation.FuncAnimation(fig, update_dust, frames=30, interval=50)
    ani_e.save(os.path.join(out_dir, "sim_ep2_particle_impact_ablation.gif"), writer='pillow')
    plt.close()

if __name__ == "__main__":
    run_simulation()
