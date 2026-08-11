import os
import json
import logging
from typing import List, Dict, Optional
import httpx

from models import HouseholdProfile, HouseholdMission, Product, RecommendationResponse
from catalog_data import PRODUCTS_CATALOG, MISSIONS_TEMPLATE

logger = logging.getLogger("heyblinkit.engine")

class HouseholdRecommendationEngine:
    def __init__(self):
        self.products = PRODUCTS_CATALOG
        self.mission_templates = MISSIONS_TEMPLATE

    def _generate_groq_insights(self, profile: HouseholdProfile) -> Optional[Dict[str, str]]:
        """
        Attempts to generate hyper-personalized persona tag and recommendation rationale
        using the Groq API (https://api.groq.com/openai/v1).
        Falls back to local heuristic rules if key is missing or request fails.
        """
        api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")
        if not api_key:
            return None

        # Determine endpoint and model based on API key prefix/env
        if api_key.startswith("xai-"):
            endpoint = "https://api.x.ai/v1/chat/completions"
            model_name = os.getenv("GROK_MODEL", "grok-2-latest")
        else:
            endpoint = "https://api.groq.com/openai/v1/chat/completions"
            model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

        prompt_content = (
            f"User Profile details:\n"
            f"- Registered Rooms: {', '.join(profile.rooms) if profile.rooms else 'None'}\n"
            f"- Home Descriptors: {', '.join(profile.home_descriptors) if profile.home_descriptors else 'None'}\n"
            f"- Monthly Goals: {', '.join(profile.monthly_goals) if profile.monthly_goals else 'None'}\n"
            f"- Custom Needs / Specific Request: '{profile.specific_help or 'None'}'\n\n"
            "Return JSON only with keys:\n"
            "1. 'persona_tag': short punchy title (max 5 words, e.g. 'Active & Fitness Household')\n"
            "2. 'recommendation_rationale': 1-2 engaging sentences explaining why their feed is prioritized for their specific home setup and custom needs."
        )

        try:
            with httpx.Client(timeout=4.5) as client:
                resp = client.post(
                    endpoint,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model_name,
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "You are the AI Recommendation Engine for HeyBlinkit hyper-local 8-minute delivery. "
                                    "Provide response ONLY in strict JSON format with keys 'persona_tag' and 'recommendation_rationale'."
                                )
                            },
                            {
                                "role": "user",
                                "content": prompt_content
                            }
                        ],
                        "temperature": 0.3
                    }
                )

                if resp.status_code == 200:
                    data = resp.json()
                    content = data["choices"][0]["message"]["content"].strip()
                    # Strip code markdown ticks if present
                    if content.startswith("```"):
                        content = content.split("```")[1]
                        if content.startswith("json"):
                            content = content[4:]
                    content = content.strip()
                    parsed = json.loads(content)
                    if "persona_tag" in parsed and "recommendation_rationale" in parsed:
                        logger.info("Successfully fetched Groq AI insights")
                        return {
                            "persona_tag": parsed["persona_tag"],
                            "recommendation_rationale": parsed["recommendation_rationale"]
                        }
                else:
                    logger.warning(f"Groq API returned status {resp.status_code}: {resp.text}")
        except Exception as e:
            logger.warning(f"Failed to fetch Groq AI insights, using local fallback: {e}")

        return None

    def compute_recommendations(self, profile: HouseholdProfile) -> RecommendationResponse:
        # Score each mission template based on Household Mental Model
        scored_missions: List[HouseholdMission] = []

        rooms_set = set(profile.rooms)
        goals_set = set(profile.monthly_goals)
        desc_set = set(profile.home_descriptors)

        for template in self.mission_templates:
            score = 50.0  # Base affinity score

            # Room matching (+30)
            if template["target_room"] in rooms_set:
                score += 30.0

            # Fitness matching
            if "Gym" in rooms_set or "Fitness-focused" in desc_set or "Stay fit" in goals_set:
                if template["id"] == "level-up-workouts":
                    score += 50.0

            # Pet matching
            if "Pet Corner" in rooms_set or "Pet parents" in desc_set:
                if template["id"] == "pet-care":
                    score += 50.0

            # Healthy eating / Breakfast matching
            if "Healthy eating" in desc_set or "Eat healthier" in goals_set:
                if template["id"] == "morning-breakfast":
                    score += 40.0

            # Busy professional / Save time
            if "Busy professionals" in desc_set or "Save time" in goals_set:
                if template["id"] in ["morning-breakfast", "freshen-home"]:
                    score += 35.0

            # Entertain guests
            if "Guests often visit" in desc_set or "Entertain guests" in goals_set:
                if template["id"] == "movie-marathon":
                    score += 45.0

            mission = HouseholdMission(
                id=template["id"],
                title=template["title"],
                subtitle=template["subtitle"],
                eyebrow=template["eyebrow"],
                target_room=template["target_room"],
                target_routine=template["target_routine"],
                match_score=round(score, 1),
                recommended_product_ids=template["recommended_product_ids"],
                cta=template["cta"]
            )
            scored_missions.append(mission)

        # Sort missions by match score descending
        scored_missions.sort(key=lambda m: m.match_score, reverse=True)

        top_slugs = [m.id for m in scored_missions]

        # Priority Products: select products matching top 3 missions
        top_product_ids = set()
        for m in scored_missions[:3]:
            top_product_ids.update(m.recommended_product_ids)

        priority_products = [
            Product(**p) for p in self.products if p["id"] in top_product_ids
        ]

        # Determine Persona Tag & Rationale (Try Groq AI first, fallback to heuristics)
        groq_data = self._generate_groq_insights(profile)

        if groq_data:
            persona = groq_data["persona_tag"]
            rationale = groq_data["recommendation_rationale"]
        else:
            persona = "Multi-Purpose Household"
            if "Fitness-focused" in desc_set or "Stay fit" in goals_set:
                persona = "Active & Fitness Household"
            elif "Pet parents" in desc_set:
                persona = "Pet Parent Household"
            elif "Busy professionals" in desc_set or "Save time" in goals_set:
                persona = "Executive & Time-Optimized"
            elif "Guests often visit" in desc_set:
                persona = "Hosting & Social Household"

            rationale = (
                f"Modeled based on {len(profile.rooms)} registered rooms ({', '.join(profile.rooms[:3]) or 'All'}) "
                f"and focus goals: {', '.join(profile.monthly_goals[:2]) or 'General Household'}. "
                "Products are grouped into single-click mission bundles."
            )

        return RecommendationResponse(
            profile=profile,
            top_mission_slugs=top_slugs,
            missions=scored_missions,
            priority_products=priority_products,
            persona_tag=persona,
            recommendation_rationale=rationale
        )

