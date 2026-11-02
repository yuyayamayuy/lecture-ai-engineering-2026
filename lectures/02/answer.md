# 第2回 解答
 
## 演習

- 使ったモデル・設定：
  * base_model=Qwen/Qwen3.5-0.8B
  * revision=2fc06364715b967f1860aea9cf38778875588b17
  * seed=42
  * num_train_epochs=20
  * lora_r=16
- 自分で学習を実行したか（`executed_training_myself`）：はい（実行できた範囲：　）
- 学習前：`format_rate` =　0.09523809523809523 / `content_rate` =　0.0
- 学習後：`format_rate` =　1.0 / `content_rate` =　0.9047619047619048
- 退行した質問：
  * なし
- 学習後に残った失敗と、その型（根拠なしの質問に断定した / 根拠ありの質問に確認要求で逃げた / 形式の崩れ）：
  * 失敗した質問：成績はいつでますか？
  * 根拠なしの質問に断定した
- 知識を問う質問（セクション 6）の結果（学習前の分類 → 学習後の分類）と気づいたこと：
  * FAQにない質問に対しても断定で言い切っている回答がある
- 学習で変わったこと・変わらなかったこと：
  * 形式と内容が正しく出力できるようになった質問がある。

## 宿題
### 宿題①
- 取り組んだレベル：基礎
- 変えた設定やデータ：epochs 20 → 60 に変更
- 結果（比較表や数字）：
  * 退行: 0 件
    |  | format_rate | content_rate | both_rate | seconds |
    | ---- | ---- | ---- | ---- | ---- |
    | before | 0.095238 | 0.000000 | 0.000000 | 43.4 |
    | after | 1.000000 | 0.904762 | 0.904762 | 44.1 |

### 宿題②
- 取り組んだレベル：基礎
- 変えた設定やデータ：lora_rを16 → 2 に変更
- 結果（比較表や数字）：
  * 退行: 0 件
    |  | format_rate | content_rate | both_rate | seconds |
    | ---- | ---- | ---- | ---- | ---- |
    | before | 0.095238 | 0.000000 | 0.000000 | 43.6 |
    | after | 1.000000 | 0.857143 | 0.857143 | 43.4 |

### 宿題③
- 取り組んだレベル：実装
- 変えた設定やデータ：
    ```
    FAQ = {
        "date": "無料開放日は 2026 年 11 月 3 日です。",
        "occasion": "2026 年 11 月 3 日は文化の日です。",
        "facilities": "無料開放される施設は、東京国立博物館、国立西洋美術館、栃木県立美術館、国立工芸館、国立国際美術館の 5 施設です。",
        "tokyo": "東京都内の対象施設は、東京国立博物館と国立西洋美術館です。",
        "other_regions": "東京都以外の対象施設は、栃木県立美術館（栃木県）、国立工芸館（石川県）、国立国際美術館（大阪府）です。",
    }

    GROUNDED = {
        "date": (
            [
                "無料開放日はいつですか",
                "美術館や博物館が無料になる日はいつですか",
                "何月何日に無料開放されますか",
                "無料で入館できる日を教えてください",
            ],
            ["2026 年 11 月 3 日"]
        ),

        "occasion": (
            [
                "2026 年 11 月 3 日は何の日ですか",
                "無料開放日は何の祝日ですか",
                "今回の無料開放は何の日に実施されますか",
                "11 月 3 日の祝日名を教えてください",
            ],
            ["文化の日"]
        ),

        "facilities": (
            [
                "無料開放される施設を教えてください",
                "対象となる美術館や博物館はどこですか",
                "今回無料になる施設をすべて教えてください",
                "無料開放の対象施設は何施設ありますか",
            ],
            ["東京国立博物館", "国立西洋美術館", "栃木県立美術館",
            "国立工芸館", "国立国際美術館"]
        ),

        "tokyo": (
            [
                "東京都内で無料になる施設はどこですか",
                "東京の対象施設を教えてください",
                "東京で無料開放される博物館や美術館はありますか",
                "東京都にある対象施設をすべて教えてください",
            ],
            ["東京国立博物館", "国立西洋美術館"]
        ),

        "other_regions": (
            [
                "東京以外で無料になる施設はどこですか",
                "地方の対象施設を教えてください",
                "栃木県や石川県、大阪府で無料になる施設はありますか",
                "東京以外の3施設について教えてください",
            ],
            ["栃木県立美術館", "国立工芸館", "国立国際美術館"]
        ),
    }

    UNGROUNDED = [
        "各施設の開館時間は何時から何時までですか",
        "無料開放には事前予約が必要ですか",
        "特別展も無料で鑑賞できますか",
        "無料開放の日に駐車場は利用できますか",
        "子どもも無料で入館できますか",
        "各施設ではどのような展示が開催されていますか",
        "無料開放の日は混雑しますか",
        "入館する際に身分証明書は必要ですか",
    ]
    TEST_EXTRA_GROUNDED = {
        "date": [
            "2026 年に無料で美術館や博物館を見学できる日は何月何日ですか",
            "文化の日の無料開放はいつ実施されますか",
        ],

        "occasion": [
            "11 月 3 日はどのような祝日ですか",
            "今回の施設無料開放が行われる記念日は何ですか",
        ],

        "facilities": [
            "今回の無料開放の対象となる5つの施設名を挙げてください",
            "無料で見学できる博物館と美術館の一覧を教えてください",
        ],

        "tokyo": [
            "東京都にある無料開放対象の2施設は何ですか",
            "東京で文化の日に無料で入れる施設名を教えてください",
        ],

        "other_regions": [
            "栃木、石川、大阪で無料開放される施設をそれぞれ教えてください",
            "東京以外にある無料開放対象の美術館を3つ挙げてください",
        ],
    }

    TEST_EXTRA_UNGROUNDED = [
        "各施設の最終入館時刻は何時ですか",
        "無料開放の日に音声ガイドは無料で借りられますか",
        "各施設の最寄り駅と徒歩での所要時間を教えてください",
        "無料開放の日に団体で訪問する場合は予約が必要ですか",
    ]
    ```

