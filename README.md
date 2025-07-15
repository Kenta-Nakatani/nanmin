# 🌍 世界難民分布マップ 2020-2024

HDX (Humanitarian Data Exchange) HAPIから取得した2020年から2024年までの世界の難民データを可視化したプロジェクトです。

## 📊 データについて

- **データソース**: HDX HAPI Refugees Global Dataset
- **データ期間**: 2020年1月1日 - 2024年12月31日
- **データサイズ**: 約60万レコード
- **含まれる情報**: 出身国、避難先国、年齢層、性別、人口数

## 📁 ファイル構成

### メインファイル
- `hdx_hapi_refugees_global_2020_2024.csv` - 元データ（HDX HAPIから取得）
- `refugee_map_simple.html` - サンプルデータ版の難民分布マップ
- `refugee_map_with_data.html` - **実データ版の難民分布マップ（推奨）**

### 分析スクリプト
- `refugee_analysis.py` - Python版の分析スクリプト（pandas + plotly）
- `refugee_map.py` - シンプルなPython版マップ作成スクリプト

## 🚀 使い方

### 🌐 オンライン版（推奨）
GitHub Pagesで公開されているバージョンにアクセス：
- **メインページ**: [https://yourusername.github.io/refugee-data-visualization](https://yourusername.github.io/refugee-data-visualization)
- **直接マップ**: [https://yourusername.github.io/refugee-data-visualization/refugee_map_with_data.html](https://yourusername.github.io/refugee-data-visualization/refugee_map_with_data.html)

### 1. ローカル版 - 実データ版マップ（推奨）
```bash
# ブラウザで開く
refugee_map_with_data.html
```

**特徴:**
- 実際のCSVデータを読み込み
- インタラクティブな世界地図
- 年別推移、年齢層別、性別別のグラフ
- リアルタイム統計情報
- レスポンシブデザイン

### 2. サンプル版マップ
```bash
# ブラウザで開く
refugee_map_simple.html
```

**特徴:**
- サンプルデータを使用
- 基本的な世界地図表示
- 軽量で高速

### 3. Python版（オプション）
```bash
# 必要なライブラリをインストール
pip install pandas plotly

# スクリプトを実行
python refugee_analysis.py
```

## 🗺️ マップの機能

### 世界地図
- **避難先国別難民数**: 赤色の濃さで難民数を表示
- **インタラクティブ操作**: ズーム、パン、ホバー情報
- **国コード表示**: ISO-3形式の国コード

### 統計情報
- 総難民数（最新年）
- 対象国数
- データ期間
- データポイント数
- 最大避難先国
- 最大出身国

### 追加グラフ
- **年別難民数推移**: 2020-2024年の変化
- **年齢層別分布**: 0-4歳、5-11歳、12-17歳、18-59歳、60+
- **性別別分布**: 男性・女性の比率
- **上位10カ国**: 避難先国別ランキング

## 🎯 データの活用例

### 1. 政策・人道支援
- 支援ニーズの特定
- 資源配分の最適化
- 国際協力の優先順位決定

### 2. 研究・分析
- 難民移動パターンの分析
- 地域別の傾向把握
- 時系列での変化追跡

### 3. 教育・啓発
- 難民問題の理解促進
- データリテラシーの向上
- 国際問題への関心喚起

## 🔧 技術仕様

### 使用技術
- **HTML5/CSS3**: モダンなレスポンシブデザイン
- **JavaScript**: インタラクティブ機能
- **Plotly.js**: データ可視化ライブラリ
- **PapaParse**: CSV解析ライブラリ

### ブラウザ対応
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 📈 データの見方

### データ除外について
- **国内避難民（IDP）**: 出身国と避難先国が同じデータは除外
- **イラン（IRN）**: データの信頼性の問題により除外
- **ゼロ値**: 人口数が0のデータは除外
- **重複データ**: 年齢・性別の総計行（all,all）は除外

### 色の意味
- **赤色**: 難民数が多いほど濃い赤
- **白色**: データなしまたは難民数が少ない

### 国コード
- **ISO-3形式**: 3文字の国コード（例：JPN = 日本）
- **標準化**: 国際標準に準拠

### 統計情報
- **最新年**: データに含まれる最新の年
- **総数**: その年の全世界の難民総数
- **国数**: データに含まれる国の数

## 🤝 貢献

このプロジェクトは、人道支援データの可視化を通じて、難民問題への理解を深めることを目的としています。

### 改善提案
- 新しい可視化手法の追加
- データ分析の深化
- UI/UXの改善
- 多言語対応

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

データの使用については、HDX HAPIの利用規約に従ってください。

## 🔗 関連リンク

- [HDX Humanitarian Data Exchange](https://data.humdata.org/)
- [HAPI Humanitarian API](https://data.humdata.org/api)
- [UNHCR Refugee Statistics](https://www.unhcr.org/refugee-statistics/)

## 🚀 GitHub Pagesでの公開

このプロジェクトはGitHub Pagesで公開されています。

### 公開手順
1. GitHubでリポジトリを作成
2. ファイルをプッシュ
3. Settings > Pages でGitHub Pagesを有効化
4. ブランチを選択（通常は`main`または`gh-pages`）

### カスタマイズ
- `index.html`のGitHubリンクを実際のリポジトリURLに変更
- README.mdのリンクを実際のGitHub Pages URLに変更

---

**作成者**: AI Assistant  
**最終更新**: 2024年  
**バージョン**: 1.0 