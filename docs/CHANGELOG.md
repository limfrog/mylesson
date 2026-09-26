# Changelog

## 2.2.7 — 2026-09-26
- 로컬 JSON 백업에 앱 환경설정을 함께 저장하도록 확장했습니다.
- 백업 대상에 다크모드, 언어, 학생 표시항목 설정, 학생/수업 정렬 방식, 카드 밀도, 폴더 보기 상태, 접힌 폴더 상태, Google Calendar 동기화 사용 여부와 이벤트 색상 기준을 포함했습니다.
- Google 로그인 토큰, Drive 연결 정보, 앱 잠금 PIN/복구정보/생체인증 설정은 보안상 백업 대상에서 제외했습니다.
- 구버전 JSON 백업과의 하위 호환성을 유지했습니다.
- 환경설정이 포함된 백업을 복원하면 설정 적용을 위해 앱이 한 번 새로고침되도록 처리했습니다.

## 2.2.6 — 2026-09-26
- 앱 아이콘을 새 레슨 체크카드 + 음표 디자인으로 교체했습니다.
- favicon, Apple touch icon, Android/PWA 아이콘과 1024px 원본 아이콘을 추가했습니다.
- `manifest.webmanifest`를 추가하고 `index.html`의 아이콘 링크를 표준 외부 파일 방식으로 정리했습니다.
- `logo.png`를 새 아이콘으로 교체했습니다.
- Service Worker 캐시를 `mylesson-v226`으로 갱신했습니다.

## 2.2.5 — 2026-09-25
- 학생 목록 검색 대상에 메모 필드를 추가했습니다.

## 2.2.4 — 2026-09-25
- Google Calendar 이벤트 색상을 학생 개별색 또는 폴더색 기준으로 선택 가능
- 앱 색상을 Google Calendar 기본 이벤트 색 팔레트의 가장 가까운 색으로 매핑
- 선택한 색이 없거나 폴더색 모드에서 폴더 미지정 학생은 Google Calendar 기본색 사용
- 추가 Google Calendar 권한 없이 기존 calendar.events 권한만 사용

## 2.2.3 — 2026-09-25
- Prevent duplicate student saves and duplicate Google Calendar event creation with synchronous in-flight locks.
- Student save button is disabled while saving and shows a saving status.

## 2.2.2 — 2026-09-25
- 상단 점 3개 메뉴를 viewport 기준 플로팅 레이어로 조정해 상세 화면에서 가려지는 현상 방지.
- 개인정보처리방침/서비스 이용약관이 앱의 다크모드 설정을 자동으로 이어받도록 변경.
- 정책/약관 페이지 왼쪽 상단에 앱으로 돌아가는 고정 `닫기` 버튼 추가.

## 2.2.1 — 2026-09-25
- 학생 상세 화면의 학생 색상 명도를 계산해 밝은 배경에서는 어두운 글씨를 자동 적용.
- 상세 화면의 수정/보관/삭제 버튼, 연락처/정보 카드, 메모 영역까지 대비 규칙 통일.

## 2.2.0 — 2026-09-25
안정화 릴리스.

- Service Worker를 Blob 등록에서 표준 `sw.js` 등록으로 변경.
- 캐시 삭제 범위를 `mylesson-` 앱 캐시로 제한.
- 소스/템플릿/스타일/빌드/감사 구조를 GitHub에 다시 포함.
- 보관 학생을 신규 수업 등록 및 반복 캘린더 정리 대상에서 제외.
- 기존 무색상 학생에 안정적인 색상을 부여하는 데이터 정규화/마이그레이션 추가.
- JSON/Drive 데이터 로드시 students/lessons/folders를 정규화하고 손상 참조를 방어.
- 학생 사진의 로컬 저장을 IndexedDB로 분리하여 localStorage 용량 위험 완화.
- Drive 상태 메시지를 문자열 정규식 번역 중심에서 구조화된 status code 방식으로 변경.
- 중복 학생/폴더 색상 팔레트 제거.
- 중복 런타임 Google Font 로드와 CSS 주입 제거; `styles.css`로 분리.
- `window.__gcalCleanup`, `window.__requestLockSetup` 전역 연결 제거.
- native `window.confirm()` / `alert()` 제거 후 앱 내부 확인/알림 UI로 통일.
- 모바일 viewport의 확대 금지 옵션 제거.
- 정책 문서의 `운영자` 표현을 `개발자`로 통일.
- 정적 안정성 검사 `tools/audit.py` 추가.
