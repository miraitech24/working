#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 11:57:05 2026

@author: iwamura
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_simulation():
    # 1. データのインポート
    try:
        # header=None を維持し、namesで列名を指定
        data = pd.read_csv("energy_grid_pw.csv", header=None, names=['year', 'power_pw'])
    except FileNotFoundError:
        print("Error: energy_grid_pw.csv not found.")
        return

    # 2. 自己複製ロボット増殖シミュレーション
    # 拠点の履歴を保存する配列をゼロで初期化
    nodes = np.zeros(len(data))
    
    # 【重要】配列の「最初の要素」に初期値を代入
    nodes[0] = 1.0 
    
    target_nodes = 865
    growth_rate_base = 0.025 # 基本増殖率
    
    for t in range(1, len(data)):
        # 前年の拠点数に基づき、供給エネルギーPWに応じて増殖
        # data.iloc[t] は pandas の Series なので、floatとして計算
        energy_factor = float(data.iloc[t]['power_pw']) / 2.5
        new_nodes = nodes[t-1] * growth_rate_base * energy_factor
        
        # 拠点数はターゲット(865)を上限として累積
        nodes[t] = min(nodes[t-1] + new_nodes, target_nodes)

    # 3. 結果の可視化
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.set_xlabel('Years after Arrival')
    ax1.set_ylabel('Infrastructure Node Count', color='tab:cyan')
    
    # プロット
    ax1.plot(data['year'], nodes, color='tab:cyan', linewidth=3, label='Active Nodes (N=865)')
    ax1.axhline(y=target_nodes, color='r', linestyle='--', alpha=0.5, label='Target Capacity')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='upper left')

    # エネルギー供給の変動を背景に表示
    ax2 = ax1.twinx()
    ax2.set_ylabel('Input Energy from Binary (PW)', color='tab:blue')
    ax2.plot(data['year'], data['power_pw'], color='tab:blue', alpha=0.2, label='Available Power')

    plt.title('Task #3013: Interstellar Infrastructure Growth Workflow')
    plt.savefig('task3013_construction.png')
    
    print(f"Simulation Complete: {nodes[-1]:.1f} nodes active at Year 300.")

if __name__ == "__main__":
    run_simulation()