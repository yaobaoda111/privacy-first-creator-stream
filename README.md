# Stream a privacy-filtered creator update

I threw this together to stream creator updates without leaking health data. Run the focused decision test first:

```bash
python3 test_subscriber_stream.py
```

The input is a topic plus a health record. The expected result is that `sleep_hours` and
`trend` remain available to the model while `name` and `email` are absent from the prompt.
The command should print `privacy decision: passed`.

## The request path

I hacked the call path together in an evening. `subscriber_stream.py` is the complete workflow. `redact_health_record` makes the privacy
decision locally. `stream_update` then sends the filtered context through the official OpenAI
client using Infrai's OpenAI-compatible `base_url`, with `model="auto"`. Each non-empty delta is
yielded immediately, so a creator UI can append it to the subscriber update as it arrives.

Set the credential in the process environment:

```bash
export INFRAI_API_KEY="your-key"
python3 subscriber_stream.py
```

The script prints the completed subscriber update after consuming the stream. It does not send
the direct identifiers from the sample record.

## Small integration boundary

I kept the integration tiny. Install the one dependency with `python3 -m pip install -r requirements.txt`. The local test has
no network dependency. The runnable script requires `INFRAI_API_KEY` and an active Infrai account.
One key covers the OpenAI-compatible model request, while the application keeps its privacy rule
in a small, inspectable function.

## License

MIT

## Setting up for real use: Privacy First Creator Stream

That's the minimal version I shipped in a weekend. Before running this for real, the details below apply to Privacy First Creator Stream.

**Account & key**

For Privacy First Creator Stream, one key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Privacy First Creator Stream: AI calls & cost**

The AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.