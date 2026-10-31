import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"), override=True)


FALLBACK_SUMMARY = (
    "The AI could not explain the offers right now.\n"
    "The offer prices are still shown in the comparison.\n"
    "The cheapest offer is marked by the app."
)


class OllamaUnavailable(RuntimeError):
    """The local Ollama service or configured model cannot be reached."""


class AssistantError(RuntimeError):
    """Ollama responded but could not complete the request."""


def ask_about_catalog(question, cars, quotes):
    """Answer using only catalog and quote rows supplied by the app."""
    model = os.getenv("OLLAMA_MODEL", "").strip()
    if not model:
        raise OllamaUnavailable("Set OLLAMA_MODEL in your .env file.")

    context = json.dumps(
        {"catalog": cars, "dealer_quotes": quotes},
        ensure_ascii=True,
        default=str,
    )
    prompt = (
        "Answer the buyer using only the supplied JSON data. "
        "Do not use outside knowledge or guess missing specifications, prices, "
        "discounts, safety ratings, or availability. If the data does not contain "
        "an answer, say that the information is unavailable. Do not calculate prices; "
        "the app's Python code does all price math.\n\n"
        f"DATA:\n{context}\n\nQUESTION:\n{question.strip()}"
    )

    try:
        import ollama
    except ImportError as error:
        raise OllamaUnavailable("The Ollama Python package is not installed.") from error

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": "Use only the data supplied in the user message."},
                {"role": "user", "content": prompt},
            ],
            options={"temperature": 0},
        )
    except Exception as error:
        message = str(error).lower()
        unavailable_markers = (
            "connection refused",
            "failed to connect",
            "connection error",
            "model not found",
            "not running",
        )
        if isinstance(error, (ConnectionError, TimeoutError, OSError)) or any(
            marker in message for marker in unavailable_markers
        ):
            raise OllamaUnavailable(
                "Ollama is unavailable. Start Ollama and make sure the model is installed."
            ) from error
        raise AssistantError("Ollama returned an error. Please try again.") from error

    answer = response.message.content.strip()
    if not answer:
        raise AssistantError("Ollama returned an empty answer.")
    return answer


def summarize_offers(offers):
    """Ask the local Ollama model for exactly three short lines."""
    model = os.getenv("OLLAMA_MODEL", "").strip()
    if not model:
        return FALLBACK_SUMMARY

    offer_lines = "\n".join(
        f"{offer['dealer']}: {offer['total']}"
        + (" (cheapest)" if offer["cheapest"] else "")
        for offer in offers
    )
    prompt = (
        "Explain these already-calculated car offer totals in simple words. "
        "Do not calculate or change any prices. Write exactly three short lines.\n"
        f"{offer_lines}"
    )

    try:
        import ollama

        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        lines = [line.strip() for line in response.message.content.splitlines() if line.strip()]
        if not lines:
            return FALLBACK_SUMMARY
        lines = lines[:3]
        while len(lines) < 3:
            lines.append("See the comparison table for the exact prices.")
        return "\n".join(lines)
    except Exception:
        return FALLBACK_SUMMARY
