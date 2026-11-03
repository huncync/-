// 1:1 남자 심리 분석 신청서 (.docx) — 휴대폰(Word · 한컴오피스)에서 빈칸에 바로 입력하는 서식. node form_docx.js
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  AlignmentType, BorderStyle, VerticalAlign, Footer, PageNumber, HeightRule,
} = require('docx');

const FONT = '맑은 고딕';
const INK = '1D1A16', GOLD = '9A6A1F', SOFT = 'F4EEE3', LINE = 'CDB68A', MUTED = '6F665A';
const W = 10206; // A4 - 여백 0.8인치씩 (11906 - 1700)
const LW = 2700, VW = W - LW;

const r = (text, o = {}) => new TextRun({ text, font: { ascii: FONT, eastAsia: FONT, hAnsi: FONT }, size: o.size || 20, bold: o.bold, color: o.color || INK });
const p = (runs, o = {}) => new Paragraph({ keepNext: o.keep, keepLines: true, children: Array.isArray(runs) ? runs : [runs], spacing: { before: o.before || 0, after: o.after ?? 60, line: o.line || 300 }, alignment: o.align, border: o.border });
const thin = { style: BorderStyle.SINGLE, size: 4, color: LINE };
const borders = { top: thin, bottom: thin, left: thin, right: thin };
const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };

function cell(children, width, o = {}) {
  return new TableCell({
    children: children.length ? children : [p(r(''))], width: { size: width, type: WidthType.DXA }, borders: o.borders || borders,
    shading: o.fill ? { type: ShadingType.CLEAR, color: 'auto', fill: o.fill } : undefined,
    margins: { top: 90, bottom: 90, left: 140, right: 140 }, verticalAlign: o.v || VerticalAlign.CENTER, columnSpan: o.span,
  });
}
// 짧은 칸: 왼쪽 질문 · 오른쪽 빈칸
function field(label, hint, h = 520) {
  return new TableRow({
    cantSplit: true, height: { value: h, rule: HeightRule.ATLEAST },
    children: [
      cell([p(r(label, { bold: true, size: 19 }), { after: hint ? 20 : 0 }), ...(hint ? [p(r(hint, { size: 16, color: MUTED }), { after: 0, line: 260 })] : [])], LW, { fill: SOFT }),
      cell([p(r(''))], VW),
    ],
  });
}
// 긴 칸: 질문 한 줄(위) + 넓은 빈칸(아래)
function longField(label, hints, h) {
  return [
    new TableRow({ cantSplit: true, children: [cell([p(r(label, { bold: true, size: 19 }), { after: hints.length ? 30 : 0, keep: true }), ...hints.map(t => p(r(t, { size: 16, color: MUTED }), { after: 0, line: 260, keep: true }))], W, { fill: SOFT, span: 2 })] }),
    new TableRow({ cantSplit: true, height: { value: h, rule: HeightRule.ATLEAST }, children: [cell([p(r(''))], W, { span: 2, v: VerticalAlign.TOP })] }),
  ];
}
const table = rows => new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [LW, VW], rows });
function section(no, title, note) {
  return [
    p([r(`${no}  `, { bold: true, size: 22, color: GOLD }), r(title, { bold: true, size: 22 })], { keep: true, before: 260, after: note ? 20 : 80, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: INK, space: 4 } } }),
    ...(note ? [p(r(note, { size: 16, color: MUTED }), { after: 80, keep: true })] : []),
  ];
}
const choice = (opts) => opts.map(o => `☐ ${o}`).join('   ');

