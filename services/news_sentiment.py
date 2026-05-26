import os
import httpx
from typing import Dict, List, Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_KEY = os.getenv("DEEP_SEEK_KEY", "")

POSITIVE_KEYWORDS = [
    "lucro", "crescimento", "alta", "ganho", "subida", "positivo",
    "supera", "recorde", "expansao", "dividendo", "distribuicao",
    "aprovado", "upgrade", "recomendacao", "compra", "oportunidade",
    "resultado", "performance", "valorizacao", "aumento", "forte",
]

NEGATIVE_KEYWORDS = [
    "prejuizo", "queda", "baixa", "perda", "negativo", "abaixo",
    "crise", "recessao", "desacelera", "problema", "investigacao",
    "processo", "multa", "dano", "risco", "downgrade", "venda",
    "fraude", "escandalo", "corrupcao", "desastre", "falha",
]


def keyword_sentiment_analysis(text: str) -> Dict:
    text_lower = text.lower()
    positive = sum(1 for kw in POSITIVE_KEYWORDS if kw in text_lower)
    negative = sum(1 for kw in NEGATIVE_KEYWORDS if kw in text_lower)
    return {"positive": positive, "negative": negative}


async def ai_sentiment_analysis(articles: List[Dict]) -> Dict:
    if not DEEPSEEK_KEY:
        return keyword_batch_analysis(articles)

    try:
        client = AsyncOpenAI(
            api_key=DEEPSEEK_KEY,
            base_url="https://api.deepseek.com",
        )

        titles = "\n".join([f"- {a.get('title', '')}" for a in articles[:5]])

        prompt = f"""Analise o sentimento das seguintes noticias financeiras sobre acoes brasileiras.
Para cada noticia, liste fatores positivos e negativos.

Noticias:
{titles}

Retorne apenas um JSON com:
{{
  "positive_factors": ["lista de fatores positivos encontrados"],
  "negative_factors": ["lista de fatores negativos encontrados"]
}}"""

        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )

        content = response.choices[0].message.content.strip()

        import json
        try:
            result = json.loads(content)
            positive_count = len(result.get("positive_factors", []))
            negative_count = len(result.get("negative_factors", []))
        except json.JSONDecodeError:
            return keyword_batch_analysis(articles)

        return {
            "positive": positive_count,
            "negative": negative_count,
        }
    except Exception as e:
        print(f"DeepSeek sentiment error: {e}")
        return keyword_batch_analysis(articles)


def keyword_batch_analysis(articles: List[Dict]) -> Dict:
    total_positive = 0
    total_negative = 0
    for article in articles:
        text = f"{article.get('title', '')} {article.get('body', '')}"
        result = keyword_sentiment_analysis(text)
        total_positive += result["positive"]
        total_negative += result["negative"]
    return {"positive": total_positive, "negative": total_negative}


def classify_sentiment(positive: int, negative: int) -> Optional[str]:
    if positive > negative:
        return "boa"
    elif negative > positive:
        return "ruim"
    return None
