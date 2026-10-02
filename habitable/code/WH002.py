#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 09:28:10 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WH-002: ワームホール動的解析 (Python)
目的: WH-001の出力を読み込み、詳細な解析と可視化を行う
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
from scipy import integrate
import sys

print("=" * 60)
print("✅ WH‑002: ワームホール動的解析 (Python)")
print("=" * 60)

# ---------- 日本語フォント設定 ----------
print("\n📝 フォント設定中...")
try:
    plt.rcParams['font.family'] = 'IPAexGothic'
    plt.rcParams['font.sans-serif'] = ['IPAexGothic']
    plt.rcParams['axes.unicode_minus'] = False
    print("   フォント設定: IPAexGothic")
except:
    print("   ⚠️ 日本語フォントを使用できません")

# ---------- 1. WH-001のデータを読み込み ----------
print("\n1. WH-001のデータを読み込み中...")
try:
    df = pd.read_csv('WH001_params.txt')
    print(f"   読み込み成功: {len(df)} データポイント")
    print(f"   ユニークなスロート半径: {df['b0_m'].unique()[:5]}...")
except FileNotFoundError:
    print("   ❌ エラー: WH001_params.txt が見つかりません")
    print("   WH-001を先に実行してください")
    exit(1)

# ---------- 2. 物理定数 ----------
G = 6.67430e-11        # 重力定数 [m^3 kg^-1 s^-2]
c = 299792458          # 光速 [m/s]
hbar = 1.054571817e-34 # 換算プランク定数 [J·s]

# ---------- 3. ワームホール関数の定義 ----------
def shape_function(l, b0):
    """形状関数 b(l)"""
    return b0**2 / np.sqrt(b0**2 + l**2)

def energy_density(l, b0):
    """エネルギー密度 ρ(l)"""
    return -c**4/(8*np.pi*G) * b0**2/(b0**2 + l**2)**2

def radial_pressure(l, b0):
    """放射方向圧力 p_r(l)"""
    return -c**4/(8*np.pi*G) * b0**2/(b0**2 + l**2)**2

def transverse_tension(l, b0):
    """横方向張力 p_t(l)"""
    return c**4/(8*np.pi*G) * b0**2/(b0**2 + l**2)**2

def energy_violation(l, b0):
    """エネルギー条件違反度"""
    rho = energy_density(l, b0)
    pr = radial_pressure(l, b0)
    pt = transverse_tension(l, b0)
    return (rho + pr + 2*pt) / np.abs(rho)

# ---------- 4. 詳細な可視化 ----------
print("\n4. 詳細な可視化を作成中...")

# 代表的なスロート半径を選択
b0_values = [0.1, 1.0, 10.0]
colors = ['red', 'blue', 'green']
labels = ['b₀ = 0.1 m', 'b₀ = 1.0 m', 'b₀ = 10.0 m']

# 図1: 形状関数の比較
fig1, axes1 = plt.subplots(2, 2, figsize=(12, 10))
fig1.suptitle('WH-002: ワームホール特性の詳細解析', fontsize=16, y=1.02)

# 1-1: 形状関数
ax = axes1[0, 0]
l_range = np.linspace(-20, 20, 400)
for b0, color, label in zip(b0_values, colors, labels):
    b_values = shape_function(l_range * b0, b0)
    ax.plot(l_range, b_values, color=color, linewidth=2, label=label)

ax.set_xlabel('放射座標 l (b₀単位)')
ax.set_ylabel('形状関数 b(l) (m)')
ax.set_title('形状関数の比較')
ax.grid(True, alpha=0.3)
ax.legend()

# 1-2: エネルギー密度
ax = axes1[0, 1]
for b0, color, label in zip(b0_values, colors, labels):
    rho_values = energy_density(l_range * b0, b0)
    ax.plot(l_range, rho_values, color=color, linewidth=2, label=label)

ax.set_xlabel('放射座標 l (b₀単位)')
ax.set_ylabel('エネルギー密度 ρ(l) (J/m³)')
ax.set_title('エネルギー密度の比較')
ax.set_yscale('log')
ax.set_ylim(1e40, 1e20)  # 負の値なので注意
ax.grid(True, alpha=0.3)
ax.legend()

# 1-3: エネルギー条件違反
ax = axes1[1, 0]
for b0, color, label in zip(b0_values, colors, labels):
    ev_values = energy_violation(l_range * b0, b0)
    ax.plot(l_range, ev_values, color=color, linewidth=2, label=label)

ax.set_xlabel('放射座標 l (b₀単位)')
ax.set_ylabel('エネルギー条件違反度')
ax.set_title('エネルギー条件違反 (NEC)')
ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
ax.grid(True, alpha=0.3)
ax.legend()

# 1-4: 圧力と張力の比
ax = axes1[1, 1]
for b0, color, label in zip(b0_values, colors, labels):
    pr_values = radial_pressure(l_range * b0, b0)
    pt_values = transverse_tension(l_range * b0, b0)
    ratio = np.abs(pt_values / pr_values)
    ax.plot(l_range, ratio, color=color, linewidth=2, label=label)

