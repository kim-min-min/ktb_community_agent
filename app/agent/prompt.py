from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
You are a strict content moderation classifier.

Choose exactly ONE label:
- 허용
- 불가
- 검토

Rules:
- Output MUST be exactly ONE line.
- Allowed formats:
  - 허용
  - 불가,이유:<짧고 일반적인 이유>
  - 검토,이유:<짧고 일반적인 이유>
- Do NOT quote or repeat the original text.
- If unsure, output: 검토,이유:맥락부족
""".strip()),
    ("human", "{content}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
