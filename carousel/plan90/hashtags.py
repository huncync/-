# 해시태그 규칙 (10/26): 인스타 5개 제한 → 고정 3개 + 주제 2개.
# 주제 해시태그는 아래 TOPIC 목록 안에서만 고른다 (사실상 통일).
import re
FIXED = ['#남자심리', '#연애심리', '#남자들끼리하는말']
TOPIC = ['#이별', '#재회', '#결혼', '#장기연애', '#권태기', '#썸', '#연락', '#여자심리', '#남자속마음', '#연애고민']
FILL = ['#남자속마음', '#연애고민']

def tags(topics):
    """주제 2개를 받아 5개 해시태그 줄을 만든다. 순서: 고정 2 · 주제 2 · 브랜드."""
    t = [x for x in topics if x in TOPIC][:2]
    for f in FILL:
        if len(t) == 2: break
        if f not in t: t.append(f)
    return ' '.join(FIXED[:2] + t + FIXED[2:])

def fix(caption):
    """캡션 끝의 해시태그 줄을 규칙에 맞게 바꾼다. 기존 태그 중 주제 목록에 있는 것을 우선 쓴다."""
    lines = caption.rstrip('\n').split('\n')
    i = max((k for k, l in enumerate(lines) if l.strip().startswith('#')), default=None)
    if i is None: return caption
    old = re.findall(r'#\S+', lines[i])
    picked = sorted([x for x in old if x in TOPIC], key=TOPIC.index)
    lines[i] = tags(picked)
    return '\n'.join(lines)