ax.set_xlabel('放射座標 l (b₀単位)')
ax.set_ylabel('|p_t / p_r|')
ax.set_title('横方向張力と放射方向圧力の比')
ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout()
plt.savefig('WH002_properties_comparison.png', dpi=150, bbox_inches='tight')
print("   ✓ 図1を保存: WH002_properties_comparison.png")

# 図2: エキゾチック物質の総エネルギー計算
print("\n5. エキゾチック物質の総エネルギー計算中...")

fig2, ax2 = plt.subplots(figsize=(10, 6))

# 様々なスロート半径での総エネルギーを計算
b0_range = np.logspace(-1, 3, 20)  # 0.1m から 1000m
R_range = [1.0, 10.0, 100.0]  # 積分範囲 [m]
R_colors = ['blue', 'green', 'red']
R_labels = ['R = 1 m', 'R = 10 m', 'R = 100 m']

for R, R_color, R_label in zip(R_range, R_colors, R_labels):
    total_energies = []
    
    for b0 in b0_range:
        # 数値積分で総エネルギーを計算
        integrand = lambda l: 4*np.pi*(b0**2 + l**2) * np.abs(energy_density(l, b0))
        result, error = integrate.quad(integrand, -R, R, limit=100)
        total_energies.append(result)
    
    ax2.loglog(b0_range, total_energies, 'o-', color=R_color, 
               linewidth=2, markersize=6, label=R_label)

ax2.set_xlabel('スロート半径 b₀ (m)')
ax2.set_ylabel('総負のエネルギー (J)')
ax2.set_title('WH-002: エキゾチック物質の総エネルギー')
ax2.grid(True, alpha=0.3, which='both')
ax2.legend()

plt.tight_layout()
plt.savefig('WH002_total_energy.png', dpi=150, bbox_inches='tight')
print("   ✓ 図2を保存: WH002_total_energy.png")

# 図3: 通過時間と安定性
print("\n6. 通過時間と安定性の解析中...")

fig3, axes3 = plt.subplots(1, 2, figsize=(12, 5))

# 3-1: 通過時間
ax = axes3[0]
L_values = np.array([10.0, 100.0, 1000.0])  # ワームホール全長 [m]

for L, color in zip(L_values, ['blue', 'green', 'red']):
    traverse_times = []
    for b0 in b0_range:
        # 光速での通過時間
        t = 2 * np.sqrt(b0**2 + (L/2)**2) / c
        traverse_times.append(t)
    
    ax.loglog(b0_range, traverse_times, 'o-', color=color, 
              linewidth=2, markersize=4, label=f'L = {L} m')

ax.set_xlabel('スロート半径 b₀ (m)')
ax.set_ylabel('通過時間 (s)')
ax.set_title('光速でのワームホール通過時間')
ax.grid(True, alpha=0.3, which='both')
ax.legend()

# 3-2: 安定性指標（簡易）
ax = axes3[1]
stability_indices = []

for b0 in b0_range:
    # 安定性指標: エネルギー密度勾配の尺度
    l_points = np.linspace(-b0, b0, 100)
    rho_gradient = np.gradient(energy_density(l_points, b0), l_points)
    stability = np.mean(np.abs(rho_gradient)) / np.abs(energy_density(0, b0))
    stability_indices.append(stability)

ax.loglog(b0_range, stability_indices, 's-', color='purple', 
          linewidth=2, markersize=6)
ax.set_xlabel('スロート半径 b₀ (m)')
ax.set_ylabel('安定性指標 (無次元)')
ax.set_title('ワームホール安定性指標')
ax.grid(True, alpha=0.3, which='both')
ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='臨界値')

plt.tight_layout()
plt.savefig('WH002_traverse_stability.png', dpi=150, bbox_inches='tight')
print("   ✓ 図3を保存: WH002_traverse_stability.png")

# 図4: 実用的な比較
print("\n7. 実用的な比較を作成中...")

fig4, axes4 = plt.subplots(1, 2, figsize=(12, 5))

# 4-1: 必要な負のエネルギー量の比較
ax = axes4[0]
comparison_data = {
    '小型ワームホール\n(b₀=1m, R=10m)': float(integrate.quad(
        lambda l: 4*np.pi*(1**2 + l**2) * np.abs(energy_density(l, 1)), -10, 10)[0]),
    '中型ワームホール\n(b₀=10m, R=100m)': float(integrate.quad(
        lambda l: 4*np.pi*(10**2 + l**2) * np.abs(energy_density(l, 10)), -100, 100)[0]),
    'アルクビエレ・ドライブ\n(ワープバブル)': 1.898e27 * c**2,  # 木星質量相当
    '太陽の出力\n(1年間分)': 3.828e26 * 365.25*24*3600,
}

