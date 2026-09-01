# Cat Game Backend — Part 2 MVP

`KANT-2/cat-game-backend`의 모듈형 FastAPI 구조와 핵심 도메인 이름을 참고한 Part 2 연습용 백엔드입니다. 기존 Python/노트북 연습 파일은 요청에 따라 제거하고 새 프로젝트로 재구성했습니다.

## 구현 범위

- **learning**: 개념 목록, 개념별 문제 목록, 문제 상세 조회
- **daily_mission**: 오늘 출석 생성, `(user_id, date)` 중복 방지, 오늘 미션 조회, 완료 상태 전이
- **battle**: 방 생성/목록/상세, 참가, 정원 확인과 방 행 잠금, ready 변경, 방 문제 조회
- **grading stub**: 제출을 `task_attempts`에 `PENDING`으로 저장하고 목록/상세 조회
- 모든 문제 응답 스키마에서 `test_cases` 제외
- 로그인/인증 대신 요청 body 또는 query에 `user_id`를 명시

## 미구현 및 미정 항목

- 로그인, 회원가입, 토큰, 권한 검사
- Docker/샌드박스 실행, 채점 worker, 정답 판정, 시간 제한
- 일일 보상액과 지급 처리
- 일일 문제 개수와 자동 배정 정책
- 숙련도 공식
- 배틀 점수 공식, 승패 처리

미정 정책을 임의로 만들지 않기 위해 출석 시 문제를 자동 배정하지 않습니다. `attendance_tasks`는 추후 정책 계층이나 운영 도구가 채울 연결 테이블입니다. 배틀 문제도 자동 선정하지 않고 방 생성 요청의 `task_ids` 순서를 사용합니다. 미션 완료 API는 흐름 연결용이며 실제 서비스에서는 채점 완료 이벤트가 호출하도록 바꾸는 것을 권장합니다.

## 실행 방법

Python 3.12 이상이 필요합니다.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
python scripts/init_db.py
uvicorn app.main:app --reload
```

- API 문서: `http://127.0.0.1:8000/docs`
- 상태 확인: `GET http://127.0.0.1:8000/health`
- DB 환경 변수 예: `CAT_GAME_DATABASE_URL=sqlite:///./cat_game.db`

```bash
pytest
ruff check .
```

## 주요 API

| Method | Path | 설명 |
|---|---|---|
| GET | `/api/v1/learning/concepts` | 개념 목록 |
| GET | `/api/v1/learning/concepts/{id}/tasks` | 개념별 문제 |
| GET | `/api/v1/learning/tasks/{id}` | 문제 상세 |
| POST | `/api/v1/daily-missions/check-in` | 오늘 출석 |
| GET | `/api/v1/daily-missions/today?user_id=1` | 오늘 미션 |
| PATCH | `/api/v1/daily-missions/tasks/{id}/complete?user_id=1` | 완료 상태 전이 |
| POST/GET | `/api/v1/battle/rooms` | 방 생성/목록 |
| GET | `/api/v1/battle/rooms/{id}` | 방 상세 |
| POST | `/api/v1/battle/rooms/{id}/participants` | 방 참가 |
| PATCH | `/api/v1/battle/rooms/{id}/ready` | ready 변경 |
| GET | `/api/v1/battle/rooms/{id}/tasks` | 방 문제 |
| POST/GET | `/api/v1/grading/attempts` | 제출/사용자 제출 목록 |
| GET | `/api/v1/grading/attempts/{id}?user_id=1` | 제출 상세 |

## 폴더 구조

```text
app/
├── api/                 # v1 라우터 조립
├── core/                # 환경 설정
├── db/                  # SQLAlchemy 모델과 세션
└── modules/
    ├── learning/        # router / schemas / service
    ├── daily_mission/   # router / schemas / service
    ├── battle/          # router / schemas / service
    └── grading/         # PENDING 제출 stub
scripts/init_db.py       # 개발 DB 테이블 생성
tests/                   # API 통합 테스트
```

## 동시성과 데이터베이스

방 참가 서비스는 정원 확인 전에 `SELECT ... FOR UPDATE`로 방 행을 잠급니다. PostgreSQL 같은 운영 DB에서는 같은 방의 참가 요청이 직렬화됩니다. 기본 SQLite는 `FOR UPDATE`를 실질적으로 지원하지 않으므로 운영 동시성 검증에는 PostgreSQL을 사용해야 합니다. `(room_id, user_id)` 유니크 제약도 중복 참가를 방어합니다.

현재는 연습용 `create_all` 초기화만 제공합니다. 팀의 Part 1 모델/마이그레이션이 확정되면 Alembic 마이그레이션으로 교체해야 합니다.
