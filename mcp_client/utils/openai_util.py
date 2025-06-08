import os
from openai import OpenAI
from dotenv import load_dotenv

# .envからAPIキーを読み込み
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 分類用プロンプトテンプレートの読み込み
with open("prompt/classify_prompt.txt", "r", encoding="utf-8") as f:
    classify_template = f.read()

def classify_question(question: str) -> str:
    prompt = classify_template.replace("{{question}}", question)

    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": "あなたは証券分野のアシスタントです。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    answer = response.choices[0].message.content.strip().lower()
    if "知識" in answer:
        return "knowledge"
    elif "データ" in answer:
        return "data"
    else:
        return "unknown"

def ask_openai(question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは金融に詳しい証券アナリストのようにユーザーに優しく説明します。"},
            {"role": "user", "content": question}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def generate_natural_language(data: dict) -> str:
    if data.get("pbr", -1) < 0:
        return f"{data.get('company_name', '該当企業')}の財務情報を取得できませんでした。"

    # ユーザーの質問内容を組み込む
    original_question = data.get("original_question", "")

    prompt = (
        f"企業名: {data['company_name']}\n"
        f"ティッカー: {data['ticker']}\n"
        f"PBR: {data['pbr']:.2f}\n"
        f"PER: {data['per']:.2f}\n"
        f"ROE: {data['roe']:.2f}\n"
        f"時価総額: {data['market_cap']:,}円\n"
        f"配当利回り: {data['dividend_yield'] * 100:.2f}%\n\n"
        "この情報をもとに、証券アナリストとして"f"ユーザーの質問: {original_question}""について解説してください。"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは投資家向けにアドバイスを行う証券アナリストです。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()


