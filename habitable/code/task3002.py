#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 13:46:25 2026

@author: iwamura
"""

import json
import numpy as np
import matplotlib.pyplot as plt

# 1. バトンのインポート (#3001からの引き継ぎ)
try:
    with open('params_3001.json', 'r') as f:
        params = json.load(f)
    r0 = params['r0_min']
    rho_threshold = params['rho_threshold']
except FileNotFoundError:
    print("Error: params_3001.json が見つかりません。#3001を先に実行してください。")
    exit()

# 2. 物理定数と注入パラメータ
P_inject = 1.64e15  # 注入電力 1.64 [PW] [3]
c = 299792458.0     # 光速 [m/s]
G = 6.67430e-11     # 万有引力定数

# 3. 質量透過率シミュレーション
# 負のエネルギー密度を維持するための効率を100%と仮定しても
# 現状の電力ではスロート全体を維持するには不足するため、維持可能時間(dt)を計算
# E_required = |rho_threshold| * Volume (スロート近傍の薄い殻を想定)
shell_thickness = 1e-15 # 1フェムトメートル厚の仮想的な維持
volume = 4 * np.pi * (r0**2) * shell_thickness
energy_needed = abs(rho_threshold) * volume

# 透過可能な質量(M = E/c^2)の経時変化
time_axis = np.linspace(0, 10, 100) # 秒
m_max = (P_inject * time_axis) / (c**2)

# 4. 結果の出力
print(f"--- #3002 透過率解析レポート ---")
print(f"ターゲット半径: {r0} m")
print(f"必要エネルギー密度: {rho_threshold:.4e} J/m^3")
print(f"1.64PWで1秒間に生成可能な負のエネルギー等価質量: {m_max[4]:.4e} kg")

# 5. 可視化 (png出力 [1])
plt.figure(figsize=(10, 6))
plt.plot(time_axis, m_max, color='cyan', label='Max Permeable Mass (Theoretical)')
plt.axhline(y=70, color='red', linestyle='--', label='Human Mass (70kg)')
plt.title("Mass Transmittance under 1.64PW Injection")
plt.xlabel("Maintenance Duration [s]")
plt.ylabel("Cumulative Transmittable Mass [kg]")
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend()
plt.savefig("mass_transmittance.png")
print("グラフを出力しました: mass_transmittance.png")

