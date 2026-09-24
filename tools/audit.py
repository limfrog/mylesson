#!/usr/bin/env python3
"""Static stability audit for My Lesson Diary v2.2.0."""
from pathlib import Path
import re, subprocess, shutil, sys

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT/'src/app.js').read_text(encoding='utf-8')
TPL = (ROOT/'src/index.template.html').read_text(encoding='utf-8')
CSS = (ROOT/'styles.css').read_text(encoding='utf-8')
SW = (ROOT/'sw.js').read_text(encoding='utf-8')
PRIV = (ROOT/'privacy.html').read_text(encoding='utf-8')
TERMS = (ROOT/'terms.html').read_text(encoding='utf-8')
BUILD = (ROOT/'tools/build.py').read_text(encoding='utf-8')

checks = []
def check(name, ok, detail=''):
    checks.append((name, bool(ok), detail))

check('app version 2.2.0', APP.count('"2.2.0"') >= 2)
check('schema version 3', bool(re.search(r'\bgu\s*=\s*3\b', APP)))
check('single color palette', 'Tm =' not in APP and 'Tm=' not in APP and APP.count('var zm = [') == 1)
check('no native confirm', 'window.confirm' not in APP)
check('no native alert', not re.search(r'(?<![\w.])alert\s*\(', APP))
check('no old window calendar global', 'window.__gcalCleanup' not in APP)
check('no old window lock global', 'window.__requestLockSetup' not in APP)
check('archive excluded from lesson form', 'students: activeStudents' in APP)
check('archive calendar cleanup skip', 'if (S0.archived === true) continue' in APP)
check('archive add-lesson hidden', 'e.archived === true' in APP and 'addLessonBtn' in APP)
check('backup normalization', all(x in APP for x in ['_normBackup','_normStudents','_normLessons','_normFolders']))
check('stable color migration', '_validColor' in APP and 'color: _validColor' in APP)
check('photo IndexedDB storage', all(x in APP for x in ['_photoDB','_saveStudentPhotos','_hydrateStudentPhotos','_studentsForLocal']))
check('structured Drive status messages', '_syncStatus' in APP and 'case "connected"' in APP and 'case "loaded"' in APP)
check('runtime font injection removed', 'fonts.googleapis.com' not in APP)
check('runtime CSS injection removed', 'app-theme-css' not in APP)
check('external stylesheet linked', 'href="./styles.css"' in TPL or "href='./styles.css'" in TPL)
check('zoom accessibility enabled', 'user-scalable=no' not in TPL and 'maximum-scale=1' not in TPL)
check('external service worker registration', "serviceWorker.register('./sw.js'" in TPL)
check('scoped SW cache cleanup', "key.startsWith('mylesson-')" in SW and "CACHE_NAME = 'mylesson-v220'" in SW)
check('SW caches stylesheet', "'./styles.css'" in SW)
check('build copies stylesheet', '"styles.css"' in BUILD)
check('privacy wording updated', '운영자' not in PRIV and '개발자' in PRIV)
check('terms wording updated', '운영자' not in TERMS and '개발자' in TERMS)
check('one spinner keyframe in stylesheet', CSS.count('@keyframes sbaspin') == 1)

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
