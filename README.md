# 나의 레슨일지 (My Lesson Diary)

현재 안정화 버전: **2.2.8**

## v2.2.8 변경사항
- 앱을 다시 열었을 때 저장된 Google 계정이 있고 access token이 만료되었거나 만료 임박 상태이면 자동 재연결을 먼저 시도
- Google Identity Services 스크립트 로딩을 최대 약 6초 기다린 뒤 재연결해 앱 시작 직후의 일시적 로딩 실패를 줄임
- 앱이 백그라운드에서 다시 활성화되거나 iOS PWA가 재개될 때 만료 토큰을 다시 자동 갱신 시도
- 자동 갱신 중복 요청을 하나로 합쳐 동시에 여러 토큰 요청이 발생하지 않도록 보호
- 토큰 유효 판정과 자동 갱신 시점을 모두 만료 5분 전으로 맞춰 기존 1분 불일치 구간 제거
- 자동 재연결 실패 시에만 기존 재로그인 안내 표시
- Service Worker 캐시를 mylesson-v228로 갱신

## 개발
```bash
python3 tools/audit.py
python3 tools/build.py
```

배포 결과는 `deploy/`에 생성된다. GitHub Pages 루트에는 `deploy`의 파일들을 배치한다.

자세한 구조와 수정 규칙은 `docs/HANDOFF.md`를 참고한다.