- 結果（比較表や数字）：
  * 退行: 0 件
    |  | format_rate | content_rate | both_rate | seconds |
    | ---- | ---- | ---- | ---- | ---- |
    | before | 0.142857 | 0.095238 | 0.095238 | 43.6 |
    | after | 1.000000 | 1.000000 | 1.000000 | 43.4 |

    | No. | 質問                               | 正解の needs_review | 学習前の出力 | 学習前 形式/内容                                                                                                                                                       | 学習後の出力 | 学習後 形式/内容                                                                                        |
    | --- | -------------------------------- | ---------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------ |
    | 0   | 無料で入館できる日を教えてください                | False            | ×/×    | `{"answer": "2026 年 11 月 3 日"}`                                                                                                                                 | ○/○    | `{"answer": "無料開放日は 2026 年 11 月 3 日です。", "needs_review": false}`                                 |
    | 1   | 2026 年に無料で美術館や博物館を見学できる日は何月何日ですか | False            | ×/×    | `{"answer": "2026 年 11 月 3 日"}`                                                                                                                                 | ○/○    | `{"answer": "無料開放日は 2026 年 11 月 3 日です。", "needs_review": false}`                                 |
    | 2   | 文化の日の無料開放はいつ実施されますか              | False            | ×/×    | `{"answer": "2026 年 11 月 3 日"}`                                                                                                                                 | ○/○    | `{"answer": "無料開放日は 2026 年 11 月 3 日です。", "needs_review": false}`                                 |
    | 3   | 11 月 3 日の祝日名を教えてください             | False            | ×/×    | `{"answer": "文化の日"}`                                                                                                                                            | ○/○    | `{"answer": "2026 年 11 月 3 日は文化の日です。", "needs_review": false}`                                   |
    | 4   | 11 月 3 日はどのような祝日ですか              | False            | ○/○    | `{"answer": "文化の日", "needs_review": false}`                                                                                                                     | ○/○    | `{"answer": "2026 年 11 月 3 日は文化の日です。", "needs_review": false}`                                   |
    | 5   | 今回の施設無料開放が行われる記念日は何ですか           | False            | ×/×    | `{"answer": "2026 年 11 月 3 日"}`                                                                                                                                 | ○/○    | `{"answer": "文化の日です。", "needs_review": false}`                                                   |
    | 6   | 無料開放の対象施設は何施設ありますか               | False            | ○/×    | `{"answer": "5", "needs_review": false}`                                                                                                                        | ○/○    | `{"answer": "無料開放される施設は、東京国立博物館、国立西洋美術館、栃木県立美術館、国立工芸館、国立国際美術館の 5 施設です。", "needs_review": false}` |
    | 7   | 今回の無料開放の対象となる5つの施設名を挙げてください      | False            | ×/×    | `{"answer": "東京国立博物館、国立西洋美術館、栃木県立美術館、国立工芸館、国立国際美術館"}`                                                                                                           | ○/○    | `{"answer": "無料開放される施設は、東京国立博物館、国立西洋美術館、栃木県立美術館、国立工芸館、国立国際美術館の 5 施設です。", "needs_review": false}` |
    | 8   | 無料で見学できる博物館と美術館の一覧を教えてください       | False            | ×/×    | `{"answer": "東京国立博物館、国立西洋美術館、栃木県立美術館、国立工芸館、国立国際美術館"}`                                                                                                           | ○/○    | `{"answer": "無料開放される施設は、東京国立博物館、国立西洋美術館、栃木県立美術館、国立工芸館、国立国際美術館の 5 施設です。", "needs_review": false}` |
    | 9   | 東京都にある対象施設をすべて教えてください            | False            | ×/×    | `{"answer": "東京国立博物館、国立西洋美術館"}`                                                                                                                                 | ○/○    | `{"answer": "東京都内の対象施設は、東京国立博物館と国立西洋美術館です。", "needs_review": false}`                             |
    | 10  | 東京都にある無料開放対象の2施設は何ですか            | False            | ×/×    | `{"answer": "東京国立博物館、国立西洋美術館"}`                                                                                                                                 | ○/○    | `{"answer": "東京都内の対象施設は、東京国立博物館と国立西洋美術館です。", "needs_review": false}`                             |
    | 11  | 東京で文化の日に無料で入れる施設名を教えてください        | False            | ×/×    | `{"answer": "東京国立博物館、国立西洋美術館"}`                                                                                                                                 | ○/○    | `{"answer": "東京都内の対象施設は、東京国立博物館と国立西洋美術館です。", "needs_review": false}`                             |
    | 12  | 東京以外の3施設について教えてください              | False            | ×/×    | `{"answer": "栃木県立美術館、国立工芸館、国立国際美術館"}`                                                                                                                           | ○/○    | `{"answer": "東京都以外の対象施設は、栃木県立美術館（栃木県）、国立工芸館（石川県）、国立国際美術館（大阪府）です。", "needs_review": false}`       |
    | 13  | 栃木、石川、大阪で無料開放される施設をそれぞれ教えてください   | False            | ×/×    | `{"answer": "栃木県立美術館、石川県国立工芸館、大阪府国立国際美術館"}`                                                                                                                     | ○/○    | `{"answer": "東京都以外の対象施設は、栃木県立美術館（栃木県）、国立工芸館（石川県）、国立国際美術館（大阪府）です。", "needs_review": false}`       |
    | 14  | 東京以外にある無料開放対象の美術館を3つ挙げてください      | False            | ×/×    | `{"answer": "栃木県立美術館、国立工芸館、国立国際美術館"}`                                                                                                                           | ○/○    | `{"answer": "東京都以外の対象施設は、栃木県立美術館（栃木県）、国立工芸館（石川県）、国立国際美術館（大阪府）です。", "needs_review": false}`       |
    | 15  | 無料開放の日に駐車場は利用できますか               | True             | ×/×    | `{"answer": "確認が必要"}`                                                                                                                                           | ○/○    | `{"answer": "この FAQ には記載がありません。運営に確認が必要です。", "needs_review": true}`                              |
    | 16  | 入館する際に身分証明書は必要ですか                | True             | ○/○    | `{"answer": "確認が必要", "needs_review": true}`                                                                                                                     | ○/○    | `{"answer": "この FAQ には記載がありません。運営に確認が必要です。", "needs_review": true}`                              |
    | 17  | 各施設の最終入館時刻は何時ですか                 | True             | ×/×    | `{"answer": "確認が必要"}`                                                                                                                                           | ○/○    | `{"answer": "この FAQ には記載がありません。運営に確認が必要です。", "needs_review": true}`                              |
    | 18  | 無料開放の日に音声ガイドは無料で借りられますか          | True             | ×/×    | `{"answer": "無料開放の日に音声ガイドは無料で借りられます。"}`                                                                                                                         | ○/○    | `{"answer": "この FAQ には記載がありません。運営に確認が必要です。", "needs_review": true}`                              |
    | 19  | 各施設の最寄り駅と徒歩での所要時間を教えてください        | True             | ×/×    | `{"answer": "無料開放日は 2026 年 11 月 3 日です。2026 年 11 月 3 日は文化の日です。無料開放される施設は、東京国立博物館、国立西洋美術館、栃木県立美術館、国立工芸館、国立国際美術館の 5 施設です。東京都内の対象施設は、東京国立博物館と国立西洋美術館です。東京都以外の..."}` | ○/○    | `{"answer": "この FAQ には記載がありません。運営に確認が必要です。", "needs_review": true}`                              |
    | 20  | 無料開放の日に団体で訪問する場合は予約が必要ですか        | True             | ×/×    | `{"answer": "確認が必要"}`                                                                                                                                           | ○/○    | `{"answer": "この FAQ には記載がありません。運営に確認が必要です。", "needs_review": true}`                              |



