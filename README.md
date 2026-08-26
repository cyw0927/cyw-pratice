# AX 2기 이미지 알고리즘 퀴즈

이 저장소는 문제 2 **컬러 이미지의 임계값을 계산하고 흑백 이미지 만들기**의 최종 코드, 75단계 학습 노트, AI 활용 기록, 풀이 설명과 테스트 결과를 한 흐름으로 정리한다.

## 현재 검증 상태

| 항목 | 현재 상태 |
|---|---:|
| 학습 질문 | 75개 |
| Notebook 전체 셀 | 151개 |
| 실행 완료 코드 셀 | 75개 |
| Notebook 오류 출력 | 0개 |
| 최종 코드 테스트 | 8개 PASS |
| 공식 예제 threshold | 102 |
| 공식 예제 결과 | `110`, `100`, `000` |

## 파일 구성

- `problem02.py`: 입력을 받아 정답 형식으로 출력하는 최종 실행 코드
- `problem02_learning.ipynb`: 설명과 실행 셀을 Q01~Q75로 구성한 누적 학습 노트
- `AI_LOG.md`: Notebook 질문과 1:1로 대응하는 AI 활용 학습·검증 기록
- `SOLUTION_GUIDE.md`: 문제 해석, 알고리즘, 함수 역할, 예제 추적과 복잡도 설명
- `TEST_RESULTS.md`: 테스트 입력, 예상값, 실제값과 자동 검증 결과
- `problem01.py`: 문제 1 관련 파일

## 문제 2 전체 흐름

```text
H, W와 RGB 입력
→ 공백으로 픽셀 분리
→ 쉼표로 R, G, B 분리
→ brightness = (R + G + B) // 3
→ 2차원 brightness_map 구성
→ threshold = 전체 밝기 합 // (H * W)
→ brightness >= threshold이면 1, 아니면 0
→ threshold와 흑백 행 출력
```

## 최종 코드 실행

저장소 폴더에서 다음 명령을 실행한다.

```powershell
python problem02.py
```

예제 입력:

```text
3 3
255,255,255 200,200,200 0,0,0
120,120,120 60,60,60 30,30,30
255,0,0 0,255,0 0,0,255
```

정상 출력:

```text
102
110
100
000
```

## Notebook 실행

VS Code에서 `problem02_learning.ipynb`를 열고 Python/Jupyter 커널을 선택한 뒤 `Run All`을 실행한다. 모든 학습 셀은 입력 대기 없이 실행되며, 오류 사례는 실행이 중단되지 않도록 코드 내부에서 안전하게 처리한다.

노트북은 다음 순서로 코드가 점진적으로 길어진다.

1. Q01~Q10: RGB와 한 픽셀의 밝기
2. Q11~Q21: 문자열 파싱, 한 행, 2차원 밝기 맵
3. Q22~Q35: 누적 합, threshold, 0/1 변환
4. Q36~Q48: 함수화와 예제 전체 연결
5. Q49~Q64: 경계값, 입력 검증, 복잡도
6. Q65~Q75: 실행 환경, `assert`, 전체 재구성

각 질문은 실행 전 예상, 중간 변수, 출력 해석, 헷갈린 점과 학습 정리를 포함한다.

## 문서 읽는 순서

처음 보는 경우 `README → problem02_learning.ipynb → AI_LOG → SOLUTION_GUIDE → TEST_RESULTS → problem02.py` 순서를 권장한다. 제출 전에는 Notebook의 `Run All`과 `TEST_RESULTS.md`의 예상값이 최종 코드 결과와 일치하는지 확인한다.

