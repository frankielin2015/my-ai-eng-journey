Classify the sentiment of the product review as "positive", "negative", "mixed", or "neutral".

Respond with ONLY a JSON object with these keys:
- sentiment: "positive" | "negative" | "mixed" | "neutral"
- confidence: number between 0.0 and 1.0
- key_topics: list of up to 5 topic strings
- reasoning: one sentence explaining the classification

Review: {{user_text}}