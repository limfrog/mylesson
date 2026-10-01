#!/usr/bin/env python3
"""Static stability audit for My Lesson Diary v2.5.0."""
from pathlib import Path
import json, re, subprocess, shutil, sys

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT/'src/app.js').read_text(encoding='utf-8')
TPL = (ROOT/'src/index.template.html').read_text(encoding='utf-8')
SW = (ROOT/'sw.js').read_text(encoding='utf-8')
MANIFEST = json.loads((ROOT/'manifest.webmanifest').read_text(encoding='utf-8'))
BUILD = (ROOT/'tools/build.py').read_text(encoding='utf-8')

checks = []
def check(name, ok, detail=''):
    checks.append((name, bool(ok), detail))

check('app version 2.5.0', APP.count('\"2.5.0\"') >= 2)
check('schema version 3', bool(re.search(r'\bgu\s*=\s*3\b', APP)))
check('no native confirm', 'window.confirm' not in APP)
check('no native alert', not re.search(r'(?<![\w.])alert\s*\(', APP))
check('student form save lock', '_savingRef.current' in APP and '저장 중...' in APP)
check('student save handler lock', '_studentSaveLock.current' in APP and 'return false' in APP)
check('backup normalization', all(x in APP for x in ['_normBackup','_normStudents','_normLessons','_normFolders']))
check('local backup includes app settings', all(x in APP for x in ['_normBackupSettings','_collectBackupSettings','settings: _collectBackupSettings()']))
check('local backup restores app settings', '_applyBackupSettings(nd.settings)' in APP and '_importLocal(C.students, C.lessons, C.folders, C.settings)' in APP)
check('local backup legacy compatible', 'settings: _normBackupSettings(v.settings)' in APP)
check('local backup excludes credentials', 'Google 로그인 정보와 앱 잠금 PIN은 포함하지 않습니다.' in APP)
check('photo IndexedDB storage', all(x in APP for x in ['_photoDB','_saveStudentPhotos','_hydrateStudentPhotos','_studentsForLocal']))
check('gcal color source preference', all(x in APP for x in ['gcal_color_source','calColorSource','setCalColorSource']))
check('gcal event color mapping', all(x in APP for x in ['_GCAL_EVENT_COLORS','_nearestGcalColorId','_gcalColorIdForStudent','colorId']))
check('student search includes memo', 'h.memo.includes(U)' in APP)
check('Google startup expiry marks only', 'saved != null && saved.email && !g(saved) && S();' in APP)
check('Google resume expiry marks only', 'document.addEventListener("visibilitychange", resume)' in APP and 'window.addEventListener("pageshow", resume)' in APP and APP.count('saved != null && saved.email && !g(saved) && S();') >= 2)
check('Google no background token request', '_refreshInFlight.current' not in APP and 'function waitForGIS()' not in APP and 'w(saved, true)' not in APP)
check('Google manual token request', 'client.requestAccessToken({ prompt: promptMode })' in APP and 'sameScopes' in APP and 'promptMode = sameScopes ? "" : "select_account"' in APP)
check('Google GIS popup error callback', 'error_callback: (W) =>' in APP and all(x in APP for x in ['popup_failed_to_open','popup_closed','popupBlocked','popupClosed']))
check('Google token expiry timer only marks expired', 'R.current = setTimeout(() => S(), C)' in APP and 'w(k, false)' not in APP)
check('Google token threshold aligned', APP.count('300 * 1e3') >= 2 and '240 * 1e3' not in APP[APP.find('function p1'):APP.find('function sc')])
check('external service worker registration', "serviceWorker.register('./sw.js'" in TPL)
check('external manifest linked', 'href="./manifest.webmanifest"' in TPL)
check('Apple Touch Icon linked', 'href="./apple-touch-icon.png"' in TPL)
check('favicon 16 linked', 'href="./favicon-16x16.png"' in TPL)
check('favicon 32 linked', 'href="./favicon-32x32.png"' in TPL)
check('no embedded Base64 manifest', 'data:application/json;base64' not in TPL)
check('no embedded Base64 head icons', 'data:image/png;base64' not in TPL[:TPL.find('</head>')])
check('SW cache v250', "CACHE_NAME = 'mylesson-v250'" in SW)
check('SW caches manifest', "'./manifest.webmanifest'" in SW)
check('SW caches Apple icon', "'./apple-touch-icon.png'" in SW)
check('manifest standalone', MANIFEST.get('display') == 'standalone')
check('manifest scope', MANIFEST.get('scope') == './')
check('manifest has 192 icon', any(x.get('sizes')=='192x192' for x in MANIFEST.get('icons',[])))
check('manifest has 512 icon', any(x.get('sizes')=='512x512' and x.get('purpose')=='any' for x in MANIFEST.get('icons',[])))
check('manifest has maskable icon', any('maskable' in x.get('purpose','') for x in MANIFEST.get('icons',[])))
check('build copies icon assets', all(x in BUILD for x in ['manifest.webmanifest','apple-touch-icon.png','android-chrome-192x192.png','android-chrome-512x512.png','maskable-icon-512x512.png','favicon.ico']))
check('zoom accessibility enabled', 'user-scalable=no' not in TPL and 'maximum-scale=1' not in TPL)

