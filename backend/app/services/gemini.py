"""Gemini-backed sleep coach.

Builds a tight prompt from the user's last 14 nights and asks Gemini for a
short, friendly, specific paragraph. We deliberately don't ask the model to
diagnose anything medical — it's a coach, not a doctor.
"""

from __future__ import annotations

import logging
from typing import Any

import google.generativeai as genai

from ..config import get_settings

log = logging.getLogger(__name__)


class GeminiUnavailable(RuntimeError):
    """Raised when GEMINI_API_KEY isn't set or the API call fails."""


_PROMPT = """You are a friendly, concise sleep coach. Write 2–3 sentences of
personalized insight for the user based on the last {n} nights of data below.
Speak like a thoughtful friend, not a medical professional. Be specific about
the numbers — name them. Don't use bullet points or markdown. Don't tell the
user to see a doctor or to "consult a professional." End with one small,
concrete suggestion.

Last {n} nights — summary metrics:
- Average sleep duration: {avg_duration_minutes} minutes (goal: {goal_minutes} minutes)
- Average self-reported quality: {avg_quality}/5
- Average bedtime: {avg_bedtime}
- Weekend drift vs weekdays: {weekend_drift_minutes:+d} minutes
- Bedtime consistency (stdev): ±{bedtime_consistency_minutes} minutes
- Current streak: {current_streak} consecutive nights logged

Write the response now (plain prose, 2–3 sentences):"""


def generate_weekly_insight(summary: dict[str, Any], goal: dict | None) -> str:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise GeminiUnavailable("GEMINI_API_KEY is not configured")

    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel(settings.gemini_model)

    goal_minutes = int((goal or {}).get("target_duration_minutes") or 480)
    prompt = _PROMPT.format(
        n=summary["sessions_count"],
        avg_duration_minutes=summary["avg_duration_minutes"],
        goal_minutes=goal_minutes,
        avg_quality=summary["avg_quality"],
        avg_bedtime=summary["avg_bedtime"] or "n/a",
        weekend_drift_minutes=summary["weekend_drift_minutes"],
        bedtime_consistency_minutes=summary["bedtime_consistency_minutes"],
        current_streak=summary["current_streak"],
    )

    try:
        response = model.generate_content(prompt)
    except Exception as exc:  # google's SDK raises a wide variety of errors
        log.exception("Gemini call failed")
        raise GeminiUnavailable(str(exc)) from exc

    text = (response.text or "").strip()
    if not text:
        raise GeminiUnavailable("Gemini returned empty text")
    return text
