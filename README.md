# PairWork

**いつものAIから、得意を交換。 / Trade expertise with human-AI teams.**

人間とAIのチームが得意な仕事でポイントを獲得し、専門性の異なるチームへ仕事を依頼する、2026年のハッカソン向けプロトタイプです。

> **制作版です。** 2チームのローカルデモであり、一般向けの運用サービスではありません。募集要項・提出動画の尺は未確認です。Solana Devnetへの送信はテストSOL配布エラーにより未確認です。

![PairWorkの編集ビジュアル：二人の専門家が机で共同作業するAI生成画像](editorial-collaboration.png)

## 見る・試す

- [デモ解説動画：60秒・英語ナレーションと字幕](demo.mp4)（[WebVTT](demo.vtt) / [SRT](demo.srt)）
- [投資家向け動画：54秒・英語ナレーションと字幕](investor.mp4)（[WebVTT](investor.vtt) / [SRT](investor.srt)）
- [概要PDF：日本語1ページ](overview-ja.pdf)
- [English overview](overview-en.md)
- [実装状況と検証記録](STATUS.md)
- [AI生成画像の制作プロンプト](IMAGE_PROMPTS.md)
- [完全ソース一式（スキルとテストを含む）](pairwork-source.zip)

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

- CodexやClaude Codeなど、自分が使い慣れたAIを得意分野の仕事に生かし、貢献に応じてポイントを得る。そのポイントで苦手な仕事を専門チームに依頼する。
- 「スキル導入 → 接続許可 → 受注・納品 → 人間による確認・承認 → ポイント獲得 → 次の依頼」という流れを想定。現行のスキル接続はローカルデモで、公開アカウント連携は未実装。
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

将来は、当事者の確認と結び付いた完了履歴を検証可能な証跡として積み上げ、翻訳・コードレビューなど分野別の専門性の評判に活用する構想です。得意分野の判定とポイント配分の候補データは、PairWork内の作業ログ、AI評価、依頼者評価、完了までの速度、分野別の経験量です。ポイント配分ルールの版と適用結果を公開し、第三者が配分過程を監査できるようにすることも検討します。さらに、PairWork内の実績に基づく専門家証明書を発行し、Solanaエコシステムの他サービスでも提示できる設計を目指します。証明書は公的資格を意味しません。

チェーンだけで得意分野の発見、仕事の品質評価、公平なポイント配分が自動的に保証されるわけではありません。評判の算定、評価・配分ロジックの公開と監査、証明書の発行、他サービスとの連携は未実装です。候補データの重み付け、評価の信頼性、不正対策も未設計・未検証です。現時点のSolana機能は完了ハッシュのDevnet Memo送信コードに限られ、確認済み送信はありません。

## 収益モデル（仮説）

AIツールに継続課金する利用者が専門家の助けにも対価を払うかを検証します。これは市場規模の推計ではありません。仕事交換そのものは貢献で得たポイントで行い、運営はチーム指名・優先マッチングを含むPro月額で収益を得る構想です。将来は企業内ネットワーク契約も検討します。ポイント自体は売りません。

需要の背景として、[OpenAIは2026年6月にCodexの週間アクティブ利用者が500万人超](https://openai.com/index/codex-for-knowledge-work/)と発表し、[Anthropicは2026年2月にClaude Codeの法人契約数が年初から4倍](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation)と発表しました。これは各社が公表した利用動向であり、PairWorkの獲得可能市場や有料会員数を示しません。

[ChatGPT Pro $100](https://help.openai.com/en/articles/9793128-what-is-chatgpt-pro/) と [Claude Max 5x（月額$100）](https://support.claude.com/en/articles/11049741-what-is-the-max-plan?subjects=product) にも利用枠があり、[Codexの上限](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan) や [Claude Maxの週次上限](https://support.claude.com/en/articles/11049741-what-is-the-max-plan?subjects=product) に達して仕事が残る場面が考えられます。PairWorkでは、空き時間に得意分野で他チームを助けてポイントを貯め、忙しい時に専門チームへ依頼する流れを想定します。各チームは自分のAI契約を使い、アカウントや利用枠を共有しません。

Proの月額$10は、月額$100のAIプランに対する追加費用の10%という価格仮説です。専門家の助けで作業効率が**仮に10%以上改善**し、限られた時間・利用枠の中でも苦手な仕事を納期に向けて進められるなら、チーム指名・優先マッチングに**月額$10**を払う動機になり得ます。効率改善率も支払意向も未検証で、金銭的な元が取れることを示すものではありません。

例として、Pro月額$10 × 有料会員1,000人 = 月次売上$10,000（費用控除前）です。価格・会員数とも仮定であり、実績・利益・市場規模を表す数字ではありません。運営インフラ、サポート、紛争対応、集客、決済、オンチェーン記録の費用を控除する必要があります。各チームは自分のAI利用費を負担する想定です。継続率・獲得費用・有料化意向は未検証です。

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
