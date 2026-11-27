# R{n}.py의 R을 읽어 R{n}_script.md를 만들어요
import ast, sys
def md(n, when):
    R = ast.literal_eval(open(f'R{n}.py', encoding='utf-8').read()[4:])
    out = [f"# 릴스 R{n} · {when} 「{R['title']}」\n", f"상단 텍스트: {' / '.join(R['top'])}  ", f"작은 글씨: {R['label']}  ", f"길이: {R['len']}  ", "틀: 11/18 새 틀 (후킹 → 포모 → 번역 → 해결 · 나도 할 수 있겠다 → 결과 신호 → 끝 멘트)\n", '## 대본\n']
    for a, b, c, d in R['script']:
        out.append(f'**{a} · {b}**\n'); out.append('  \n'.join(c.split('\n')) + '\n')
        if d: out.append(f'_{d}_\n')
    out += ['## 촬영 메모\n', '\n'.join('- ' + s for s in R['shoot']) + '\n', '## 캡션\n', '```\n' + R['caption'] + '\n```\n', '## 고정 댓글\n', '```\n' + R['pin'] + '\n```\n']
    open(f'R{n}_script.md', 'w', encoding='utf-8').write('\n'.join(out))
if __name__ == '__main__':
    md(sys.argv[1], sys.argv[2])
