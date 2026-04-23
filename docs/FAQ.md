# Beginner FAQ

This page answers the questions a first-time user is most likely to ask.

---

## 1. What does this repository actually do?

It gives you a small Python command that reuses your **already logged-in local Codex CLI** to generate an image, save the image to a stable path, and optionally save JSON metadata.

It is an automation wrapper, not a hosted image website.

---

## 2. Do I need a Codex account or login first?

Yes.

This repository expects:
- `codex` is installed
- `codex login status` is healthy

It does **not** perform the login step for you.

---

## 3. Do I need Python?

Yes.

You need **Python 3.11 or newer** to install and run the wrapper.

Check it with:

```bash
python3.11 --version
```

If that command is missing, try another Python 3.11+ binary like `python3`.

---

## 4. What is the quickest proof that installation worked?

Run:

```bash
hermes-codex-image --help
```

If you see usage/help text, the package installed correctly.

---

## 5. What is the quickest proof that the repository itself is healthy?

Run:

```bash
make doctor
```

That checks:
- CLI version
- `ruff`
- `pytest`
- package build

If those pass, the repo is healthy.

---

## 6. What is the first real image generation test?

If Codex is installed and logged in:

```bash
hermes-codex-image \
  "Generate a minimal banana icon on a light background" \
  --output /tmp/hermes-codex-image-smoke.png \
  --metadata-json /tmp/hermes-codex-image-smoke.json
```

Expected result:
- one image file
- one JSON metadata file

---

## 7. What if `hermes-codex-image --help` works, but image generation fails?

That usually means:
- package install is fine
- but Codex runtime/login/output behavior is the issue

Check:

```bash
codex --version
codex login status
```

Then see:
- [TROUBLESHOOTING_QUICK.md](TROUBLESHOOTING_QUICK.md)

---

## 8. Can Hermes Agent install this for me automatically?

Yes.

Give Hermes this prompt:

```text
Open this repository and install it for me like I am a first-time user. Check Python first, check whether Codex is installed and logged in, create the virtualenv, install the package, run lint/tests/build, and then summarize exactly what worked and what still needs my action.
```

Korean version:

```text
이 저장소를 초심자 기준으로 설치해줘. Python 먼저 확인하고, Codex 설치 여부와 로그인 상태를 확인한 다음, 가상환경을 만들고, 패키지를 설치하고, lint/test/build까지 검증한 뒤 무엇이 성공했고 무엇이 내 수동 조치가 필요한지 정확히 알려줘.
```

Also point Hermes to:
- [../AGENTS.md](../AGENTS.md)

---

## 9. Is this an official OpenAI Images API client?

No.

This project is intentionally narrower than that.
It wraps local Codex CLI image generation.

---

## 10. Which document should I read first?

Choose one:

- fastest install → [../README.md](../README.md)
- detailed install guide → [HERMES_AGENT_INSTALL.md](HERMES_AGENT_INSTALL.md)
- Korean guide → [README.ko.md](README.ko.md)
- visual flow → [VISUAL_QUICKSTART.md](VISUAL_QUICKSTART.md)
- troubleshooting → [TROUBLESHOOTING_QUICK.md](TROUBLESHOOTING_QUICK.md)
- preview/share copy → [GITHUB_PREVIEW_COPY.md](GITHUB_PREVIEW_COPY.md)
- Instagram promo pack → [INSTAGRAM_PROMO_PACK.md](INSTAGRAM_PROMO_PACK.md)

---

## 11. What should I do if I am still stuck?

Check in this order:

1. Python version
2. Codex installed
3. Codex login healthy
4. package installed
5. `make doctor` passes
6. real smoke test

If needed, collect the exact failing command and its output before asking for help.