### 宿題④
- 取り組んだレベル：発展
- 変えた設定やデータ：
  * glossary_sft.jsonlで学習するコードは以下の通り。(Gemini 3.1 Proを使用)
    ```
    from datasets import load_dataset
    from peft import LoraConfig
    from trl import SFTTrainer, SFTConfig
    import torch
    from transformers import AutoModelForCausalLM

    # 1. 前回の学習状態をリセットするため、基盤モデルを再読み込み
    print("基盤モデルを再読み込みしています...")
    clean_model = AutoModelForCausalLM.from_pretrained(
        CONFIG["base_model"], 
        revision=CONFIG["revision"], 
        dtype=torch.float32
    ).to(DEVICE)
    clean_model.config.use_cache = False

    # 2. glossary_sft.jsonl の読み込み
    # messages形式のJSONLデータを読み込みます。trlのSFTTrainerは 'messages' カラムを自動的に認識します。
    data_path = "/content/qlora_lab/glossary_sft.jsonl"
    dataset = load_dataset("json", data_files=data_path, split="train")

    # 学習データと検証データに分割 (例として1割を検証用に使用)
    dataset = dataset.train_test_split(test_size=0.1, seed=CONFIG["seed"])
    train_ds_gloss = dataset["train"]
    valid_ds_gloss = dataset["test"]
    print(f"学習データ: {len(train_ds_gloss)}件, 検証データ: {len(valid_ds_gloss)}件")

    # 3. LoRA および SFTTrainer の設定
    lora_config = LoraConfig(
        r=CONFIG["lora_r"], 
        lora_alpha=CONFIG["lora_alpha"], 
        lora_dropout=0.05, 
        bias="none", 
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    )

    sft_config = SFTConfig(
        output_dir=str(WORK / "glossary_ckpt"),
        num_train_epochs=10,  # データ量に応じて調整してください
        per_device_train_batch_size=4,
        gradient_accumulation_steps=2,
        learning_rate=CONFIG["lr"],
        lr_scheduler_type="cosine",
        logging_steps=5,
        save_steps=20,
        max_length=CONFIG["max_seq_len"],
        packing=False,
        report_to="none",
        seed=CONFIG["seed"]
    )

    trainer_gloss = SFTTrainer(
        model=clean_model,
        args=sft_config,
        train_dataset=train_ds_gloss,
        eval_dataset=valid_ds_gloss,
        peft_config=lora_config,
        processing_class=tok
    )

    # 4. 学習の実行
    print("学習を開始します...")
    trainer_gloss.train()

    # 5. アダプタの保存
    GLOSSARY_ADAPTER_DIR = WORK / "glossary_adapter"
    trainer_gloss.model.save_pretrained(GLOSSARY_ADAPTER_DIR)
    print(f"\n学習完了。新しいアダプタを {GLOSSARY_ADAPTER_DIR} に保存しました。")

    # 評価用にキャッシュを有効化しておく
    tuned_gloss = trainer_gloss.model
    tuned_gloss.config.use_cache = True
    _ = tuned_gloss.eval()
    ```
    * 評価コードは以下の通り。
    ```
    import contextlib
    import pandas as pd

    # 1. 評価用の質問と正解の定義（事前に定義した変数から抽出）
    GLOSSARY_EVAL_DATA = [
        {
            "type": "用語集にある語",
            "question": GROUNDED["date"][0][0], 
            "expected_keyword": GROUNDED["date"][1][0]
        },
        {
            "type": "言い回しを変えた質問",
            "question": TEST_EXTRA_GROUNDED["date"][0], 
            "expected_keyword": GROUNDED["date"][1][0]
        },
        {
            "type": "用語集にない語",
            "question": UNGROUNDED[0], 
            "expected_keyword": "確認が必要"
        }
    ]

    # プロンプト構築関数（実際の学習データのsystemプロンプトに合わせて調整）
    def build_glossary_prompt(question):
        system_msg = "あなたは講座 FAQ の回答係です。与えられた FAQ だけを根拠に、必ず JSON 1 行で答えてください。形式: {\"answer\": 文字列, \"needs_review\": 真偽値}。FAQ に記載が無いことは answer に『確認が必要』と書き、needs_review を true にします。"
        user_msg = f"FAQ:\n{FAQ_TEXT}\n\n質問: {question}"
        return [{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}]

    # 評価関数
    def evaluate_glossary(model, is_before=False):
        results = []
        # 学習前（before）の評価時は adapter を一時的に無効化する
        context = model.disable_adapter() if is_before else contextlib.nullcontext()
        with context:
            for item in GLOSSARY_EVAL_DATA:
                prompt = tok.apply_chat_template(
                    build_glossary_prompt(item["question"]), 
                    tokenize=False, 
                    add_generation_prompt=True, 
                    enable_thinking=False
                )
                inputs = tok(prompt, return_tensors="pt").to(model.device)
                with torch.no_grad():
                    out = model.generate(
                        **inputs, 
                        max_new_tokens=64, 
                        pad_token_id=tok.pad_token_id, 
                        **CONFIG["gen"]
                    )
                ans = tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
                results.append({
                    "質問タイプ": item["type"],
                    "質問": item["question"],
                    "期待されるキーワード": item["expected_keyword"],
                    "モデルの出力": ans
                })
        return results

    # 2. 学習前の評価
    print("=== 学習前 (Base Model) の出力 ===")
    before_gloss_res = evaluate_glossary(tuned_gloss, is_before=True)
    display(pd.DataFrame(before_gloss_res))

    # 3. 学習後の評価
    print("\n=== 学習後 (LoRA Tuned Model) の出力 ===")
    after_gloss_res = evaluate_glossary(tuned_gloss, is_before=False)
    display(pd.DataFrame(after_gloss_res))
    ```

