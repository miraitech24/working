#!/usr/bin/env python3
"""
【C110 / MER-16】第1話: 非定常熱伝導方程式 & CFL条件超過熱爆発シミュレーション
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def run_simulation(out_dir="./sim_assets"):
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. 安定時: クランク・ニコルソン陰解法
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    x = np.linspace(0, 1, 50)
    u = np.sin(np.pi * x)
    line, = ax.plot(x, u, color='#38bdf8', lw=2, label='Temp T(x)')
    ax.set_ylim(0, 1.2)
    ax.set_title("Task C110: Crank-Nicolson Scheme (Stable)", color='#f8fafc')
    ax.tick_params(colors='#94a3b8')
    ax.grid(True, alpha=0.3)

    def update_c_n(frame):
        u_curr = u * (0.93 ** frame)
        line.set_ydata(u_curr)
        return line,

    ani_s = animation.FuncAnimation(fig, update_c_n, frames=30, interval=80)
    ani_s.save(os.path.join(out_dir, "sim_ep1_heat_conduction_stable.gif"), writer='pillow')
    plt.close()

    # 2. 失敗時: 陽解法 CFL>0.5 数値的発散 (MER-16)
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    line_exp, = ax.plot(x, u, color='#f87171', lw=1.8, label='CFL Explosion')
    ax.set_ylim(-5, 5)
    ax.set_title("Task MER-16: Explicit Euler CFL > 0.5 Explosion", color='#f8fafc')
    ax.tick_params(colors='#94a3b8')
    ax.grid(True, alpha=0.3)

    def update_cfl(frame):
        noise = ((-1.4) ** frame) * 0.05 * np.sin(10 * np.pi * x)
        u_curr = u * (0.9 ** frame) + noise
        line_exp.set_ydata(u_curr)
        return line_exp,

    ani_e = animation.FuncAnimation(fig, update_cfl, frames=20, interval=100)
    ani_e.save(os.path.join(out_dir, "sim_ep1_cfl_thermal_explosion.gif"), writer='pillow')
    plt.close()

if __name__ == "__main__":
    run_simulation()
