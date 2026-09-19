"""promptfoo output transform — strip the <thinking> fence before assertions.

sentiment_v2's contract: model reasons inside <thinking>...</thinking>, then
emits ONLY the JSON object after the fence. This transform extracts that
payload so is-json / label assertions see clean JSON.

For sentiment_v1 output (bare JSON, no fence) the transform is a no-op —
split() returns a single-element list and [-1] is the whole string.

Same extraction logic as src/week3/lab_sentiment.py (TODO 5), with one
difference: promptfoo already strips whitespace, so no .strip() needed here.
"""

def get_transform(output: str, context) -> str:
    return output.split("</thinking>")[-1]