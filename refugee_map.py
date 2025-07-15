import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# データを読み込み
print("CSVファイルを読み込み中...")
df = pd.read_csv('hdx_hapi_refugees_global_2020_2024.csv')

# ヘッダー行をスキップ（2行目が実際のヘッダー）
df = df.iloc[1:].reset_index(drop=True)

# カラム名を設定
df.columns = [
    'origin_location_code', 'origin_has_hrp', 'origin_in_gho',
    'asylum_location_code', 'asylum_has_hrp', 'asylum_in_gho',
    'population_group', 'gender', 'age_range', 'min_age', 'max_age',
    'population', 'reference_period_start', 'reference_period_end',
    'dataset_hdx_id', 'resource_hdx_id', 'warning', 'error'
]

# データ型を変換
df['population'] = pd.to_numeric(df['population'], errors='coerce')
df['reference_period_start'] = pd.to_datetime(df['reference_period_start'], errors='coerce')
df['reference_period_end'] = pd.to_datetime(df['reference_period_end'], errors='coerce')

# 年を抽出
df['year'] = df['reference_period_start'].dt.year

print("データの基本情報:")
print(f"データ期間: {df['year'].min()} - {df['year'].max()}")
print(f"総レコード数: {len(df):,}")
print(f"国コード数: {df['asylum_location_code'].nunique()}")

# 1. 避難先国別の難民数集計（最新年）
latest_year = df['year'].max()
latest_data = df[df['year'] == latest_year]

asylum_counts = latest_data.groupby('asylum_location_code')['population'].sum().reset_index()
asylum_counts = asylum_counts.sort_values('population', ascending=False)

print(f"\n{latest_year}年の避難先国別難民数（上位10カ国）:")
print(asylum_counts.head(10))

# 2. 出身国別の難民数集計
origin_counts = latest_data.groupby('origin_location_code')['population'].sum().reset_index()
origin_counts = origin_counts.sort_values('population', ascending=False)

print(f"\n{latest_year}年の出身国別難民数（上位10カ国）:")
print(origin_counts.head(10))

# 3. 年別の総難民数推移
yearly_totals = df.groupby('year')['population'].sum().reset_index()

# 4. インタラクティブな世界地図を作成
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        f'{latest_year}年 避難先国別難民数',
        f'{latest_year}年 出身国別難民数', 
        '年別難民数推移',
        '年齢層別難民数'
    ),
    specs=[[{"type": "choropleth"}, {"type": "choropleth"}],
           [{"type": "bar"}, {"type": "bar"}]]
)

# 避難先国別マップ
fig.add_trace(
    go.Choropleth(
        locations=asylum_counts['asylum_location_code'],
        z=asylum_counts['population'],
        locationmode='ISO-3',
        colorscale='Reds',
        name='避難先国',
        colorbar=dict(title="難民数", x=0.45, y=0.5)
    ),
    row=1, col=1
)

# 出身国別マップ
fig.add_trace(
    go.Choropleth(
        locations=origin_counts['origin_location_code'],
        z=origin_counts['population'],
        locationmode='ISO-3',
        colorscale='Blues',
        name='出身国',
        colorbar=dict(title="難民数", x=0.95, y=0.5)
    ),
    row=1, col=2
)

# 年別推移グラフ
fig.add_trace(
    go.Bar(
        x=yearly_totals['year'],
        y=yearly_totals['population'],
        name='年別総数',
        marker_color='green'
    ),
    row=2, col=1
)

# 年齢層別グラフ
age_data = latest_data.groupby('age_range')['population'].sum().reset_index()
fig.add_trace(
    go.Bar(
        x=age_data['age_range'],
        y=age_data['population'],
        name='年齢層別',
        marker_color='orange'
    ),
    row=2, col=2
)

# レイアウトを更新
fig.update_layout(
    title_text="世界難民分布マップ 2020-2024",
    title_x=0.5,
    height=800,
    showlegend=False
)

# 各サブプロットのレイアウトを更新
fig.update_geos(
    showframe=False,
    showcoastlines=True,
    projection_type="equirectangular"
)

fig.update_xaxes(title_text="年", row=2, col=1)
fig.update_yaxes(title_text="難民数", row=2, col=1)
fig.update_xaxes(title_text="年齢層", row=2, col=2)
fig.update_yaxes(title_text="難民数", row=2, col=2)

# HTMLファイルとして保存
fig.write_html("refugee_world_map.html")
print("\n難民分布マップを 'refugee_world_map.html' として保存しました！")

# 統計情報も表示
print(f"\n=== 統計サマリー ===")
print(f"総難民数（{latest_year}年）: {latest_data['population'].sum():,.0f}")
print(f"データに含まれる国数: {latest_data['asylum_location_code'].nunique()}")
print(f"最大の避難先国: {asylum_counts.iloc[0]['asylum_location_code']} ({asylum_counts.iloc[0]['population']:,.0f}人)")
print(f"最大の出身国: {origin_counts.iloc[0]['origin_location_code']} ({origin_counts.iloc[0]['population']:,.0f}人)")

# 年齢層別の詳細
print(f"\n年齢層別分布（{latest_year}年）:")
for _, row in age_data.iterrows():
    percentage = (row['population'] / age_data['population'].sum()) * 100
    print(f"  {row['age_range']}: {row['population']:,.0f}人 ({percentage:.1f}%)") 