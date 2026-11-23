"""第1回: 会話履歴を保って素のLLMに質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする
    uv run python -m app.ask --list-models  # 利用可能なモデルを表示する
    uv run python -m app.ask --measure 3 "LoRAとは何ですか？"
    uv run python -m app.ask --measure 3 --model gemini-3.5-flash "LoRAとは何ですか？"

ツールは使わないが、起動中は会話履歴を保って続けて質問できる。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import time

from google import genai
from google.genai import chats, errors
from google.genai import types

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def print_models(client: genai.Client) -> None:
    """APIキーで利用できるモデルを表示する。"""
    models = client.models.list()
    print("利用可能なモデル:")
    found = False
    for model in models:
        if model.name is None:
            continue
        display_name = f" ({model.display_name})" if model.display_name else ""
        print(f"- {model.name}{display_name}")
        found = True
    if not found:
        print("利用可能なモデルがありません。")


def ask(
    question: str,
    chat: chats.Chat | None = None,
    temperature: float | None = None,
) -> str:
    if chat is None:
        client = genai.Client(api_key=get_api_key())
        chat = client.chats.create(model=MODEL)

    response, elapsed = _send(question, chat, temperature)

    print(f"[応答時間] {elapsed:.2f}秒")
    usage = response.usage_metadata
    if usage is None:
        print("[トークン数] 入力: 不明, 出力: 不明")
    else:
        print(
            f"[トークン数] 入力: {usage.prompt_token_count}, "
            f"出力: {usage.candidates_token_count}"
        )

    return response.text


def _send(
    question: str,
    chat: chats.Chat,
    temperature: float | None,
) -> tuple[types.GenerateContentResponse, float]:
    started_at = time.perf_counter()
    config = (
        types.GenerateContentConfig(temperature=temperature)
        if temperature is not None
        else None
    )
    response = chat.send_message(question, config=config)
    elapsed = time.perf_counter() - started_at
    return response, elapsed


def measure(
    client: genai.Client,
    question: str,
    repetitions: int,
    temperature: float | None,
    model: str,
) -> None:
    """同じ質問を指定回数実行し、応答時間とトークン数の平均を表示する。"""
    total_elapsed = 0.0
    prompt_tokens: list[int] = []
    candidate_tokens: list[int] = []

    for iteration in range(1, repetitions + 1):
        print(f"{iteration}/{repetitions}回目実行中...", flush=True)
        # 各回を独立した会話にして、前回の質問・回答が測定値に影響しないようにする。
        chat = client.chats.create(model=model)
        response, elapsed = _send(question, chat, temperature)
        total_elapsed += elapsed
        usage = response.usage_metadata
        prompt_count = (
            usage.prompt_token_count
            if usage is not None and usage.prompt_token_count is not None
            else "不明"
        )
        candidate_count = (
            usage.candidates_token_count
            if usage is not None and usage.candidates_token_count is not None
            else "不明"
        )
        print(
            f"[{iteration}/{repetitions}回目] [応答時間] {elapsed:.2f}秒 "
            f"[トークン数] 入力: {prompt_count}, 出力: {candidate_count}"
        )
        if usage is not None:
            if usage.prompt_token_count is not None:
                prompt_tokens.append(usage.prompt_token_count)
            if usage.candidates_token_count is not None:
                candidate_tokens.append(usage.candidates_token_count)

    average_elapsed = total_elapsed / repetitions
    average_prompt = (
        f"{sum(prompt_tokens) / len(prompt_tokens):.1f}"
        if prompt_tokens
        else "不明"
    )
    average_candidates = (
        f"{sum(candidate_tokens) / len(candidate_tokens):.1f}"
        if candidate_tokens
        else "不明"
    )
    print(f"[平均応答時間] {average_elapsed:.2f}秒（{repetitions}回）")
    print(
        f"[平均トークン数] 入力: {average_prompt}, "
        f"出力: {average_candidates}"
    )


def positive_int(value: str) -> int:
    """1以上の整数を argparse で受け付ける。"""
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("1以上の整数を指定してください") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("1以上の整数を指定してください")
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser(description="会話履歴を保って素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="APIキーで利用できるモデルを表示して終了する",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        help="回答の多様性を指定する（モデルの対応範囲に従う）",
    )
    parser.add_argument(
        "--model",
        default=MODEL,
        help=f"使用するモデル（既定: {MODEL}）",
    )
    parser.add_argument(
        "--measure",
        type=positive_int,
        metavar="回数",
        help="同じ質問を指定回数だけ測定し、平均応答時間とトークン数を表示する",
    )
    args = parser.parse_args()

    client = genai.Client(api_key=get_api_key())

    try:
        if args.list_models:
            print_models(client)
            return

        print(f"[model] {args.model}")
        if args.measure is not None:
            measure(
                client,
                args.question,
                args.measure,
                args.temperature,
                args.model,
            )
            return

        chat = client.chats.create(model=args.model)
        question = args.question
        print("空行または exit で終了できます。")
        while question:
            if question.strip().lower() == "exit":
                break
            print(f"\n[質問] {question}\n")
            print(ask(question, chat, args.temperature))
            try:
                question = input("\n続けて質問してください: ").strip()
            except EOFError:
                break
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
