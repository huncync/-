# 남자끼리 하는 말 — 전자책 사전예약 사이트

2030 여성을 위한 전자책 《남자끼리 하는 말》 사전예약 랜딩 페이지입니다.
빌드 과정 없이 `index.html`, `style.css`, `script.js` 세 파일로 동작합니다.

## 미리보기
`index.html`을 브라우저로 열면 됩니다.

## 출시 전 꼭 할 일
1. **사전예약 신청 저장 연결** — 지금은 테스트 모드라 신청 내용이 저장되지 않습니다.
   - https://formspree.io 에서 무료 가입 후 폼을 만들고
   - 발급받은 주소(예: `https://formspree.io/f/abcdwxyz`)를 `script.js` 맨 위 `FORM_ENDPOINT`에 넣으세요.
   - 신청이 들어오면 이메일로 받고 Formspree 대시보드에서 CSV로 내려받을 수 있습니다.
2. **문의 이메일** — `index.html` 하단의 `contact@example.com`을 실제 주소로 바꾸세요.
3. **미리보기 문장·목차·혜택** — 실제 원고 내용에 맞게 수정하세요.

## 무료 배포 (GitHub Pages)
저장소 Settings → Pages → Branch를 `main` / `(root)`로 선택하고 저장하면
몇 분 뒤 `https://<아이디>.github.io/<저장소이름>/` 주소로 공개됩니다.
