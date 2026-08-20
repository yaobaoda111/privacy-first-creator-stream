from subscriber_stream import build_prompt, redact_health_record


def test_subscriber_prompt_keeps_context_and_removes_identifiers() -> None:
    record = {
        "name": "Ada Example",
        "email": "ada@example.test",
        "sleep_hours": "6.5",
        "trend": "improving",
    }

    safe = redact_health_record(record)
    prompt = build_prompt("Sleep diary", record)

    assert safe == {"sleep_hours": "6.5", "trend": "improving"}
    assert "6.5" in prompt
    assert "Ada Example" not in prompt
    assert "ada@example.test" not in prompt


if __name__ == "__main__":
    test_subscriber_prompt_keeps_context_and_removes_identifiers()
    print("privacy decision: passed")

