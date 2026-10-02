#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 19:16:25 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BH-002: ブラックホール動的解析 (Python) - 日本語版
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import matplotlib.font_manager as fm
import sys

print("=" * 60)
print("✅ BH‑002: ブラックホール動的解析 (Python)")
print("=" * 60)

# ---------- 日本語フォント設定 ----------
print("\n📝 フォント設定中...")
try:
    # IPAexGothicを設定（見つかっているので）
    plt.rcParams['font.family'] = 'IPAexGothic'
    plt.rcParams['font.sans-serif'] = ['IPAexGothic']
    plt.rcParams['axes.unicode_minus'] = False  # マイナス記号の表示を修正
    
    print("   フォント設定: IPAexGothic")
    print("   日本語表示が有効になりました")
    
except Exception as e:
    print(f"   ⚠️ フォント設定エラー: {e}")
    print("   英語表示で続行します")

# ---------- 1. BH-001のデータを読み込み ----------
print("\n1. BH-001のデータを読み込み中...")
try:
    df = pd.read_csv('BH001_params.txt')
    print(f"   読み込み成功: {len(df)} データポイント")
except FileNotFoundError:
    print("   ❌ エラー: BH001_params.txt が見つかりません")
    print("   BH-001を先に実行してください")
    exit(1)

# ---------- 2. データの前処理 ----------
print("\n2. データの前処理...")
mass = df['mass_kg'].values
radius = df['Rs_m'].values
gravity = df['kappa_ms2'].values
temperature = df['T_K'].values
power = df['P_W'].values
evap_time = df['tau_s'].values

# 年単位に変換
evap_time_years = evap_time / (365.25 * 24 * 3600)

# ---------- 3. 追加計算: ペンローズ過程 ----------
print("\n3. 追加計算: ペンローズ過程のエネルギー抽出")
c = 299792458  # 光速 [m/s]
extractable_energy_ratio = 0.29
extractable_energy = extractable_energy_ratio * mass * c**2

# ペンローズ過程の効率
a_values = np.array([0.0, 0.5, 0.9, 0.99, 0.999])
penrose_efficiency = 1 - np.sqrt((1 + np.sqrt(1 - a_values**2))/2)

print("   回転パラメータ a に対するペンローズ効率:")
for a, eff in zip(a_values, penrose_efficiency):
    print(f"     a = {a:.3f} : η = {eff:.3%}")

# ---------- 4. 詳細な可視化（日本語ラベル） ----------
print("\n4. 詳細な可視化を作成中...")

# 図1: すべての関係をサブプロットで表示
fig1, axes1 = plt.subplots(2, 3, figsize=(16, 10))
fig1.suptitle('BH-002: ブラックホール特性の詳細解析', fontsize=16, y=1.02)

# 1-1: 質量 vs 半径
ax = axes1[0, 0]
ax.loglog(mass, radius, 'b-', linewidth=2, marker='o', markersize=4)
ax.set_xlabel('質量 (kg)')
ax.set_ylabel('シュワルツシルト半径 (m)')
ax.set_title('質量 vs 事象の地平線半径')
ax.grid(True, alpha=0.3)

# 1-2: 質量 vs 表面重力
ax = axes1[0, 1]
ax.loglog(mass, gravity, 'r-', linewidth=2, marker='s', markersize=4)
ax.set_xlabel('質量 (kg)')
ax.set_ylabel('表面重力 (m/s²)')
ax.set_title('質量 vs 表面重力')
ax.grid(True, alpha=0.3)

# 1-3: 質量 vs 温度
ax = axes1[0, 2]
ax.loglog(mass, temperature, 'g-', linewidth=2, marker='^', markersize=4)
ax.set_xlabel('質量 (kg)')
ax.set_ylabel('ホーキング温度 (K)')
ax.set_title('質量 vs ホーキング温度')
ax.grid(True, alpha=0.3)

# 1-4: 質量 vs 放射パワー
ax = axes1[1, 0]
ax.loglog(mass, power, 'm-', linewidth=2, marker='d', markersize=4)
ax.set_xlabel('質量 (kg)')
ax.set_ylabel('ホーキング放射 (W)')
ax.set_title('質量 vs ホーキング放射')
ax.grid(True, alpha=0.3)

# 1-5: 質量 vs 蒸発時間（年単位）
ax = axes1[1, 1]
ax.loglog(mass, evap_time_years, 'c-', linewidth=2, marker='v', markersize=4)
ax.set_xlabel('質量 (kg)')
ax.set_ylabel('蒸発時間 (年)')
ax.set_title('質量 vs 蒸発時間')
ax.grid(True, alpha=0.3)

# 1-6: 抽出可能エネルギー
ax = axes1[1, 2]
ax.loglog(mass, extractable_energy, 'y-', linewidth=2, marker='*', markersize=4)
ax.set_xlabel('質量 (kg)')
ax.set_ylabel('抽出可能エネルギー (J)')
ax.set_title('ペンローズ過程: 抽出可能エネルギー')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('BH002_all_properties_ja.png', dpi=150, bbox_inches='tight')
print("   ✓ 図1を保存: BH002_all_properties_ja.png")

# 図2: ペンローズ過程の詳細
fig2, ax2 = plt.subplots(figsize=(10, 6))
colors = plt.cm.viridis(np.linspace(0, 1, len(a_values)))

for i, (a, eff, color) in enumerate(zip(a_values, penrose_efficiency, colors)):
    energy_extracted = eff * extractable_energy
    ax2.loglog(mass, energy_extracted, '-', color=color, linewidth=2, 
               label=f'a = {a:.3f} (η = {eff:.1%})')

