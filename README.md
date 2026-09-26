# 나의 레슨일지 (My Lesson Diary)

현재 안정화 버전: **2.2.7**

## v2.2.7 변경사항
- 로컬 JSON 백업에 앱 환경설정 포함
- 다크 모드, 언어, 학생 표시 항목, 정렬/밀도, 폴더 보기·접힘 상태 백업/복원
- 수업 목록 정렬/밀도/폴더 보기·접힘 상태 백업/복원
- Google Calendar 동기화 사용 여부와 이벤트 색상 기준 백업/복원
- Google 로그인 토큰·Drive 연결 정보·앱 잠금 PIN/복구정보는 보안상 백업에서 제외
- 구버전 JSON 백업은 기존처럼 학생·수업·폴더 데이터만 정상 복원
- Service Worker 캐시를 mylesson-v227로 갱신

## 개발
```bash
python3 tools/audit.py
python3 tools/build.py
```

배포 결과는 `deploy/`에 생성된다. GitHub Pages 루트에는 `deploy`의 파일들을 배치한다.

자세한 구조와 수정 규칙은 `docs/HANDOFF.md`를 참고한다.
