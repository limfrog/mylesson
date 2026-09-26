# 나의 레슨일지 (My Lesson Diary)

현재 안정화 버전: **2.2.6**

## v2.2.6 변경사항
- 새 레슨 체크카드 아이콘 적용
- favicon 16/32px 및 favicon.ico 적용
- iPhone 홈 화면용 180px Apple Touch Icon 적용
- PWA 192/512px 및 maskable 아이콘 적용
- 인라인 Base64 아이콘/manifest를 실제 파일 기반으로 전환
- Service Worker 캐시를 mylesson-v226으로 갱신

## 개발
```bash
python3 tools/audit.py
python3 tools/build.py
```

배포 결과는 `deploy/`에 생성된다. GitHub Pages 루트에는 `deploy`의 파일들을 배치한다.

자세한 구조와 수정 규칙은 `docs/HANDOFF.md`를 참고한다.
