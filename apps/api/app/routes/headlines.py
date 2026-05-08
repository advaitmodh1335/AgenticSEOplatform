from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/headlines", tags=["headlines"])


class HeadlineRequest(BaseModel):
    keyword: str
    draft: dict


def score_headline(headline: str, keyword: str):
    score = 50
    text = headline.lower()
    keyword = keyword.lower().strip()

    if keyword and keyword in text:
        score += 20

    if len(headline) >= 40 and len(headline) <= 70:
        score += 15
    else:
        score -= 5

    power_words = ["best", "guide", "how", "improve", "boost", "strategy", "tips"]
    power_word_hits = sum(1 for word in power_words if word in text)
    score += min(power_word_hits * 3, 12)

    if ":" in headline:
        score += 5

    if headline.endswith("?"):
        score += 3

    return min(score, 100)


@router.post("/generate")
def generate_headlines(data: HeadlineRequest):
    keyword = data.keyword.strip()
    draft = data.draft

    base_title = draft.get("title", f"{keyword} Guide")

    variants = [
        base_title,
        f"How to Improve {keyword} for Better SEO Results",
        f"{keyword}: A Practical Guide for Faster SEO Growth",
        f"Best Practices for {keyword} in 2026",
        f"How Startup Founders Can Use {keyword} to Boost SEO",
        f"{keyword} Tips: What Actually Works for Organic Growth",
        f"Why {keyword} Matters More Than Ever for SEO",
    ]

    unique_variants = []
    seen = set()
    for title in variants:
        normalized = title.strip().lower()
        if normalized not in seen:
            seen.add(normalized)
            unique_variants.append(title)

    ranked = []
    for title in unique_variants:
        ranked.append({
            "headline": title,
            "score": score_headline(title, keyword),
        })

    ranked.sort(key=lambda item: item["score"], reverse=True)

    return {
        "headlines": ranked
    }