- 結果（比較表や数字）：
  * 学習前 (Base Model) の出力

    | No. | 質問タイプ      | 質問                               | 期待されるキーワード      | モデルの出力                                                                                               |
    | --- | ---------- | -------------------------------- | --------------- | ---------------------------------------------------------------------------------------------------- |
    | 0   | 用語集にある語    | 無料開放日はいつですか                      | 2026 年 11 月 3 日 | `{"answer": "2026 年 11 月 3 日"}`                                                                      |
    | 1   | 言い回しを変えた質問 | 2026 年に無料で美術館や博物館を見学できる日は何月何日ですか | 2026 年 11 月 3 日 | `{"answer": "2026 年 11 月 3 日"}`                                                                      |
    | 2   | 用語集にない語    | 各施設の開館時間は何時から何時までですか             | 確認が必要           | `{"answer": "無料開放日は 2026 年 11 月 3 日です。2026 年 11 月 3 日は文化の日です。無料開放される施設は、東京国立博物館、国立西洋美術館、栃木県立美術館、...` |

  * 学習後 (LoRA Tuned Model) の出力

    | No. | 質問タイプ      | 質問                               | 期待されるキーワード      | モデルの出力                                                                                  |
    | --- | ---------- | -------------------------------- | --------------- | --------------------------------------------------------------------------------------- |
    | 0   | 用語集にある語    | 無料開放日はいつですか                      | 2026 年 11 月 3 日 | `{"answer": "2026 年 11 月 3 日"}`                                                         |
    | 1   | 言い回しを変えた質問 | 2026 年に無料で美術館や博物館を見学できる日は何月何日ですか | 2026 年 11 月 3 日 | `{"answer": "2026 年 11 月 3 日"}`                                                         |
    | 2   | 用語集にない語    | 各施設の開館時間は何時から何時までですか             | 確認が必要           | `{"answer": "東京国立博物館：9:00～14:00、17:00～19:30。国立西洋美術館：9:00～14:00、17:00～19:30。栃木県立美術館：...` |

- ファインチューニングが向く場面・向かない場面についての考察：
  * 各施設の開放時間に関する質問について、学習前は「確認が必要」かつ開放時間は回答に含めていなかった。しかし、学習後は「確認が必要」としながらも開放時間を含めていた。
  * 講義では、FTすることによって人に迎合する傾向のある回答を出すことに触れられていたが、その傾向がこの実験によって確認されたと思う。開館時間についてのデータは与えていないのに、もっともらしい時間を出力した。
  * この実験によりFT後の評価を注意深く行う必要があることが分かった。