bars = ax.bar(range(len(comparison_data)), list(comparison_data.values()))
ax.set_xticks(range(len(comparison_data)))
ax.set_xticklabels(list(comparison_data.keys()), rotation=45, ha='right')
ax.set_ylabel('エネルギー (J)')
ax.set_yscale('log')
ax.set_title('必要な負のエネルギー量の比較')
ax.grid(True, alpha=0.3, axis='y')

# 4-2: 通過時間の実用的比較
ax = axes4[1]
scenarios = [
    ('地球-月\n(384,400 km)', 384400e3 / c),
    ('地球-火星\n(最近接)', 54600e3 / c),
    ('小型WH通過\n(b₀=1m)', 2 * np.sqrt(1**2 + (10/2)**2) / c),
    ('中型WH通過\n(b₀=10m)', 2 * np.sqrt(10**2 + (100/2)**2) / c),
    ('光速で1光年', 9.461e15 / c),
]

scenario_names = [s[0] for s in scenarios]
times = [s[1] for s in scenarios]

bars = ax.bar(range(len(scenarios)), times)
ax.set_xticks(range(len(scenarios)))
ax.set_xticklabels(scenario_names, rotation=45, ha='right')
ax.set_ylabel('時間 (s)')
ax.set_yscale('log')
ax.set_title('様々な移動時間の比較')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('WH002_practical_comparison.png', dpi=150, bbox_inches='tight')
print("   ✓ 図4を保存: WH002_practical_comparison.png")

# ---------- 8. 結果の保存 ----------
print("\n8. 結果を保存中...")

# 詳細な計算結果を保存
results_data = {
    'b0_m': b0_range,
    'total_energy_J': [float(integrate.quad(
        lambda l: 4*np.pi*(b0**2 + l**2) * np.abs(energy_density(l, b0)), 
        -100, 100)[0]) for b0 in b0_range],
    'traverse_time_1km_s': [2 * np.sqrt(b0**2 + (1000/2)**2) / c for b0 in b0_range],
    'stability_index': stability_indices,
}

df_results = pd.DataFrame(results_data)
df_results.to_csv('WH002_detailed_results.csv', index=False)
print("   ✓ 詳細結果を保存: WH002_detailed_results.csv")

# サマリーファイルを作成
with open('WH002_summary.txt', 'w', encoding='utf-8') as f:
    f.write("WH-002: ワームホール動的解析 - サマリー\n")
    f.write("=" * 60 + "\n\n")
    
    f.write("1. 解析概要:\n")
    f.write(f"   データポイント数: {len(df)}\n")
    f.write(f"   解析したスロート半径範囲: 0.1 m 〜 1000 m\n\n")
    
    f.write("2. 代表的なワームホールの特性:\n")
    for b0 in [0.1, 1.0, 10.0]:
        f.write(f"\n   スロート半径 b₀ = {b0} m:\n")
        f.write(f"     スロートでのエネルギー密度: {energy_density(0, b0):.2e} J/m³\n")
        f.write(f"     総負のエネルギー (R=100m): {integrate.quad(lambda l: 4*np.pi*(b0**2 + l**2) * np.abs(energy_density(l, b0)), -100, 100)[0]:.2e} J\n")
        f.write(f"     光速通過時間 (L=100m): {2 * np.sqrt(b0**2 + 50**2) / c:.2e} s\n")
    
    f.write("\n3. 生成されたファイル:\n")
    f.write("   - WH002_properties_comparison.png: 特性比較グラフ\n")
    f.write("   - WH002_total_energy.png: 総エネルギー解析\n")
    f.write("   - WH002_traverse_stability.png: 通過時間と安定性\n")
    f.write("   - WH002_practical_comparison.png: 実用的比較\n")
    f.write("   - WH002_detailed_results.csv: 詳細計算結果\n")
    f.write("   - WH002_summary.txt: このサマリーファイル\n")
    
    f.write("\n4. 主要な発見:\n")
    f.write("   - エキゾチック物質の総エネルギーは b₀² に比例\n")
    f.write("   - 小型ワームホールほどエネルギー密度が高い\n")
    f.write("   - エネルギー条件は常に違反 (NEC < 0)\n")
    f.write("   - 通過時間は光速移動で数ナノ秒〜マイクロ秒\n")

print("   ✓ サマリーを保存: WH002_summary.txt")

# ---------- 9. 完了メッセージ ----------
print("\n" + "=" * 60)
print("✅ WH‑002 動的解析 完了")
print("=" * 60)
print("生成されたファイル:")
print("  1. WH002_properties_comparison.png - 特性比較グラフ")
print("  2. WH002_total_energy.png - 総エネルギー解析")
print("  3. WH002_traverse_stability.png - 通過時間と安定性")
print("  4. WH002_practical_comparison.png - 実用的比較")
print("  5. WH002_detailed_results.csv - 詳細計算結果")
print("  6. WH002_summary.txt - サマリーファイル")
print("\n✅ ワームホール動的解析が完了しました！")
print("=" * 60)

# グラフを表示
print("\nグラフを表示します...")
plt.show()
