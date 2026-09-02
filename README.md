# Cat Game Backend

코딩 학습, 채점, 일일 미션, 배틀, 랭킹·승급전, 경제, 상점·가챠, 고양이와 하우징을 제공하는 FastAPI 백엔드다.

## 구조 원칙

- 기능 중심 모듈형 모놀리스
- HTTP router와 비즈니스 규칙 분리
- 배틀은 서버 권위 상태 머신으로 관리
- Docker 채점과 일반 학습 기능 분리
- 재화 변경은 economy 모듈을 단일 진입점으로 사용
- 공개 방문자는 타인의 영구 상태에 read-only
- 미확정 가격·확률·보상 정책은 코드에 하드코딩하지 않음

## 시작

```bash
python -m venv .venv
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## 채점 MVP

채점 구현과 항목별 실제 검증 상태는
[검증된 채점 체크리스트](docs/features/verified-grading-checklist.md)를 참고한다.

```bash
docker build -t cat-game-python-grader:3.12 infra/docker/grader
uvicorn app.main:app --reload
```

- 제출: `POST /api/v1/attempts` → `202 PENDING`
- 조회: `GET /api/v1/attempts/{attempt_public_id}`
- 인증: 기존 팀 인증이 `app.api.dependencies.get_current_user`를 제공하거나 override한다.
- 운영 DB: Alembic과 PostgreSQL을 사용한다.
- 코드 크기, 운영 자원 제한값, 배틀 점수, 일일 보상은 정책 확정 전까지 TBD다.
