# 상담 이미지 · 캡션을 작업실(.work/dl)에 맞춰요 (11/23) — kakao_menu.py · kakao_docs.py · render_kakao.js · docs_v2.py · render_docs_v2.js 다음에
# python3 sync_workroom.py → 바뀐 파일 목록을 출력(작업실 publish에 쓰기)
import shutil, os, re, importlib.util as u, hashlib, json
D = os.path.dirname(os.path.abspath(__file__)); W = '/home/user/-/.work/dl/'
def load(name):
    sp = u.spec_from_file_location(name, os.path.join(D, f'{name}.py')); m = u.module_from_spec(sp); sp.loader.exec_module(m); return m
KM, KD = load('kakao_menu'), load('kakao_docs')
changed = []
def put(src, dst, jpg=False):
    dst = W + 'img/' + dst
    old = hashlib.md5(open(dst, 'rb').read()).hexdigest() if os.path.exists(dst) else None
    if jpg:
        from PIL import Image
        Image.open(src).convert('RGB').save(dst, quality=88)
    else:
        shutil.copy(src, dst)
    if hashlib.md5(open(dst, 'rb').read()).hexdigest() != old: changed.append('img/' + os.path.basename(dst))
for i, m in enumerate(KM.MENU, 1): put(f'{D}/kakao_menu/{m[0]}.jpg', f'kkmenu_{i:02d}.jpg')
put(f'{D}/kakao_menu/all.jpg', 'kkall_01.jpg')
for k in ('card_guide', 'card_form', 'card_report'): put(f'{D}/kakao_menu/{k}.jpg', f'{k}_01.jpg')
for k in ('guide', 'form', 'report'): put(f'{D}/kakao_menu/doc_{k}.jpg', f'doc_{k}_01.jpg', jpg=True)
cnt = {}
for k in ('guide', 'form', 'report'):
    fs = sorted([f for f in os.listdir(f'{D}/kakao_news') if f.startswith(k + '_')], key=lambda f: int(f.split('_')[1].split('.')[0])); cnt[k] = len(fs)
    for i, f in enumerate(fs, 1): put(f'{D}/kakao_news/{f}', f'news_{k}_{i:02d}.jpg')
s = open(W + 'index.html', encoding='utf-8').read()
def setcap(key, body):
    global s
    i = s.index(f"key: '{key}'"); a = s.index('caption:\n`', i) + len('caption:\n`'); b = s.index('` },', a)
    s = s[:a] + body.replace('`', '\\`') + s[b:]
for k in ('card_guide', 'card_form', 'card_report'): setcap(k, KD.MSG[k])
setcap('kkall', KM.ALL_MSG)
i = s.index("key: 'kkmenu'"); a = s.index('caption:\n`', i) + len('caption:\n`'); b = s.index('` },', a)
head = s[a:b][:s[a:b].index('━━ 1.')]
s = s[:a] + (head + '\n\n'.join(f'━━ {n}. 메뉴명: {name}\n{msg}' for n, (key, name, _, msg, btn) in enumerate(KM.MENU, 1))).replace('`', '\\`') + s[b:]
for k, n in cnt.items(): s = re.sub(rf"(key: 'news_{k}', tab: 'consult', n: )\d+", lambda m: m.group(1) + str(n), s)
open(W + 'index.html', 'w', encoding='utf-8').write(s)
print(json.dumps({p: W + p for p in changed}, ensure_ascii=False))