ax2.set_xlabel('質量 (kg)', fontsize=12)
ax2.set_ylabel('ペンローズ過程による抽出可能エネルギー (J)', fontsize=12)
ax2.set_title('BH-002: ペンローズ過程によるエネルギー抽出', fontsize=14)
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10)
plt.tight_layout()
plt.savefig('BH002_penrose_process_ja.png', dpi=150, bbox_inches='tight')
print("   ✓ 図2を保存: BH002_penrose_process_ja.png")

# 図3: 実用的な比較
fig3, axes3 = plt.subplots(1, 2, figsize=(13, 5))

# 3-1: 太陽質量との比較
ax = axes3[0]
sun_mass = 1.989e30
sun_index = np.argmin(np.abs(mass - sun_mass))

comparison_masses = np.array([1.0, 70.0, 5.972e24, 1.989e30])
comparison_labels = ['1 kg', '人間 (70 kg)', '地球', '太陽']

for m, label in zip(comparison_masses, comparison_labels):
    idx = np.argmin(np.abs(mass - m))
    ax.scatter(mass[idx]/sun_mass, evap_time_years[idx], s=100, label=label)

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('質量 (太陽質量単位)')
ax.set_ylabel('蒸発時間 (年)')
ax.set_title('様々な質量のブラックホールの蒸発時間')
ax.grid(True, alpha=0.3)
ax.legend()

# 3-2: エネルギー比較
ax = axes3[1]
energy_sources = {
    'ホーキング放射': power[sun_index],
    'ペンローズ (a=0.99)': penrose_efficiency[3] * extractable_energy[sun_index] / evap_time[sun_index],
    '太陽の出力': 3.828e26,
    '人類文明の消費': 1.8e13,
}

bars = ax.bar(range(len(energy_sources)), list(energy_sources.values()))
ax.set_xticks(range(len(energy_sources)))
ax.set_xticklabels(list(energy_sources.keys()), rotation=45, ha='right')
ax.set_ylabel('出力 (W)')
ax.set_yscale('log')
ax.set_title('太陽質量ブラックホールのエネルギー出力比較')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('BH002_practical_comparison_ja.png', dpi=150, bbox_inches='tight')
print("   ✓ 図3を保存: BH002_practical_comparison_ja.png")

# ---------- 5. 結果の保存 ----------
print("\n5. 結果を保存中...")

# 追加計算結果をCSVに保存
df_results = pd.DataFrame({
    '質量_kg': mass,
    'シュワルツシルト半径_m': radius,
    '表面重力_ms2': gravity,
    'ホーキング温度_K': temperature,
    'ホーキング放射_W': power,
    '蒸発時間_s': evap_time,
    '蒸発時間_年': evap_time_years,
    '抽出可能エネルギー_J': extractable_energy,
    '単位質量当たり抽出可能エネルギー_Jkg': extractable_energy / mass
})

df_results.to_csv('BH002_detailed_results_ja.csv', index=False)
print("   ✓ データを保存: BH002_detailed_results_ja.csv")

# サマリーファイルを作成（日本語）
with open('BH002_summary_ja.txt', 'w', encoding='utf-8') as f:
    f.write("BH-002: ブラックホール動的解析 - サマリー\n")
    f.write("=" * 60 + "\n\n")
    
    f.write("1. データ概要:\n")
    f.write(f"   データポイント数: {len(df)}\n")
    f.write(f"   質量範囲: {mass[0]:.2e} kg 〜 {mass[-1]:.2e} kg\n\n")
    
    f.write("2. 代表的なブラックホールの特性:\n")
    for m, label in zip(comparison_masses, comparison_labels):
        idx = np.argmin(np.abs(mass - m))
        f.write(f"\n   {label} ({m:.2e} kg):\n")
        f.write(f"     シュワルツシルト半径: {radius[idx]:.2e} m\n")
        f.write(f"     表面重力: {gravity[idx]:.2e} m/s²\n")
        f.write(f"     ホーキング温度: {temperature[idx]:.2e} K\n")
        f.write(f"     ホーキング放射: {power[idx]:.2e} W\n")
        f.write(f"     蒸発時間: {evap_time_years[idx]:.2e} 年\n")
        f.write(f"     抽出可能エネルギー: {extractable_energy[idx]:.2e} J\n")
    
    f.write("\n3. ペンローズ過程の効率:\n")
    for a, eff in zip(a_values, penrose_efficiency):
        f.write(f"   回転パラメータ a = {a:.3f}: 効率 η = {eff:.3%}\n")
    
    f.write("\n4. 生成されたファイル:\n")
    f.write("   - BH002_all_properties_ja.png: 全特性のサブプロット\n")
    f.write("   - BH002_penrose_process_ja.png: ペンローズ過程の詳細\n")
    f.write("   - BH002_practical_comparison_ja.png: 実用的比較\n")
    f.write("   - BH002_detailed_results_ja.csv: 詳細な計算結果\n")
    f.write("   - BH002_summary_ja.txt: このサマリーファイル\n")

print("   ✓ サマリーを保存: BH002_summary_ja.txt")

# ---------- 6. 完了メッセージ ----------
print("\n" + "=" * 60)
print("✅ BH‑002 動的解析 完了")
print("=" * 60)
print("生成されたファイル:")
print("  1. BH002_all_properties_ja.png - 全特性のサブプロット")
print("  2. BH002_penrose_process_ja.png - ペンローズ過程の詳細")
print("  3. BH002_practical_comparison_ja.png - 実用的比較")
print("  4. BH002_detailed_results_ja.csv - 詳細な計算結果")
print("  5. BH002_summary_ja.txt - サマリーファイル")
print("\n✅ 日本語表示でグラフが作成されました！")
print("=" * 60)

# グラフを表示
print("\nグラフを表示します...")
plt.show()
