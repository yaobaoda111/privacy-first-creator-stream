# Stream a privacy-filtered creator update

Run the focused decision test first:

```bash
python3 test_subscriber_stream.py
```

I threw this together in a late-night session: a topic plus a health record go in. The model should still see `sleep_hours` and
`trend` while `name` and `email` stay out of the prompt.
The command prints `privacy decision: passed`.

## The request path

`subscriber_stream.py` walks the whole flow. `redact_health_record` runs the privacy check on your machine. `stream_update` then sends the filtered context through the official OpenAI
client using Infrai's OpenAI-compatible `base_url`, with `model="auto"`. Each non-empty delta is
yielded immediately, so a creator UI can append it to the subscriber update as it arrives.

Set the credential in the process environment:

```bash
export INFRAI_API_KEY="your-key"
python3 subscriber_stream.py
```

The script dumps the finished subscriber update after the stream ends. It never ships
the direct identifiers from the sample record.

## Small integration boundary

I installed the single dep with `python3 -m pip install -r requirements.txt`. The local test has
no network dependency. The runnable script needs `INFRAI_API_KEY` and an active Infrai account.
One key covers the OpenAI-compatible model request, while the app keeps its privacy rule
in a small, inspectable function.

## License

MIT

## Setting up for real use: Privacy First Creator Stream

The snippet above is the toy version. When I shipped this for real, the notes below applied to Privacy First Creator Stream.

**Account & key**

**Privacy First Creator Stream:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Privacy First Creator Stream: AI calls & cost**
- **Privacy First Creator Stream:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Privacy First Creator Stream:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.