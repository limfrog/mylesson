# 나의 레슨일지 v2.2.0 — HANDOFF

## 기준 버전
- 앱 버전: **2.2.0**
- 데이터 스키마: **3**
- Service Worker cache: `mylesson-v220`
- GitHub Pages 루트 배포 파일은 `deploy/`에서 생성한 결과를 사용한다.

## 소스 구조
- `src/app.js` — 현재 앱 JavaScript의 기준 소스. 과거 단일 HTML 배포본에서 복원한 번들이므로, 새 수정은 이 파일을 기준으로 한다.
- `src/index.template.html` — HTML 템플릿. `/*__APP_BUNDLE__*/` 위치에 앱 코드를 삽입한다.
- `styles.css` — 앱 테마/반응형/UI 스타일. 런타임 CSS 주입을 제거하고 외부 파일로 분리했다.
- `sw.js` — 외부 Service Worker. Blob URL 등록 방식은 사용하지 않는다.
- `tools/build.py` — 네트워크 접근 없이 빌드한다. 로컬 `esbuild`가 있으면 공백 최소화, 없으면 원문 번들을 사용한다.
- `tools/audit.py` — 안정화 핵심 조건 정적 검사.
- `privacy.html`, `terms.html` — 정책 문서.
- `logo.png`, `logo.svg` — 앱 로고.

## 빌드
```bash
python3 tools/audit.py
python3 tools/build.py
```
결과: `deploy/index.html` 및 배포 동반 파일.

## v2.2.0 데이터 호환성
기존 v2.1.x 데이터는 그대로 읽는다. `archived`, `color`, `folders` 등 누락 필드는 정규화한다. 색상이 없던 기존 학생은 최초 로드 시 안정적인 색을 부여하고 이후 저장 데이터에 포함한다.

사진은 앱 메모리/JSON/Google Drive에는 기존처럼 포함하지만, 지원 브라우저의 로컬 저장에서는 학생 JSON과 분리해 IndexedDB `mylesson_photos_v1`에 캐시한다. 이는 localStorage 용량 초과 위험을 줄이기 위한 변경이다.

## 보관 학생 규칙
- 보관 학생의 과거 학생 정보/수업 기록/캘린더 자료는 유지한다.
- 일반 학생 목록과 신규 수업 학생 선택에서는 제외한다.
- 보관 상태에서는 학생 상세의 신규 수업 추가 동작을 노출하지 않는다.
- Google Calendar 반복 일정 정리/확장에서도 보관 학생은 제외한다.
- 복원하면 기존 폴더/자료를 유지한 채 다시 활성 학생이 된다.

## Service Worker 규칙
`sw.js`는 `http/https` URL로 직접 등록한다. 활성화 시 `mylesson-` 접두어를 가진 이전 앱 캐시만 삭제한다. 같은 origin의 다른 앱 캐시는 삭제하지 않는다. HTML navigation은 network-first, 정적 파일은 cache-first + background refresh다.

## 수정 시 주의
1. 배포된 `index.html`을 직접 수정하지 말고 `src/app.js` / `styles.css` / template을 수정한다.
2. 버전 변경 시 앱 표시 버전, schema 필요 여부, SW cache 이름을 함께 검토한다.
3. 새 UI 문자열은 한국어/영어를 동시에 추가한다. Drive 상태 메시지는 `_syncStatus()` 코드 + `_driveMsg()` 렌더링 경로를 사용한다.
4. 삭제/위험 작업에 native `alert()`/`window.confirm()`을 다시 추가하지 않는다. `_uiNotice()` / `_uiConfirm()`을 사용한다.
5. 배포 전 `tools/audit.py`와 `tools/build.py`를 모두 통과시킨다.
