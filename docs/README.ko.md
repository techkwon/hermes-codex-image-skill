# Hermes Codex Image Skill 한국어 안내

이 문서는 **AI를 처음 쓰는 사용자**와 **Hermes/OpenClaw 에이전트에게 설치를 맡기려는 사용자**를 위한 한국어 보조 안내입니다.

가장 중요한 요약:

- 이 저장소는 **로컬 Codex CLI 이미지 생성을 더 쉽게 자동화**하기 위한 작은 Python 래퍼입니다.
- `codex`가 이미 설치되어 있고, 로그인도 되어 있어야 합니다.
- 이 저장소 자체가 로그인까지 대신 해주지는 않습니다.

---

## 이 저장소가 하는 일

쉽게 말하면:

1. `codex exec`로 이미지를 생성시킵니다.
2. Codex가 만든 이미지 파일을 찾습니다.
3. 그 파일을 사용자가 지정한 경로로 복사합니다.
4. 자동화가 읽기 쉬운 JSON 결과도 같이 남길 수 있습니다.

즉,
이 프로젝트는 **이미지 생성 서비스 자체**가 아니라,
**이미 로그인된 Codex CLI를 Hermes/OpenClaw에서 안정적으로 재사용하게 해주는 연결 래퍼**입니다.

---

## 시작 전에 꼭 필요한 것

### 필수
- Python **3.11 이상**
- 로컬 `codex` CLI 설치
- 로컬 `codex login` 완료 상태

### 먼저 확인할 명령

```bash
python3.11 --version
codex --version
codex login status
```

정상이라면:
- Python 버전이 3.11 이상으로 보이고
- Codex 버전이 출력되고
- 로그인 상태가 정상으로 나와야 합니다.

만약 여기서 막히면,
이 저장소 문제라기보다 **사전 준비 문제**일 가능성이 큽니다.

---

## 초심자용 가장 쉬운 설치 순서

터미널에서 아래를 그대로 실행하시면 됩니다.

```bash
git clone https://github.com/techkwon/hermes-codex-image-skill.git
cd hermes-codex-image-skill
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -e .[dev]
```

설치가 끝난 뒤 아래를 실행해 보세요.

```bash
hermes-codex-image --help
```

도움말이 뜨면 설치는 정상입니다.

---

## 첫 테스트 실행

`codex login status`가 정상이라면 아래처럼 테스트할 수 있습니다.

```bash
hermes-codex-image \
  "Generate a minimal banana icon on a light background" \
  --output /tmp/hermes-codex-image-smoke.png \
  --metadata-json /tmp/hermes-codex-image-smoke.json
```

정상이라면:
- `/tmp/hermes-codex-image-smoke.png` 이미지 파일 생성
- `/tmp/hermes-codex-image-smoke.json` 메타데이터 생성

---

## Hermes에게 설치를 맡기고 싶다면

Hermes/OpenClaw 같은 에이전트에게는 이렇게 말하면 됩니다.

> 이 저장소를 초심자 기준으로 설치해줘. Python 먼저 확인하고, Codex 설치 여부와 로그인 상태를 확인한 다음, 가상환경 만들고 설치하고, lint/test/build까지 검증한 뒤 무엇이 성공했고 무엇이 내 수동 조치가 필요한지 정확히 알려줘.

이렇게 말하면 에이전트가 보통 더 안전한 순서로 진행합니다.

---

## 에이전트가 따라야 할 권장 순서

1. Python 버전 확인
2. `codex --version` 확인
3. `codex login status` 확인
4. 가상환경 생성
5. `pip install -e .[dev]`
6. `hermes-codex-image --version`
7. `ruff check .`
8. `pytest`
9. `python -m build`
10. 필요 시 실제 이미지 스모크 테스트

---

## 자주 막히는 경우

### 1) `python3.11`이 없음
다른 Python 3.11+ 실행 파일을 써야 합니다.
예:

```bash
python3 --version
python3 -m venv .venv
```

### 2) `codex: command not found`
Codex CLI가 설치되지 않았거나 PATH에 없습니다.
먼저 Codex 쪽을 해결해야 합니다.

### 3) `codex login status`가 비정상
Codex에 먼저 로그인해야 합니다.
이 저장소는 로그인 자체를 대신 처리하지 않습니다.

### 4) 설치는 됐는데 실제 생성 실패
보통 아래 중 하나입니다.
- Codex 로그인 상태 문제
- Codex 출력 형식 변화
- 타임아웃

이럴 때는 timeout을 늘려볼 수 있습니다.

```bash
hermes-codex-image "Generate a minimal banana icon on a light background" --output /tmp/test.png --timeout 300
```

---

## 어떤 문서를 먼저 보면 좋은가

- `README.md` → 전체 개요
- `docs/HERMES_AGENT_INSTALL.md` → 영어 기준 자세한 설치 안내
- `docs/README.ko.md` → 한국어 초심자 안내
- `docs/VISUAL_QUICKSTART.md` → 빠르게 보는 시각형 설치 흐름
- `docs/TROUBLESHOOTING_QUICK.md` → 가장 빠른 문제 원인 체크
- `AGENTS.md` → 에이전트 전용 빠른 지침
- `skill/SKILL.md` → 스킬 관점 설명
- `docs/KNOWN_LIMITATIONS.md` → 과장 없이 한계 설명

---

## 꼭 기억할 점

이 저장소는 **실용적인 자동화 래퍼**입니다.

즉:
- 로컬 Codex 이미지 생성 흐름을 더 다루기 쉽게 만들어주지만,
- Codex 내부 백엔드 모델의 정확한 정체를 증명하는 프로젝트는 아닙니다.
- 앞으로 Codex CLI 동작이 바뀌면 유지보수가 필요할 수 있습니다.
