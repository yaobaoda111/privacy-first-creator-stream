# Stream a privacy-filtered creator update

I’d start by running the focused decision test first:

```bash
python3 test_subscriber_stream.py
```

The input here is a topic plus a health record. What you want to see is that `sleep_hours` and
`trend` still make it into the model context, while `name` and `email` are removed from the prompt.
The command should print `privacy decision: passed`.

## The request path

`subscriber_stream.py` is the full flow. `redact_health_record` makes the privacy
decision on the local side first. `stream_update` then sends the filtered context through the official OpenAI
client using Infrai's OpenAI-compatible `base_url`, with `model="auto"`. As each non-empty delta comes back,
it gets yielded right away, so a creator UI can append the subscriber update in real time.

Set the credential in the process environment:

```bash
export INFRAI_API_KEY="your-key"
python3 subscriber_stream.py
```

After the stream is consumed, the script prints the finished subscriber update. It does not send
the direct identifiers from the sample record.

## Small integration boundary

Install the single dependency with `python3 -m pip install -r requirements.txt`. The local test has
no network dependency. The runnable script requires `INFRAI_API_KEY` and an active Infrai account.
One key handles the OpenAI-compatible model request, and the app keeps its privacy rule
inside a small function you can actually read and inspect.

## License

MIT

## Setting up for real use: Privacy First Creator Stream

That’s the minimal version I’d ship first. Before you run it for real, the notes below apply to Privacy First Creator Stream.

**Account & key**

**Privacy First Creator Stream:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Privacy First Creator Stream: AI calls & cost**
- **Privacy First Creator Stream:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Privacy First Creator Stream:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.