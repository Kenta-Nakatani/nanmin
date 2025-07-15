import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def load_and_clean_data():
    """データの読み込みとクリーニング"""
    print("📊 データを読み込み中...")
    df = pd.read_csv('hdx_hapi_refugees_global_2020_2024.csv')
    
    # ヘッダー行をスキップ
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
    df['year'] = df['reference_period_start'].dt.year
    
    # 欠損値を除去
    df = df.dropna(subset=['population', 'asylum_location_code', 'origin_location_code'])
    
    return df

def create_comprehensive_map(df):
    """包括的な難民分布マップを作成"""
    print("🗺️ 世界地図を作成中...")
    
    # 最新年のデータを取得
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year]
    
    # 避難先国別集計
    asylum_counts = latest_data.groupby('asylum_location_code')['population'].sum().reset_index()
    asylum_counts = asylum_counts.sort_values('population', ascending=False)
    
    # 出身国別集計
    origin_counts = latest_data.groupby('origin_location_code')['population'].sum().reset_index()
    origin_counts = origin_counts.sort_values('population', ascending=False)
    
    # 年別推移
    yearly_totals = df.groupby('year')['population'].sum().reset_index()
    
    # 年齢層別集計
    age_data = latest_data.groupby('age_range')['population'].sum().reset_index()
    
    # 性別別集計
    gender_data = latest_data.groupby('gender')['population'].sum().reset_index()
    gender_data['gender_label'] = gender_data['gender'].map({'f': '女性', 'm': '男性'})
    
    # サブプロットを作成
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            f'🌍 {latest_year}年 避難先国別難民数',
            f'🏠 {latest_year}年 出身国別難民数',
            '📈 年別難民数推移',
            '👥 年齢層別難民数',
            '👨‍👩‍👧‍👦 性別別難民数',
            '🏆 上位10カ国（避難先）'
        ),
        specs=[
            [{"type": "choropleth"}, {"type": "choropleth"}],
            [{"type": "scatter"}, {"type": "bar"}],
            [{"type": "bar"}, {"type": "bar"}]
        ],
        vertical_spacing=0.08,
        horizontal_spacing=0.05
    )
    
    # 1. 避難先国別マップ
    fig.add_trace(
        go.Choropleth(
            locations=asylum_counts['asylum_location_code'],
            z=asylum_counts['population'],
            locationmode='ISO-3',
            colorscale='Reds',
            name='避難先国',
            colorbar=dict(title="難民数", x=0.45, y=0.8),
            hovertemplate='<b>%{location}</b><br>難民数: %{z:,.0f}人<extra></extra>'
        ),
        row=1, col=1
    )
    
    # 2. 出身国別マップ
    fig.add_trace(
        go.Choropleth(
            locations=origin_counts['origin_location_code'],
            z=origin_counts['population'],
            locationmode='ISO-3',
            colorscale='Blues',
            name='出身国',
            colorbar=dict(title="難民数", x=0.95, y=0.8),
            hovertemplate='<b>%{location}</b><br>難民数: %{z:,.0f}人<extra></extra>'
        ),
        row=1, col=2
    )
    
    # 3. 年別推移（線グラフ）
    fig.add_trace(
        go.Scatter(
            x=yearly_totals['year'],
            y=yearly_totals['population'],
            mode='lines+markers',
            name='年別総数',
            line=dict(color='green', width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{x}年</b><br>難民数: %{y:,.0f}人<extra></extra>'
        ),
        row=2, col=1
    )
    
    # 4. 年齢層別グラフ
    fig.add_trace(
        go.Bar(
            x=age_data['age_range'],
            y=age_data['population'],
            name='年齢層別',
            marker_color='orange',
            hovertemplate='<b>%{x}</b><br>難民数: %{y:,.0f}人<extra></extra>'
        ),
        row=2, col=2
    )
    
    # 5. 性別別グラフ
    fig.add_trace(
        go.Bar(
            x=gender_data['gender_label'],
            y=gender_data['population'],
            name='性別別',
            marker_color=['pink', 'lightblue'],
            hovertemplate='<b>%{x}</b><br>難民数: %{y:,.0f}人<extra></extra>'
        ),
        row=3, col=1
    )
    
    # 6. 上位10カ国（避難先）
    top_10_asylum = asylum_counts.head(10)
    fig.add_trace(
        go.Bar(
            x=top_10_asylum['asylum_location_code'],
            y=top_10_asylum['population'],
            name='上位10カ国',
            marker_color='red',
            hovertemplate='<b>%{x}</b><br>難民数: %{y:,.0f}人<extra></extra>'
        ),
        row=3, col=2
    )
    
    # レイアウトを更新
    fig.update_layout(
        title_text="🌍 世界難民分布マップ 2020-2024 📊",
        title_x=0.5,
        title_font_size=20,
        height=1200,
        showlegend=False,
        template="plotly_white"
    )
    
    # 地理的プロットの設定
    fig.update_geos(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="gray",
        showland=True,
        landcolor="lightgray",
        showocean=True,
        oceancolor="lightblue",
        projection_type="equirectangular"
    )
    
    # 軸ラベルの設定
    fig.update_xaxes(title_text="年", row=2, col=1)
    fig.update_yaxes(title_text="難民数", row=2, col=1)
    fig.update_xaxes(title_text="年齢層", row=2, col=2)
    fig.update_yaxes(title_text="難民数", row=2, col=2)
    fig.update_xaxes(title_text="性別", row=3, col=1)
    fig.update_yaxes(title_text="難民数", row=3, col=1)
    fig.update_xaxes(title_text="国コード", row=3, col=2)
    fig.update_yaxes(title_text="難民数", row=3, col=2)
    
    return fig, latest_data, asylum_counts, origin_counts

def print_statistics(latest_data, asylum_counts, origin_counts):
    """統計情報を表示"""
    print("\n" + "="*60)
    print("📊 統計サマリー")
    print("="*60)
    
    latest_year = latest_data['year'].iloc[0]
    total_refugees = latest_data['population'].sum()
    
    print(f"📅 データ期間: 2020-{latest_year}")
    print(f"🌍 総難民数（{latest_year}年）: {total_refugees:,.0f}人")
    print(f"🏳️ データに含まれる国数: {latest_data['asylum_location_code'].nunique()}")
    
    print(f"\n🏆 最大の避難先国: {asylum_counts.iloc[0]['asylum_location_code']} ({asylum_counts.iloc[0]['population']:,.0f}人)")
    print(f"🏆 最大の出身国: {origin_counts.iloc[0]['origin_location_code']} ({origin_counts.iloc[0]['population']:,.0f}人)")
    
    # 年齢層別の詳細
    age_data = latest_data.groupby('age_range')['population'].sum().reset_index()
    print(f"\n👥 年齢層別分布（{latest_year}年）:")
    for _, row in age_data.iterrows():
        percentage = (row['population'] / age_data['population'].sum()) * 100
        print(f"  {row['age_range']}: {row['population']:,.0f}人 ({percentage:.1f}%)")
    
    # 性別別の詳細
    gender_data = latest_data.groupby('gender')['population'].sum().reset_index()
    print(f"\n👨‍👩‍👧‍👦 性別別分布（{latest_year}年）:")
    for _, row in gender_data.iterrows():
        gender_label = "女性" if row['gender'] == 'f' else "男性"
        percentage = (row['population'] / gender_data['population'].sum()) * 100
        print(f"  {gender_label}: {row['population']:,.0f}人 ({percentage:.1f}%)")

def main():
    """メイン関数"""
    try:
        # データ読み込み
        df = load_and_clean_data()
        
        # マップ作成
        fig, latest_data, asylum_counts, origin_counts = create_comprehensive_map(df)
        
        # HTMLファイルとして保存
        fig.write_html("refugee_world_map_interactive.html")
        print("\n✅ 難民分布マップを 'refugee_world_map_interactive.html' として保存しました！")
        
        # 統計情報表示
        print_statistics(latest_data, asylum_counts, origin_counts)
        
        print(f"\n🎉 分析完了！ブラウザで 'refugee_world_map_interactive.html' を開いてインタラクティブなマップをご覧ください。")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    main() 