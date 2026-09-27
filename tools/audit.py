#!/usr/bin/env python3
"""Static stability audit for My Lesson Diary v2.2.8."""
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

check('app version 2.2.8', APP.count('"2.2.8"') >= 2)
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
check('Google startup auto reconnect', 'saved != null && saved.email && !g(saved) && w(saved, true)' in APP)
check('Google resume auto reconnect', 'document.addEventListener("visibilitychange", resume)' in APP and 'window.addEventListener("pageshow", resume)' in APP)
check('Google GIS load wait', 'function waitForGIS()' in APP and '++tries >= 40' in APP and 'setTimeout(tick, 150)' in APP)
check('Google refresh deduplicated', '_refreshInFlight.current' in APP and 'if (_refreshInFlight.current) return _refreshInFlight.current' in APP)
check('Google refresh does not require old token', 'if (!(k != null && k.email)) return Promise.resolve(false)' in APP)
check('Google token threshold aligned', APP.count('300 * 1e3') >= 2 and '240 * 1e3' not in APP[APP.find('function p1'):APP.find('function sc')])
check('Google reconnect status messages', all(x in APP for x in ['"reconnecting"','"reconnected"','Google 연결 자동 복원 중','Google 연결 자동 복원 완료']))
check('external service worker registration', "serviceWorker.register('./sw.js'" in TPL)
check('external manifest linked', 'href="./manifest.webmanifest"' in TPL)
check('Apple Touch Icon linked', 'href="./apple-touch-icon.png"' in TPL)
check('favicon 16 linked', 'href="./favicon-16x16.png"' in TPL)
check('favicon 32 linked', 'href="./favicon-32x32.png"' in TPL)
check('no embedded Base64 manifest', 'data:application/json;base64' not in TPL)
check('no embedded Base64 head icons', 'data:image/png;base64' not in TPL[:TPL.find('</head>')])
check('SW cache v228', "CACHE_NAME = 'mylesson-v228'" in SW)
check('SW caches manifest', "'./manifest.webmanifest'" in SW)
check('SW caches Apple icon', "'./apple-touch-icon.png'" in SW)
check('manifest standalone', MANIFEST.get('display') == 'standalone')
check('manifest scope', MANIFEST.get('scope') == './')
check('manifest has 192 icon', any(x.get('sizes')=='192x192' for x in MANIFEST.get('icons',[])))
check('manifest has 512 icon', any(x.get('sizes')=='512x512' and x.get('purpose')=='any' for x in MANIFEST.get('icons',[])))
check('manifest has maskable icon', any('maskable' in x.get('purpose','') for x in MANIFEST.get('icons',[])))
check('build copies icon assets', all(x in BUILD for x in ['manifest.webmanifest','apple-touch-icon.png','android-chrome-192x192.png','android-chrome-512x512.png','maskable-icon-512x512.png','favicon.ico']))
check('zoom accessibility enabled', 'user-scalable=no' not in TPL and 'maximum-scale=1' not in TPL)

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
