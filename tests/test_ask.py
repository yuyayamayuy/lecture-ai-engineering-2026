"""素のLLMに質問するCLIのテスト（APIは呼び出さない）。"""

from types import SimpleNamespace

import pytest

from app import ask as ask_module


def test_main_reuses_chat_for_follow_up_questions(monkeypatch, capsys):
    questions = []

    class FakeChat:
        def send_message(self, question, config=None):
            assert config is None
            questions.append(question)
            return SimpleNamespace(
                text=f"回答: {question}",
                usage_metadata=None,
            )

    chat = FakeChat()

    def create_chat(*, model):
        assert model == ask_module.MODEL
        return chat

    client = SimpleNamespace(
        chats=SimpleNamespace(create=create_chat),
    )

    def create_client(*, api_key):
        assert api_key == "test-key"
        return client

    monkeypatch.setattr(ask_module.genai, "Client", create_client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr("sys.argv", ["app.ask", "最初の質問"])
    answers = iter(["続けて質問", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    ask_module.main()

    output = capsys.readouterr().out
    assert questions == ["最初の質問", "続けて質問"]
    assert "回答: 最初の質問" in output
    assert "回答: 続けて質問" in output


def test_main_passes_temperature_to_every_message(monkeypatch):
    configs = []

    class FakeChat:
        def send_message(self, question, config=None):
            configs.append(config)
            return SimpleNamespace(text=f"回答: {question}", usage_metadata=None)

    chat = FakeChat()

    def create_chat(*, model):
        assert model == ask_module.MODEL
        return chat

    client = SimpleNamespace(chats=SimpleNamespace(create=create_chat))

    def create_client(*, api_key):
        assert api_key == "test-key"
        return client

    monkeypatch.setattr(ask_module.genai, "Client", create_client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(
        "sys.argv",
        ["app.ask", "--temperature", "0.7", "最初の質問"],
    )
    answers = iter(["続けて質問", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    ask_module.main()

    assert [config.temperature for config in configs] == [0.7, 0.7]


def test_main_lists_available_models_without_starting_chat(monkeypatch, capsys):
    class FakeModels:
        def list(self):
            return [
                SimpleNamespace(name="models/model-a", display_name="Model A"),
                SimpleNamespace(name="models/model-b", display_name=None),
            ]

    def unexpected_chat_create(*, model):
        assert model == ask_module.MODEL
        raise AssertionError("モデル一覧表示でチャットを開始してはいけない")

    client = SimpleNamespace(
        models=FakeModels(),
        chats=SimpleNamespace(create=unexpected_chat_create),
    )

    def create_client(*, api_key):
        assert api_key == "test-key"
        return client

    monkeypatch.setattr(ask_module.genai, "Client", create_client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr("sys.argv", ["app.ask", "--list-models"])

    ask_module.main()

    output = capsys.readouterr().out
    assert "models/model-a (Model A)" in output
    assert "models/model-b" in output


def test_measure_runs_requested_count_and_prints_averages_without_responses(
    monkeypatch,
    capsys,
):
    sent_questions = []
    created_chats = []
    responses = iter(
        [
            SimpleNamespace(
                text="この回答は表示しない",
                usage_metadata=SimpleNamespace(
                    prompt_token_count=10,
                    candidates_token_count=4,
                ),
            ),
            SimpleNamespace(
                text="この回答も表示しない",
                usage_metadata=SimpleNamespace(
                    prompt_token_count=14,
                    candidates_token_count=8,
                ),
            ),
        ]
    )

    class FakeChat:
        def send_message(self, question, config=None):
            sent_questions.append((question, config))
            return next(responses)

    def create_chat(*, model):
        assert model == ask_module.MODEL
        chat = FakeChat()
        created_chats.append(chat)
        return chat

    client = SimpleNamespace(chats=SimpleNamespace(create=create_chat))

    def create_client(*, api_key):
        assert api_key == "test-key"
        return client

    monkeypatch.setattr(ask_module.genai, "Client", create_client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(
        "sys.argv",
        ["app.ask", "--measure", "2", "--temperature", "0.5", "測定する質問"],
    )
    timestamps = iter([0, 1, 2, 5])
    monkeypatch.setattr(ask_module.time, "perf_counter", lambda: next(timestamps))

    ask_module.main()

    output = capsys.readouterr().out
    assert len(created_chats) == 2
    assert [question for question, _ in sent_questions] == ["測定する質問"] * 2
    assert all(config.temperature == 0.5 for _, config in sent_questions)
    assert "1/2回目実行中..." in output
    assert "2/2回目実行中..." in output
    assert output.index("1/2回目実行中...") < output.index("2/2回目実行中...")
    assert "[1/2回目] [応答時間] 1.00秒 [トークン数] 入力: 10, 出力: 4" in output
    assert "[2/2回目] [応答時間] 3.00秒 [トークン数] 入力: 14, 出力: 8" in output
    assert "[平均応答時間] 2.00秒（2回）" in output
    assert "[平均トークン数] 入力: 12.0, 出力: 6.0" in output
    assert "この回答は表示しない" not in output
    assert "この回答も表示しない" not in output


def test_measure_uses_selected_model(monkeypatch, capsys):
    models_used = []

    class FakeChat:
        def send_message(self, question, config=None):
            assert question == "質問"
            assert config is None
            return SimpleNamespace(
                text="非表示の回答",
                usage_metadata=SimpleNamespace(
                    prompt_token_count=3,
                    candidates_token_count=2,
                ),
            )

    def create_chat(*, model):
        models_used.append(model)
        return FakeChat()

    client = SimpleNamespace(chats=SimpleNamespace(create=create_chat))

    def create_client(*, api_key):
        assert api_key == "test-key"
        return client

    monkeypatch.setattr(ask_module.genai, "Client", create_client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(
        "sys.argv",
        [
            "app.ask",
            "--measure",
            "2",
            "--model",
            "gemini-test-model",
            "質問",
        ],
    )

    ask_module.main()

    output = capsys.readouterr().out
    assert models_used == ["gemini-test-model", "gemini-test-model"]
    assert "[model] gemini-test-model" in output
    assert "非表示の回答" not in output


@pytest.mark.parametrize("count", ["0", "-1", "abc"])
def test_measure_rejects_invalid_repeat_count(monkeypatch, count):
    monkeypatch.setattr("sys.argv", ["app.ask", "--measure", count])

    with pytest.raises(SystemExit) as exc:
        ask_module.main()

    assert exc.value.code == 2
