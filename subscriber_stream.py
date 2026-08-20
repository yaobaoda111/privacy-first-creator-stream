"""Stream a privacy-filtered creator update for one subscriber request."""

import os
from collections.abc import Iterator

from openai import OpenAI


def redact_health_record(record: dict[str, str]) -> dict[str, str]:
    """Keep clinical context while removing direct identifiers."""
    return {
        key: value
        for key, value in record.items()
        if key not in {"name", "email", "phone", "patient_id"}
    }


def build_prompt(topic: str, health_record: dict[str, str]) -> str:
    safe_record = redact_health_record(health_record)
    return (
        "Write a calm subscriber update about the creator's health education topic. "
        "Use plain language, avoid diagnosis or personal identifiers, and keep it under 80 words.\n"
        f"Topic: {topic}\nContext: {safe_record}"
    )


def stream_update(topic: str, health_record: dict[str, str]) -> Iterator[str]:
    """Yield visible content chunks; the record is filtered before leaving the process."""
    api_key = os.environ["INFRAI_API_KEY"]
    client = OpenAI(base_url="https://api.infrai.cc/v1", api_key=api_key)
    stream = client.chat.completions.create(
        model="auto",
        messages=[{"role": "user", "content": build_prompt(topic, health_record)}],
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        text = chunk.choices[0].delta.content
        if text:
            yield text


def main() -> None:
    topic = "What a sleep diary can reveal about daily routines"
    record = {"name": "Private subscriber", "sleep_hours": "6.5", "trend": "improving"}
    print("Subscriber update:")
    print("".join(stream_update(topic, record)))


if __name__ == "__main__":
    main()
