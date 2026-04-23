# Example Prompts

These are practical prompts that worked well enough for local testing.

## 1. Research product hero

```bash
hermes-codex-image \
  "Generate a premium hero image for a research visualization product called Paper Banana. Show a realistic peeled banana transforming into layered academic charts on a clean desk. Add Korean headline text exactly as: 논문을 한눈에 and a smaller subtitle exactly as: Paper Banana AI." \
  --output /tmp/paper-banana-hero.png
```

## 2. Korean landing banner

```bash
hermes-codex-image \
  "논문 요약 AI 서비스의 메인 배너 이미지를 만들어줘. 밝은 흰색 배경, 노란 바나나와 파란 데이터 차트가 함께 보이게 하고, 한국어 텍스트는 정확하고 읽기 쉽게 넣어줘. 문구는 정확히 '논문을 한눈에'로 넣어줘." \
  --output /tmp/korean-banner.png
```

## 3. Simple product asset card

```bash
hermes-codex-image \
  "Generate a premium flat illustration of a single yellow banana centered on a very light cream background card with soft shadow. Clean modern product-asset style. No text." \
  --output /tmp/banana-card.png
```

## 4. Hermes skill script

```bash
python3 skill/scripts/generate_with_codex.py \
  "Generate a soft pastel onboarding illustration for an AI research workspace" \
  --output /tmp/onboarding.png \
  --metadata-json /tmp/onboarding.json
```

## Prompting notes

- Quote exact text you need rendered.
- Ask for the intended use: hero, banner, product asset, sticker, thumbnail, etc.
- Keep one goal per prompt when possible.
- For edits, state invariants explicitly: what must stay unchanged.
- For public examples, verify the output visually before publishing it.
