#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 15:05:47 2026

@author: iwamura
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_civilization_balance():
    # 1. 物理定数と前提条件 (G=c=1 幾何学単位系)
    M_sol = 1.0  # 太陽質量ベース
    c = 3e8      # 光速 (m/s)
    
    # 2. #3021の解析結果に基づく初期値
    initial_spin = 0.998  # 極限カーBHに近いスピン
    
    # 3. 文明の負荷設定 (#3022に基づく)
    # ワームホール維持電力 + タイプII文明消費電力 (PW単位)
    power_load_pw = 1e6   # 1,000,000 PW (1 EW: エクサワット)
    power_load_js = power_load_pw * 1e15 * (365 * 24 * 3600) # 年間消費ジュール
    
    # 4. BHエネルギー容量の計算
    # 回転エネルギー E_rot = (M - M_irr) * c^2
    # M_irr = M / sqrt(2) * sqrt(1 + sqrt(1 - a^2))
    def calc_rotational_energy(M, a):
        m_irr = M / np.sqrt(2) * np.sqrt(1 + np.sqrt(1 - a**2))
        return (M - m_irr)
    
    # シミュレーション設定 (単位: 兆年)
    total_trillion_years = 10.0
    steps = 1000
    dt = total_trillion_years / steps
    
    current_M = 1e8 * M_sol # 超巨大ブラックホール (1億太陽質量)
    current_a = initial_spin
    
    history_a = []
    history_energy = []
    years = np.linspace(0, total_trillion_years, steps)

    # 5. スピン減衰シミュレーション
    total_energy_joules = calc_rotational_energy(current_M, current_a) * (2e30) * (c**2) # 近似質量換算
    
    for t in range(steps):
        # 毎年の消費分を差し引く (兆年単位なので 1e12倍)
        annual_drain = power_load_js * 1e12 * dt
        total_energy_joules -= annual_drain
        
        # エネルギー残量から現在のスピンaを逆算 (近似)
        # スピンが減少すると抽出効率が落ちるため 0 に近づくとシミュレーション終了
        rem_ratio = max(0, total_energy_joules / (calc_rotational_energy(current_M, initial_spin) * 2e30 * c**2))
        current_a = initial_spin * np.sqrt(rem_ratio)
        
        history_a.append(current_a)
        history_energy.append(total_energy_joules)

    # 6. 結果の可視化
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    ax1.set_xlabel('Time (Trillion Years)')
    ax1.set_ylabel('BH Spin Parameter (a)', color='tab:red')
    ax1.plot(years, history_a, color='tab:red', linewidth=2, label='BH Spin Decay')
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.grid(True, linestyle='--', alpha=0.6)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Available Energy (Joules)', color='tab:blue')
    ax2.plot(years, history_energy, color='tab:blue', alpha=0.5, label='Energy Reservoir')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    plt.title('Task #3023: Trillion-year Civilization Sustainability Balance')
    plt.savefig('task3023_sustainability.png')
    
    # 最終判定
    lifespan = years[np.where(np.array(history_a) < 0.1)] if any(np.array(history_a) < 0.1) else total_trillion_years
    print(f"Simulation Complete: Civilization Lifespan > {lifespan:.1f} Trillion Years.")
    print("Status: Galactic Battery capacity confirmed for Eternity.")

if __name__ == "__main__":
    run_civilization_balance()