check('calendar year month picker', all(x in APP for x in ['calendarPickerOpen','pickerYear','pickerMonth','applyYearMonth','연도와 월 선택']))
check('calendar year drum UI', all(x in APP for x in ['yearDrumRef','연도 드럼롤','scrollSnapType: "y mandatory"','scrollTop / 38']))
check('calendar week navigation', all(x in APP for x in ['moveWeek(-1)','moveWeek(1)','이전 주','다음 주','weekLabel']))
check('calendar search button toggle', all(x in APP for x in ['calSearchOpen','setCalSearchOpen','children: l === "ko" ? "검색" : "Search"']))
check('calendar student date search', all(x in APP for x in ['calSearch','searchResults','학생 이름으로 수업일자 검색','maxHeight: 300','overflowY: "auto"']))
check('calendar search includes historical scheduled dates', all(x in APP for x in ['buildStudentDateRows','searchStudents.flatMap(buildStudentDateRows)','if (!C.date || C.date > N) return','if (W > N) return','ee > C && (ee = new Date(C))']))
check('calendar search newest first and no future dates', 'filter((K) => K.date <= N)' in APP and 'sort((A, Y) => Y.date.localeCompare(A.date)' in APP)
check('calendar search fee-paid icon', 'title: l === "ko" ? "수업료 납부" : "Fee paid"' in APP and 'children: "💰"' in APP)
check('calendar student legend removed', 'e.length > 0 && (0, o.jsx)(\"div\", { style: { display: \"flex\", flexWrap: \"wrap\", gap: 8, marginBottom: 12' not in APP)
check('settings dark-mode status cards use theme variables', all(x in APP for x in ['background: \"var(--green-bg)\"', 'background: \"var(--surface2)\"', 'background: \"var(--purple-bg)\"', 'color: \"var(--green-text)\"']))
check('settings toggle labels use theme colors', 'borderBottom: \"1px solid var(--border)\"' in APP and 'fontSize: 14, fontWeight: 700, color: \"var(--text)\"' in APP)
check('lesson content optional label', 'label: i(\"lessonContent\"), value: r.content' in APP and 'label: i(\"lessonContent\") + \" *\"' not in APP)
check('lesson content optional save', 'disabled: !r.studentId, children: i(\"save\")' in APP and '!r.content.trim()' not in APP)
check('empty lesson content hidden in card', 'e.content && (0, o.jsx)(Vt, { title: r(\"lessonContent\"), text: e.content })' in APP)

check('calendar print button', all(x in APP for x in ['printCalendar','월간 캘린더 인쇄','주간 캘린더 인쇄','children: l === "ko" ? "인쇄" : "Print"']))
check('calendar monthly PDF landscape', all(x in APP for x in ['_calendarMonthPdfPage','841.89, 595.28','entries.slice(0, 10)','_pdfBlobFromPages']))
check('calendar monthly print time sort', '_calendarPrintEntries' in APP and 'zTimeMin(a0.time) - zTimeMin(b0.time)' in APP)
check('calendar weekly PDF 7-column landscape', all(x in APP for x in ['_calendarWeekPdfPages','colW = usableW / 7','entriesByDay','rowsPerPage','item.time ||','item.student.name','_pdfCanvasPage(canvas, 841.89, 595.28)']))
check('calendar PDF MIME', all(x in APP for x in ['type: "application/pdf"','new Blob([_pdfJoin(chunks)], { type: "application/pdf" })','.pdf`']))
check('calendar iOS PDF share path', all(x in APP for x in ['_calendarPrintDevice','navigator.share','navigator.canShare','new File([doc.blob]','iOS 공유 메뉴에서 ‘프린트’를 선택하세요.']))
check('calendar desktop PDF preview', all(x in APP for x in ['_openCalendarPdf','URL.createObjectURL(doc.blob)','window.open(url, "_blank")']))
check('calendar HTML share removed', 'text/html;charset=utf-8' not in APP and 'new File([doc.html]' not in APP)
check('weekly PDF standard font weights', 'Math.round(7.2 * dpi / 72), 650)' not in APP and 'Math.round(9.0 * dpi / 72), 750)' not in APP)

