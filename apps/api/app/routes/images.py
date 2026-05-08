from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/images", tags=["images"])


class ImagePromptRequest(BaseModel):
    keyword: str
    draft: dict
    niche: str | None = None
    audience: str | None = None


@router.post("/prompt")
def generate_image_prompts(data: ImagePromptRequest):
    keyword = data.keyword.strip()
    draft = data.draft
    niche = data.niche or "digital marketing"
    audience = data.audience or "professionals"

    title = draft.get("title", keyword)

    prompts = [
        {
            "concept_name": "Modern dashboard concept",
            "prompt": (
                f"A clean modern feature image for a blog titled '{title}'. "
                f"Show a laptop dashboard with SEO charts, content planning boards, "
                f"keyword analytics, and automation workflow visuals. "
                f"Professional, polished, startup-friendly, for {audience} in {niche}. "
                f"Minimalist design, high quality, wide blog header composition."
            ),
            "style": "Modern SaaS illustration",
            "aspect_ratio": "16:9",
        },
        {
            "concept_name": "Team strategy concept",
            "prompt": (
                f"A professional blog header image about {keyword}. "
                f"Show a small startup team reviewing SEO strategy, content outlines, "
                f"traffic charts, and planning boards in a modern workspace. "
                f"Bright lighting, clean composition, business-focused, for {audience}. "
                f"High-quality editorial style, wide composition."
            ),
            "style": "Editorial business illustration",
            "aspect_ratio": "16:9",
        },
        {
            "concept_name": "Abstract growth concept",
            "prompt": (
                f"An abstract visual for a blog about {keyword}. "
                f"Use upward growth graphs, search icons, connected content blocks, "
                f"and automation flow arrows to represent SEO growth and content systems. "
                f"Modern, minimal, sleek, technology-focused, suitable for a SaaS blog. "
                f"High-resolution, wide header format."
            ),
            "style": "Abstract tech illustration",
            "aspect_ratio": "16:9",
        },
    ]

    return {
        "image_prompts": prompts
    }