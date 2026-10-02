#!/usr/bin/env python3
"""
【HZC-14 / C001】第3話: 12m岩盤モンテカルロ放射線遮蔽 & M型フレアEMP
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def run_simulation(out_dir="./sim_assets"):
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. 安定時: モンテカルロ岩盤遮蔽 (HZC-14)
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 100)
    ax.axvline(x=12, color='#f59e0b', linestyle='--', label='Cave Rock (12m)')
    ax.set_title("Task HZC-14: Monte Carlo Radiation Shielding", color='#f8fafc')
    ax.tick_params(colors='#94a3b8')
    ax.legend(loc='upper right')

    x_vals = np.linspace(0, 15, 50)
    line, = ax.plot([], [], color='#38bdf8', lw=2)

    def update_m(frame):
        y_vals = 100 * np.exp(-0.4 * x_vals[:frame])
        line.set_data(x_vals[:frame], y_vals)
        return line,

    ani_s = animation.FuncAnimation(fig, update_m, frames=50, interval=50)
    ani_s.save(os.path.join(out_dir, "sim_ep3_cave_radiation_shielding.gif"), writer='pillow')
    plt.close()

    # 2. 失敗時: フレアEMP損壊 (C001)
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    ax.set_xlim(0, 10)
    ax.set_ylim(-10, 10)
    ax.set_title("Task C001: M-Flare EMP Circuit Damage", color='#f8fafc')
    ax.tick_params(colors='#94a3b8')

    t_vals = np.linspace(0, 10, 100)
    line_emp, = ax.plot([], [], color='#f87171', lw=1.5)

    def update_emp(frame):
        sig = np.sin(5 * t_vals[:frame]) * np.exp(t_vals[:frame]*0.2)
        line_emp.set_data(t_vals[:frame], sig)
        return line_emp,

    ani_e = animation.FuncAnimation(fig, update_emp, frames=50, interval=40)
    ani_e.save(os.path.join(out_dir, "sim_ep3_solar_flare_emp_burn.gif"), writer='pillow')
    plt.close()

if __name__ == "__main__":
    run_simulation()