# v2.5.0 data-safety hardening
check('recovery IndexedDB store', all(x in APP for x in ['_RECOVERY_DB = "mylesson_recovery_v1"','_RECOVERY_STORE = "snapshots"','_RECOVERY_LIMIT = 10','_recoveryDB','_saveRecoverySnapshot','_listRecoverySnapshots']))
check('snapshot before whole-data replacement', 'before_cloud_replace' in APP and 'before_replace' in APP and 'if (!options.skipSnapshot) await _saveRecoverySnapshot' in APP)
check('manual recovery UI', all(x in APP for x in ['데이터 안전','지금 복구본 만들기','restoreRecovery','recoveryItems.slice(0, 5)']))
check('corrupt local data detection and recovery', all(x in APP for x in ['_localDataCorrupt = false','_readLocalArray','_latestRecoverySnapshot','손상된 로컬 데이터 대신 최근 안전 복구본을 복원했습니다.']))
check('critical local writes are guarded', all(x in APP for x in ['_safeStoreJSON("students"','_safeStoreJSON("lessons"','_safeStoreJSON("student_folders"','local_storage_error']))
check('persistent storage request and estimate', all(x in APP for x in ['navigator.storage.persisted','navigator.storage.persist','navigator.storage.estimate','_storageHealth(true)']))
check('device and sync metadata', all(x in APP for x in ['_DEVICE_ID_KEY','_DATA_META_KEY','_deviceId()','_nextCloudMeta','syncMeta']))
check('dirty data tracking', all(x in APP for x in ['_DATA_DIRTY_KEY','_setDataDirty(true)','_setDataDirty(false)','_isDataDirty()']))
check('Drive conflict protection', all(x in APP for x in ['_CLOUD_SEEN_KEY','remoteMeta.updatedAt !== lastSeen','r("conflict")','_syncStatus("conflict"']))
check('explicit force overwrite only', 'p(m, f, b, true)' in APP and 'F(k, C, K, false)' in APP)
check('force overwrite preserves remote recovery', 'cloud_before_force_overwrite' in APP and 'students: remote.students' in APP)
check('cloud loads mark seen and are snapshot-safe', APP.count('_markCloudSeen(') >= 4 and APP.count('{ source: "cloud" }') >= 3)
check('new Drive file keeps current local data', 'students: [], lessons: [], folders: []' not in APP[APP.find('function p1'):APP.find('function sc')])
check('Drive file contains revision metadata', 'syncMeta: initMeta' in APP and 'syncMeta }, _ = await Wn.writeFile' in APP)
check('SW activation is not forced during install', "self.addEventListener('message'" in SW and "event.data.type === 'SKIP_WAITING'" in SW and 'cache.addAll(APP_SHELL)).catch' not in SW)
check('SW cache write uses waitUntil', 'event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.put(req, copy)))' in SW and 'event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.put(req, res.clone())))' in SW)
check('privacy login scope wording corrected', '기본 기능은 로그인 없이 사용할 수 있으며' in (ROOT/'privacy.html').read_text(encoding='utf-8') and 'localStorage 및 IndexedDB' in (ROOT/'privacy.html').read_text(encoding='utf-8'))
check('privacy dark mode and close preserved', all(x in (ROOT/'privacy.html').read_text(encoding='utf-8') for x in ['app_theme_dark','data-theme','닫기']))
check('build version 2.5.0', 'v2.5.0 build' in BUILD and 'app version 2.5.0 missing' in BUILD)

for fn in ['favicon.ico','favicon-16x16.png','favicon-32x32.png','apple-touch-icon.png','android-chrome-192x192.png','android-chrome-512x512.png','maskable-icon-512x512.png','icon-1024x1024.png','logo.png']:
    check('asset exists: '+fn, (ROOT/fn).exists())

node = shutil.which('node')
if node:
    for path in [ROOT/'src/app.js', ROOT/'sw.js']:
        r = subprocess.run([node,'--check',str(path)],capture_output=True,text=True)
        check(f'node syntax: {path.name}', r.returncode == 0, r.stderr.strip())
else:
    check('node available', False, 'Node.js not installed; syntax check skipped')

fails = [x for x in checks if not x[1]]
for name, ok, detail in checks:
    print(('PASS' if ok else 'FAIL') + ': ' + name + (f' — {detail}' if detail else ''))
print(f'\n{len(checks)-len(fails)}/{len(checks)} checks passed')
if fails:
    sys.exit(1)
