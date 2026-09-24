# v2.2.0 Stability Audit

v2.1.7에서 확인한 기술부채를 기준으로 수정했다.

| 항목 | v2.2.0 처리 |
|---|---|
| Blob Service Worker 등록 | 외부 `sw.js` 표준 등록으로 교체 |
| origin 전체 캐시 삭제 위험 | `mylesson-` 접두어 캐시만 정리 |
| 배포 HTML 직접 수정 구조 | `src/`, `styles.css`, `tools/`, `docs/` 복원 |
| 보관 학생 신규 수업 가능 | 활성 학생만 lesson form에 전달, 상세 추가 버튼 차단 |
| 보관 학생 미래 반복 캘린더 재생성 가능 | Calendar cleanup 대상에서 제외 |
| 자동 학생 색상 순번 의존 | 정규화 시 색상 누락 학생에 색상 저장 |
| JSON import 검증 부족 | students/lessons/folders 정규화 및 참조 검증 추가 |
| Drive 영문 메시지 취약 | 구조화된 `_syncStatus` 메시지 코드 사용 |
| 중복 팔레트/font/keyframe/runtime CSS | 팔레트 단일화, font 1회 로드, CSS 외부 분리 |
| window 전역 callback | 모듈 스코프 handler로 변경 |
| 사진 base64 localStorage 압박 | IndexedDB 사진 캐시 분리 |
| native confirm/alert | 앱 내부 modal/notice로 교체 |
| 확대 금지 viewport | 제거 |

### 회귀 방지
`tools/audit.py`가 위 핵심 조건을 검사하며 Node.js가 있을 경우 `src/app.js`와 `sw.js` 문법도 검사한다. `tools/build.py`에도 배포 전 guard가 있다.

### 남겨둔 부분
`styles.css`에는 base → polish → responsive/form refinement 순으로 같은 selector를 후단에서 재정의하는 **의도적인 cascade override**가 일부 있다. 이는 단순 중복이 아니라 현재 UI 결과를 보존하기 위한 계층이므로 안정화 릴리스에서는 무리하게 병합하지 않았다. 다음 디자인 시스템 개편 때 component별 stylesheet로 분리하는 것이 안전하다.

현재 `src/app.js`는 원본 JSX가 아니라 과거 빌드 결과에서 복원한 소스다. v2.2.0부터는 이 파일을 기준 소스로 보관해 더 이상 배포 HTML을 직접 수정하지 않는다. 장기적으로는 React 컴포넌트 원본 형태로 단계적 재구성할 수 있다.
