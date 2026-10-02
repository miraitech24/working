#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 11:04:36 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_proxima_grid(n_nodes=865, r_isco=1.1818):
    """
    865拠点のシードをISCO(1.1818M)上に均等配置するアルゴリズム
    """
    indices = np.arange(0, n_nodes, dtype=float) + 0.5
    phi = np.arccos(1 - 2*indices/n_nodes)
    theta = np.pi * (1 + 5**0.5) * indices

    x = r_isco * np.sin(phi) * np.cos(theta)
    y = r_isco * np.sin(phi) * np.sin(theta)
    z = r_isco * np.cos(phi)

    return x, y, z

# パラメータ設定
N_NODES = 865
R_ISCO = 1.1818 # Schwarzschild半径単位(M) [1]

# 座標計算
x, y, z = generate_proxima_grid(N_NODES, R_ISCO)

# 可視化
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# ブラックホール（事象の地平面）の象徴的描写
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
bx = 1.0 * np.cos(u) * np.sin(v) # Event Horizon (1.0M)
by = 1.0 * np.sin(u) * np.sin(v)
bz = 1.0 * np.cos(v)
ax.plot_wireframe(bx, by, bz, color="black", alpha=0.2, label="Event Horizon (1.0M)")

# 865拠点プロット
ax.scatter(x, y, z, c='cyan', s=10, alpha=0.8, label=f"Seed Nodes (N={N_NODES})")

# グラフ設定
ax.set_title(f"Task #3011: Proxima BH Grid Placement (R={R_ISCO}M)")
ax.set_xlabel("X (M)")
ax.set_ylabel("Y (M)")
ax.set_zlabel("Z (M)")
ax.legend()

# 拠点間平均距離の算出（隣接拠点との通信・干渉チェック用）
avg_dist = np.mean(np.sqrt(np.diff(x)**2 + np.diff(y)**2 + np.diff(z)**2))
print(f"--- Calculation Report #3011 ---")
print(f"Total Nodes placed: {len(x)}")
print(f"ISCO Radius: {R_ISCO} M")
print(f"Estimated Node Interval: {avg_dist:.4f} M")
print(f"Status: Grid established for #3012 coupling.")

plt.savefig("task_3011_grid.png")
plt.show()
