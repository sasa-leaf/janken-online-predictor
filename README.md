# じゃんけん LSTMオンライン学習 Webアプリ

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sasa-leaf/janken-online-predictor/blob/master/main.ipynb)

このリポジトリは、FastAPI・TensorFlow・ngrokを用いたじゃんけんオンライン学習Webアプリです。  
ユーザーが過去に出した手をもとに、次にユーザーが出す手をLSTMで予測します。


## 主な機能

- **5種じゃんけんの予測**: 過去の対戦履歴に基づくユーザーの次の手の予測（LSTMモデルを使用）
- **オンライン学習**: 対戦ごとにモデルをリアルタイムで学習し、AIが徐々に強くなる機能
- **予測の可視化**: AIが予測した手の確率分布をWeb上で表示
- **Webシステム**: FastAPIによるAPI・Webサーバー構築と、ngrokによる一時的な公開URL生成
- **対戦履歴管理**: 勝率計算、ルール・ヒントのモーダル表示機能

## ngrokの登録・トークン取得方法

このプロジェクトを利用するには、ngrokの認証トークンが必要です。  
まだngrokアカウントを作成していない方は、以下の手順で登録・トークン取得を行ってください。

1. [ngrok公式サイト](https://ngrok.com/) にアクセスし、アカウントを作成します。
2. ログイン後、ダッシュボードの「Your Authtoken」欄から認証トークンをコピーできます。
3. このトークンは、ngrokを使った公開URL生成の際に必要となります。

## ローカルでの実行方法

1. **依存パッケージのインストール**

   ```sh
   poetry install
   ```

2. **環境変数の設定**

   `.env` ファイルを作成し、以下のように設定してください（プロジェクトルートに配置）

   ```
   NGROK_TOKEN=あなたのngrokトークン
   ```

   - `NGROK_TOKEN` : ngrokの認証トークン

3. **サーバー起動**

   ```sh
   poetry run python main.py
   ```

   起動後、ngrokの公開URLが表示されます。

## Google Colabでの実行方法

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sasa-leaf/janken-online-predictor/blob/master/main.ipynb)

1. 上記のリンク先に移動する。
2. 一番上のセルの`TOKEN`に，あなたのngrokトークンを文字列として貼り付けて，全セルを実行する。


## 使い方

- ブラウザで公開URLにアクセスする。
- 画面の指示に従ってじゃんけんの手を選択していくと，AIの予測結果などが表示されます。

## ディレクトリ構成

- `main.py` : サーバー起動・API定義
- `app/model_utils.py` : モデル構築・学習
- `app/visualization.py` : 予測分布画像生成
- `templates/index.html` : Webフロントエンド
- `static/` : 静的ファイル（ロゴ等）

## 開発・テスト

- コード整形: `make fmt`
- Lint: `make lint`
- テスト: `make test`

## ライセンス

MIT
