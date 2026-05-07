from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/seo", tags=["seo"])


class SeoAnalysisRequest(BaseModel):
    keyword: str
    draft: dict


@router.post("/analyze")
def analyze_seo(data: SeoAnalysisRequest):
    draft = data.draft
    keyword = data.keyword.lower().strip()

    title = (draft.get("title") or "").lower()
    meta_description = (draft.get("meta_description") or "").lower()
    intro = (draft.get("intro") or "").lower()
    sections = draft.get("sections", [])
    faq = draft.get("faq", [])
    cta = draft.get("cta", "")

    full_text_parts = [
        draft.get("title", ""),
        draft.get("meta_title", ""),
        draft.get("meta_description", ""),
        draft.get("intro", ""),
        cta,
    ]

    for section in sections:
        full_text_parts.append(section.get("heading", ""))
        full_text_parts.append(section.get("content", ""))

    for item in faq:
        full_text_parts.append(item.get("question", ""))
        full_text_parts.append(item.get("answer", ""))

    full_text = " ".join(full_text_parts)
    full_text_lower = full_text.lower()

    issues = []
    score = 100

    if keyword not in title:
        issues.append("Primary keyword is missing from the title.")
        score -= 15

    if keyword not in meta_description:
        issues.append("Primary keyword is missing from the meta description.")
        score -= 10

    if keyword not in intro:
        issues.append("Primary keyword is missing from the introduction.")
        score -= 10

    if len(sections) < 3:
        issues.append("The draft has too few sections.")
        score -= 10

    if len(faq) < 2:
        issues.append("The FAQ section is too short.")
        score -= 10

    if not cta.strip():
        issues.append("The draft is missing a call to action.")
        score -= 10

    if len(full_text.split()) < 500:
        issues.append("The draft content is too short for a strong SEO article.")
        score -= 15

    keyword_count = full_text_lower.count(keyword)
    if keyword_count < 3:
        issues.append("Primary keyword usage is too low across the article.")
        score -= 10

    if score < 0:
        score = 0

    suggestions = []

    if "Primary keyword is missing from the title." in issues:
        suggestions.append("Add the primary keyword naturally into the title.")

    if "Primary keyword is missing from the meta description." in issues:
        suggestions.append("Include the primary keyword in the meta description.")

    if "Primary keyword is missing from the introduction." in issues:
        suggestions.append("Mention the primary keyword in the first paragraph.")

    if "The draft has too few sections." in issues:
        suggestions.append("Expand the article with more meaningful sections.")

    if "The FAQ section is too short." in issues:
        suggestions.append("Add more FAQ questions related to user search intent.")

    if "The draft is missing a call to action." in issues:
        suggestions.append("Include a stronger CTA at the end of the article.")

    if "The draft content is too short for a strong SEO article." in issues:
        suggestions.append("Add more detailed explanations and examples.")

    if "Primary keyword usage is too low across the article." in issues:
        suggestions.append("Increase natural keyword coverage throughout the draft.")

    return {
        "score": score,
        "issues": issues,
        "suggestions": suggestions,
        "keyword_count": keyword_count,
        "word_count": len(full_text.split()),
    }

class SeoOptimizeRequest(BaseModel):
    keyword: str
    draft: dict


@router.post("/optimize")
def optimize_seo(data: SeoOptimizeRequest):
    draft = data.draft
    keyword = data.keyword.strip()

    optimized_draft = {
        **draft,
        "title": draft.get("title", f"{keyword} Guide"),
        "meta_title": draft.get("meta_title", f"{keyword} Guide"),
        "meta_description": (
            f"Learn how to improve {keyword} with practical strategies, clear structure, "
            f"and actionable SEO recommendations."
        ),
        "intro": (
            f"{keyword} is an important part of a strong SEO strategy. "
            f"In this guide, you will learn practical methods, common mistakes to avoid, "
            f"and clear steps for applying it effectively."
        ),
        "cta": (
            f"Start applying these {keyword} strategies today to improve your content quality "
            f"and SEO performance."
        ),
    }

    optimized_sections = []
    for section in draft.get("sections", []):
        optimized_sections.append({
            "heading": section.get("heading", ""),
            "content": (
                f"{section.get('content', '')} "
                f"This section also reinforces how {keyword} should be used strategically "
                f"to support stronger organic search performance."
            ).strip()
        })

    optimized_draft["sections"] = optimized_sections

    if not optimized_draft.get("faq"):
        optimized_draft["faq"] = [
            {
                "question": f"What is {keyword}?",
                "answer": f"{keyword} refers to a practical SEO concept that helps improve search visibility and content performance."
            },
            {
                "question": f"Why is {keyword} important?",
                "answer": f"{keyword} is important because it helps content align more closely with search intent and user needs."
            }
        ]

    return {
        "optimized_draft": optimized_draft
    }