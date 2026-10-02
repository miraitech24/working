#!/usr/bin/env python3
"""
【#3002 / MER-12】プロローグ: 1.64PW光圧レーザー推進 & 照準軸ブレ熱偏心シミュレーション
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def run_simulation(out_dir="./sim_assets"):
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. 正解時: 1.64PW安定集光加速
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    t = np.linspace(0, 10, 100)
    v = 0.20 * (1 - np.exp(-0.3 * t))
    line, = ax.plot([], [], color='#38bdf8', lw=2.5, label='Velocity (c)')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 0.25)
    ax.set_title("Task #3002: Laser Acceleration (Stable 0.20c)", color='#f8fafc')
    ax.set_xlabel("Time (s)", color='#94a3b8')
    ax.set_ylabel("Velocity (c)", color='#94a3b8')
    ax.tick_params(colors='#94a3b8')
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(loc='upper left')

    def update_stable(frame):
        line.set_data(t[:frame], v[:frame])
        return line,

    ani_s = animation.FuncAnimation(fig, update_stable, frames=len(t), interval=50)
    ani_s.save(os.path.join(out_dir, "sim_prologue_laser_acceleration.gif"), writer='pillow')
    plt.close()

    # 2. 失敗時: 照準ブレ熱偏心歪み (MER-12)
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    theta = np.linspace(0, 2*np.pi, 100)
    line_err, = ax.plot([], [], color='#f87171', lw=2, label='Thermal Distortion')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_title("Task MER-12: Beam Misalignment & Sail Deformation", color='#f8fafc')
    ax.tick_params(colors='#94a3b8')
    ax.grid(True, linestyle='--', alpha=0.3)

    def update_err(frame):
        r = 1.0 + 0.3 * np.sin(5 * theta + frame * 0.2)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        line_err.set_data(x, y)
        return line_err,

    ani_e = animation.FuncAnimation(fig, update_err, frames=50, interval=60)
    ani_e.save(os.path.join(out_dir, "sim_prologue_beam_instability.gif"), writer='pillow')
    plt.close()

if __name__ == "__main__":
    run_simulation()