const doc = new Document({
  styles: { default: { document: { run: { font: { ascii: FONT, eastAsia: FONT, hAnsi: FONT }, size: 20 } } } },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1000, bottom: 1000, left: 850, right: 850 } } },
    footers: { default: new Footer({ children: [p([r('남자들끼리 하는 말 · 1:1 남자 심리 분석   |   카카오채널 「남자가 말하는 남자심리」   |   ', { size: 15, color: MUTED }), new TextRun({ children: [PageNumber.CURRENT], size: 15, color: MUTED, font: FONT })], { align: AlignmentType.CENTER, after: 0 })] }) },
    children: [
      p(r('남자들끼리 하는 말 · @mszexc', { size: 18, color: GOLD, bold: true }), { after: 40 }),
      p(r('1:1 남자 심리 분석 신청서', { size: 40, bold: true }), { after: 40, line: 360 }),
      p(r('그 사람이 왜 그러는지, 이제 뭐라고 보내야 하는지. 남자가 직접 읽고 답해 드립니다.', { size: 19, color: MUTED }), { after: 160, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: GOLD, space: 8 } } }),

      new Table({
        width: { size: W, type: WidthType.DXA }, columnWidths: [W],
        rows: [new TableRow({ children: [cell([
          p(r('작성 안내', { bold: true, size: 19, color: GOLD }), { after: 40 }),
          ...[
            '이 파일의 빈칸에 바로 입력하고 저장한 뒤, 카카오채널 채팅방에 파일로 보내주세요.',
            '선택 항목은 ☐ 를 지우고 ✔ 또는 O 로 바꿔 주세요.',
            '다 못 채워도 괜찮아요. 아는 만큼만 적어주시면 나머지는 제가 여쭤볼게요.',
            '사진 · 카톡 캡처는 신청서를 보낸 다음, 채팅방에 사진으로 이어서 보내주세요.',
            '남자 입장에서 상황을 해석해 드리는 서비스이며, 의료 · 치료 목적의 서비스가 아닙니다.',
          ].map(t => p(r(`·  ${t}`, { size: 17 }), { after: 20, line: 270 })),
        ], W, { fill: SOFT, borders: { top: none, bottom: none, right: none, left: { style: BorderStyle.SINGLE, size: 24, color: GOLD } } })] })],
      }),

      ...section('', '신청 정보'),
      table([
        new TableRow({ height: { value: 520, rule: HeightRule.ATLEAST }, children: [cell([p(r('신청 상품', { bold: true, size: 19 }), { after: 0 })], LW, { fill: SOFT }), cell([p(r(choice(['A · 남자 심리 분석', 'B · 분석 + 대본 ★추천', 'C · 4주 플랜']), { size: 18 }), { after: 0 })], VW)] }),
        field('입금자명', '입금 확인용'),
        field('추가 옵션', '24시간 급행 등 · 없으면 비워두세요'),
      ]),

      ...section('1', '기본 정보'),
      table([
        field('이름', null),
        field('나이 · MBTI', '나 / 그 · MBTI는 모르면 비워두세요'),
        new TableRow({ height: { value: 520, rule: HeightRule.ATLEAST }, children: [cell([p(r('지금 관계', { bold: true, size: 19 }), { after: 0 })], LW, { fill: SOFT }), cell([p(r(choice(['연애 중', '썸', '헤어짐', '재회 고민', '기타 (        )']), { size: 18 }), { after: 0 })], VW)] }),
        field('만난 기간', '헤어졌다면 사귄 기간 + 헤어진 지 얼마나'),
      ]),

      ...section('2', '관상 (선택)', '얼굴 사진은 채팅방에 따로 보내주세요. 부담스러우시면 안 보내셔도 괜찮아요. 관상 없이 이야기와 카톡으로 분석해 드려요.'),
      table([
        new TableRow({ height: { value: 520, rule: HeightRule.ATLEAST }, children: [cell([p(r('보낼 사진', { bold: true, size: 19 }), { after: 0 })], LW, { fill: SOFT }), cell([p(r(choice(['본인 1장', '상대 1~2장', '안 보낼게요']), { size: 18 }), { after: 0 })], VW)] }),
      ]),
      p(r('1년 안에 찍은, 필터 · 보정 없는 정면 사진이면 좋아요. 사진은 분석에만 쓰고 끝나면 바로 삭제합니다.', { size: 16, color: MUTED }), { before: 60, after: 0 }),

      ...section('3', '둘의 이야기'),
      table([
        ...longField('7. 처음 만난 날부터 지금까지, 둘의 이야기를 편하게 적어주세요.', [
          '순서는 상관없고, 모르는 건 빼도 돼요.',
          '· 어디서, 어떻게 만났는지 · 누가 먼저 다가갔고 누가 고백했는지',
          '· 그는 술 · 담배를 하는지, 평소 뭘 좋아하는지 (취미 · 일 · 친구)',
          '· 주로 무엇 때문에 싸웠고, 싸우면 그는 어떻게 하는지',
          '· (헤어졌다면) 누가, 어떤 말로 헤어지자고 했는지',
          '· 지금 연락 상태 (잘 됨 / 뜸함 / 읽고 답 없음 / 차단 / 내가 끊음)',
        ], 3200),
        ...longField('8. 그는 만났을 때와 카톡 · DM 할 때 어떻게 달라요?', ['말투, 표현, 누가 먼저 연락하는지, 답장이 얼마 만에 오는지 · 예전과 지금이 다르면 같이 적어주세요'], 1500),
      ]),

      ...section('4', '지금 고민'),
      table([
        ...longField('9. 지금 제일 고민되는 걸 자세하게 적어주세요.', ['무엇이 걱정되는지, 왜 그런 생각이 드는지 · 길어도 괜찮아요'], 2200),
        ...longField('10. 해석받고 싶은 그의 말이나 행동을 자유롭게 적어주세요.', ['그가 한 말은 들은 그대로 적어주시면 더 정확해요'], 1800),
        ...longField('11. 지금까지 내가 해본 것 (보낸 말 · 행동)과 그의 반응', ['이미 해본 걸 다시 권하지 않으려고 여쭤봐요. 해본 게 없다면 비워두셔도 돼요.'], 1400),
        new TableRow({ height: { value: 520, rule: HeightRule.ATLEAST }, children: [cell([p(r('12. 카톡 캡처', { bold: true, size: 19 }), { after: 0 })], LW, { fill: SOFT }), cell([p(r('최대 10장 · 가장 최근 대화 + 분위기가 바뀐 시점의 대화를 섞어서, 채팅방에 사진으로 보내주세요.', { size: 17, color: MUTED }), { after: 0 })], VW)] }),
      ]),

      ...section('5', '내가 원하는 것'),
      table([
        new TableRow({ height: { value: 620, rule: HeightRule.ATLEAST }, children: [cell([p(r('13. 원하는 방향', { bold: true, size: 19 }), { after: 0 })], LW, { fill: SOFT }), cell([p(r(choice(['재회', '관계 회복', '그의 속마음만 알고 싶음']), { size: 18 }), { after: 30 }), p(r(choice(['깔끔하게 정리', '아직 모르겠음']), { size: 18 }), { after: 0 })], VW)] }),
        ...longField('14. 꼭 답받고 싶은 질문 (1~3개)', [], 1300),
        field('언제까지 답이 필요한가요?', '예: 이번 주말에 만나기로 함 · 급하지 않음'),
      ]),

      ...section('6', '확인 및 개인정보 동의', '각 줄 오른쪽 칸에 "동의"라고 적어주세요.'),
      new Table({
        width: { size: W, type: WidthType.DXA }, columnWidths: [W - 1700, 1700],
        rows: [
          ['(필수) 재회 · 관계 회복 등 원하는 결과를 100% 장담하지 않으며, 결과를 이유로 한 환불은 어렵다는 점을 확인했습니다.'],
          ['(필수) 이름, 나이, 사진, 대화 내용을 분석 목적으로만 수집 · 이용하는 데 동의합니다. 사진은 분석이 끝나면 바로, 나머지 정보는 30일 후 삭제합니다.'],
          ['(선택) 후기를 남겨주시면 이름과 세부 내용을 바꿔서 소개해도 됩니다. (동의 / 비동의)'],
        ].map(([t], i) => new TableRow({ height: { value: 640, rule: HeightRule.ATLEAST }, children: [cell([p(r(`${15 + i}. ${t}`, { size: 17 }), { after: 0, line: 280 })], W - 1700, { fill: SOFT }), cell([p(r(''))], 1700)] })),
      }),
      p(r('작성해 주셔서 고마워요. 자료가 모두 도착한 때부터 72시간 안에 결과물을 보내드려요.', { size: 18, bold: true, color: GOLD }), { before: 240, after: 0, align: AlignmentType.CENTER }),
    ],
  }],
});

Packer.toBuffer(doc).then(b => { fs.writeFileSync(__dirname + '/files/남자심리분석_신청서.docx', b); console.log('ok'); });
