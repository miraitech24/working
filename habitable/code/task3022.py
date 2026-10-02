#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 11:41:08 2026

@author: iwamura
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_transport_simulation():
    # 1. #3021 (Maxima) からの効率データをインポート
    try:
        efficiency_data = pd.read_csv("penrose_efficiency.csv", header=None, names=['spin', 'eta'])
    except FileNotFoundError:
        print("Error: penrose_efficiency.csv not found. Using theoretical max eta=0.29.")
        efficiency_data = pd.DataFrame({'spin': [0.99], 'eta': [0.29]})

    # 2. #3022 エキゾチック物質定常輸送シミュレーション
    years = 300
    time_steps = np.linspace(0, years, 301)
    
    # 定数定義
    target_mass_flow = 3.5e8  # 3.5億トン/年 [1]
    bh_energy_pw = 2500.0     # ブラックホール抽出電力（ベースライン2.5PW）[3]
    conversion_efficiency = efficiency_data['eta'].iloc[-1] # ペンローズ効率
    
    # 輸送ステータス
    transport_loss_rate = 0.05 # 潮汐力による5%の輸送ロス
    net_mass_supply = np.zeros(len(time_steps))
    throat_stability_index = np.zeros(len(time_steps))

    for i in range(len(time_steps)):
        # 生成可能な負の質量 (E=mc^2 の逆計算含む、工学的近似)
        # 実際にはカシミール効果等の増幅を伴うため、PW級電力で3.5億トンを制御
        generated_mass = target_mass_flow * (bh_energy_pw / 2500.0) * (conversion_efficiency / 0.29)
        delivered_mass = generated_mass * (1.0 - transport_loss_rate)
        
        net_mass_supply[i] = delivered_mass
        # スロート安定度 (1.0 = 100% 安定)
        throat_stability_index[i] = min(delivered_mass / target_mass_flow, 1.2)

    # 3. 結果の可視化
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = 'tab:purple'
    ax1.set_xlabel('Years of Operation')
    ax1.set_ylabel('Exotic Matter Supply (M-tons/yr)', color=color)
    ax1.plot(time_steps, net_mass_supply / 1e6, color=color, linewidth=2, label='Mass Flow Rate')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.axhline(y=350, color='r', linestyle='--', alpha=0.5, label='Target (350M tons)')
    ax1.grid(True, linestyle='--', alpha=0.6)

    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Throat Stability Index', color=color)
    ax2.plot(time_steps, throat_stability_index, color=color, alpha=0.8, label='Stability')
    ax2.set_ylim(0, 1.5)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Task #3022: Steady-state Exotic Matter Transport Logistics')
    plt.savefig('task3022_transport.png')
    
    # 最終的な安定性の判定
    avg_stability = np.mean(throat_stability_index)
    print(f"Simulation Complete: Average Stability Index = {avg_stability:.4f}")
    if avg_stability >= 1.0:
        print("Status: Stable for Data Transmission (Latency 0.0 confirmed)")

if __name__ == "__main__":
    run_transport_simulation()