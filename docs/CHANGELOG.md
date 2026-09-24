# Changelog

## 2.2.1 — 2026-09-25
- 학생 상세 화면의 학생 색상 명도를 계산해 밝은 배경에서는 어두운 글씨를 자동 적용
- 상세 화면의 수정/보관/삭제 버튼, 연락처/정보 카드, 메모 영역까지 대비 규칙 통일

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
