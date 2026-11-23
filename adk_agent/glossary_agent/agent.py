from google.adk.agents import Agent

from app import tools
from app.agent import INSTRUCTIONS

_SAVE_INSTRUCTION = (
    "- 学習記録の保存を頼まれたら save_learning_log を使う。"
    "保存前に必ず利用者の承認を求める。\n"
)
if _SAVE_INSTRUCTION not in INSTRUCTIONS:
    raise RuntimeError("INSTRUCTIONS に学習記録の承認指示が見つかりません。")

# この演習の対象ツールには保存ツールを含めないため、その指示だけ除く。
ADK_INSTRUCTIONS = INSTRUCTIONS.replace(_SAVE_INSTRUCTION, "")

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="glossary_agent",
    instruction=ADK_INSTRUCTIONS,
    tools=[
        tools.search_glossary,
        tools.get_lecture_summary,
        tools.make_quiz,
    ],
)
