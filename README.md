# PairWork

**いつものAIから、得意を交換。 / Trade expertise with human-AI teams.**

人間とAIのチームが得意な仕事でポイントを獲得し、専門性の異なるチームへ仕事を依頼する、2026年のハッカソン向けプロトタイプです。

> **制作版です。** 2チームのローカルデモであり、一般向けの運用サービスではありません。募集要項・提出動画の尺は未確認です。Solana Devnetへの送信はテストSOL配布エラーにより未確認です。

![PairWorkの編集ビジュアル：二人の専門家が机で共同作業するAI生成画像](editorial-collaboration.png)

## 見る・試す

**[ブラウザデモ](https://yosimin265.github.io/pairwork-exchange/) · [動画と資料](https://yosimin265.github.io/pairwork-exchange/materials.html) · [完全なソース一式をダウンロード](pairwork-source.zip)**

ローカル版の起動・スキル導入・テストには、`pairwork-source.zip` を解凍して中の `pairwork` フォルダを使ってください。Webアップロード版では資料をルートに配置し、完全なディレクトリ構成をZIPに同梱しています。

- [デモ解説動画：60秒・英語ナレーションと字幕](demo.mp4)（[WebVTT](demo.vtt) / [SRT](demo.srt)）
- [投資家向け動画：60秒・英語ナレーションと字幕](investor.mp4)（[WebVTT](investor.vtt) / [SRT](investor.srt)）
- [概要PDF：日本語1ページ](overview-ja.pdf)
- [English overview](overview-en.md)
- [実装状況と検証記録](STATUS.md)
- [AI生成画像の制作プロンプト](IMAGE_PROMPTS.md)

サイトは写真と紙面のようなレイアウトを用いた編集デザインです。サイトと動画で使う2枚の人物写真はAI生成画像であり、実在の利用者や実際の仕事を撮影したものではありません。動画は実装画面のキャプチャと説明スライドを編集し、英語の合成音声ナレーションと字幕を付けたものです。サンプル翻訳を使用しており、AI製品が自動で作業する録画ではありません。

### 最も簡単な体験

[公開ブラウザデモ](https://yosimin265.github.io/pairwork-exchange/)で体験できます。ローカルで開く場合は、`index.html`、`editorial-collaboration.png`、`editorial-review.png` を同じフォルダに置いてください。GitHubのファイル表示画面では実行されません。データはブラウザ内に保存され、初期状態は各チーム300pt、翻訳依頼50ptです。

### スキルとつながるローカル版

Python 3.10以上が必要です。コア機能に追加パッケージは不要です。

```sh
python3 server.py
```

ブラウザで `http://127.0.0.1:8765` を開きます。macOSでは `sh start.command` をターミナルから実行することもできます。

1. Mio + Claude Code を選んで翻訳依頼を受注。
2. 納品画面で「サンプルを入力」し、確認して納品。
3. Kai + Codex に切り替え、成果物を確認して承認。
4. Kaiは250pt、Mioは350ptになることを確認。
5. Mioに切り替え、50ptでPythonのコードレビューを投稿。
6. 完了記録からSHA-256を確認。ハッシュだけでオンチェーン記録済みとはなりません。

### 専用スキルを導入

解凍したソースのルートから、利用するプロジェクトに導入します。既存スキルは上書きしません。

```sh
python3 install_skill.py --target codex --project /absolute/path/to/your/project
python3 install_skill.py --target claude --project /absolute/path/to/your/project
```

対象プロジェクトをCodexまたはClaude Codeで開き、「PairWorkに接続して」と依頼します。スキルは `scripts/client.py connect` を実行し、ブラウザを開きます。チームを選択し「このチームで接続を許可」を押すと接続完了です。

これは**公開サイトへの通常ログインではなく、ローカルデモ接続**です。両製品内のスキル自動認識・実機操作は未確認です。共通クライアントの接続、残高取得、投稿・受注・納品・承認のAPIは検証しています。今回の版は直接APIを呼ぶスキルであり、MCPサーバーは含みません。

セッションはスキル内 `.session.json` に保存されます。公開しないでください。サーバー再起動または8時間後は再接続が必要です。2人が別PCから使う本番ネットワークではありません。

## なぜポイントか

- ステーブルコイン決済型の方式に対し、貢献で獲得したポイントで仕事を交換。
- ポイントの販売・換金・自由送金なし。依頼ごとの暗号資産購入や送金操作なし。
- AI単体ではなく、人間が確認するチーム同士の協力。
- 各チームが自分のAIを道具として使う。アカウントや利用枠の転貸を行わない。

特定競合の機能比較や「規約・法的リスクがない」という主張はしていません。時間や利用枠の節約効果は未計測です。

## Solanaの役割

完了レコードのSHA-256を、運営のDevnet署名者がMemoに記録する設計です。成果物や個人情報を送る設計ではありません。ポイント台帳はSQLite内です。

```sh
python3 -m pip install pynacl
python3 solana_receipt.py --hash <64文字のSHA-256> --out docs/devnet-receipt.json
```

初回は専用のテスト鍵を `.pairwork/` に作り、Devnetの無料テストSOLを要求します。**Mainnetには対応せず、実資金は扱いません。** faucetが利用できない場合は送信できません。今回の検証ではfaucetがエラーとHTTP 429を返し、確認済みトランザクションは作れていません。成功時のみJSONに署名と確認状態が出ます。

ハッシュが示せるのは対応データの一致であり、仕事の品質・実在・双方の合意を独立に保証するものではありません。現状は運営による署名で、当事者双方の署名は未実装です。

## 収益モデル（仮説）

Pro月額でチーム指名・優先マッチングを提供し、将来は企業内ネットワーク契約を検討します。ポイント自体は売りません。

動画内の「月額1,500円 × 1,000人 = 月商150万円」は価格・会員数とも仮定の試算です。実績・利益・市場規模を表す数字ではありません。運営インフラ、サポート、集客、決済、オンチェーン記録の費用を控除する必要があります。各チームが自分のAI利用費を負担する想定です。

## 技術構成

- フロント：HTML/CSS/JavaScript、ビルド不要、ブラウザ体験版はlocalStorage
- ローカルAPI：Python標準ライブラリ、SQLiteのトランザクションでポイント移動
- スキル：共通SKILL.mdとPythonクライアント、ブラウザによる接続許可
- Solana：Ed25519署名したMemo（Devnetのみ、送信未確認）

```text
人間 + AI → 専用スキル → localhost API → SQLite台帳
                           ↑
                     ブラウザで接続許可・確認
完了レコード → SHA-256 → Devnet Memo（任意・別スクリプト）
```

ログインはデモの役割切り替えです。localhostのみで動かし、インターネットにサーバーをそのまま公開しないでください。Skill内の指示はOSレベルのサンドボックスを実装するものではありません。

## テスト

```sh
python3 -m unittest discover -s tests -v
```

仕事交換の往復、残高予約、修正依頼、誤った承認、並行承認による二重払い、成果物ハッシュを検証します。

## 去年の応募との関係

参考：[2025 CONPRO AI Chain / SOUL CHAIN](https://github.com/yosimin265/yosi1)。昨年の「目的→仕組み→将来像」という説明構成を参考にしました。今年は別企画・別ソースとして作成し、操作できるデモ、再現手順、実装範囲、動画2本を追加しています。去年の資料や知財主張は転載していません。

## References

- [Codex / skills](https://developers.openai.com/codex/skills/)
- [Claude Code / skills](https://code.claude.com/docs/en/skills)
- [Solana transactions](https://solana.com/docs/core/transactions)

Codex、Claude Code、Solanaはそれぞれの提供者の製品・ネットワークです。本プロジェクトは独立した試作です。
