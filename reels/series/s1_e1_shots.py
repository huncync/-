# 헤어진 남자의 1년 · EP.1 「헤어진 첫날 밤, 남자 머릿속」 — 힉스필드 장면 목록 (11/15)
# 실사(지훈님) 3컷 + AI 9컷 · 목소리는 전부 지훈님 녹음 · AI 컷은 대사 없이(립싱크 X) 내레이션 + 자막
# 프롬프트는 영어(모델이 더 정확해요) · 한국어 설명은 확인용

STYLE = ('cinematic, shot on 35mm, vertical 9:16, night, low light, muted teal shadows with one warm lamp, '
         'soft film grain, shallow depth of field, realistic, quiet and lonely mood, '
         'no text, no logos, no brand names, no watermark')

CHAR = ('A 32-year-old Korean man, ordinary office worker, short black hair slightly messy, clean-shaven, '
        'tired eyes, slim build, wearing a charcoal grey hoodie over a white t-shirt, '
        'natural skin texture, not resembling any celebrity')

CHAR_SHEET = (f'Character reference sheet. {CHAR}. Front view, three-quarter view and side profile, '
              'neutral expression, plain dark grey background, soft studio light, photorealistic.')

ROOM = 'a small one-room apartment in Seoul at night, grey bedding, one warm desk lamp, window with distant city lights'

# (번호, 시간, 구분, 대본, 장면(한국어), 프롬프트, 카메라, 길이, 편집 메모)
SHOTS = [
 ('S1', '0~4초', '실사', '헤어지자고 먼저 말한 남자, 그날 밤 진짜 괜찮을까요?',
  '지훈님 정면 · 밤 차 안 (8화 내내 같은 장소 · 같은 옷)', '', '고정', '4초',
  '상단 자막 "사귄 지 2년. 오늘 저녁, 그가 먼저 헤어지자고 했어요." · 인사 없이 바로'),
 ('S2', '4~8초', 'AI', '그녀의 마지막 메시지는 이거였어요.',
  '퇴근길 주차장, 시동을 안 건 차 안. 운전석의 그, 휴대폰 불빛이 얼굴에.',
  f'{CHAR}, sitting still in the driver seat of a parked car in a dark underground parking lot, engine off, '
  'his face lit only by the cold glow of a phone screen below frame, he stares without blinking. ' + STYLE,
  '천천히 다가가기 (slow push-in)', '5초 생성 → 4초 사용', ''),
 ('S3', '8~12초', 'AI + 그래픽', '"알겠어. 잘 지내." 그는 읽고, 답하지 않았어요.',
  '휴대폰 화면 클로즈업. 엄지가 화면 위에서 멈춰 있어요. (화면은 비워 두고 카톡 그래픽을 얹어요)',
  'Extreme close-up of a man\'s hand holding a smartphone in a dark car, the screen is blank glowing white, '
  'his thumb hovers above the screen and does not move. ' + STYLE,
  '고정 (static macro)', '5초 → 4초', '카톡 그래픽 얹기: 그녀 "알겠어. 잘 지내." · 오후 9:47 · 읽음'),
 ('S4', '12~22초', 'AI + 그래픽', '밤 10시. 남자는 이상하게 홀가분해요. "이제 싸울 일은 없겠다." 친구한테 한 줄 보내요. "나 헤어졌다."',
  '원룸 소파. 캔맥주를 따고 어깨 힘을 빼며 기대는 그. 살짝 웃었다가 휴대폰을 들어 짧게 입력.',
  f'{CHAR}, in {ROOM}, slumps back on a small sofa and opens a can of beer, his shoulders drop and he lets out a long breath, '
  'a faint relieved half-smile, then he picks up his phone and types a short message. ' + STYLE,
  '살짝 손떨림 (handheld, subtle)', '10초 생성(또는 5초 × 2) → 9초', '왼쪽 위 작은 자막 "밤 10시" · 마지막에 "나 헤어졌다" 말풍선 그래픽 · 금색 강조: 홀가분해요'),
 ('S5', '22~28초', 'AI', '밤 12시. 집이 너무 조용해요.',
  '불 끈 방. 침대에 누워 천장을 보는 그. 휴대폰 불빛만.',
  f'{CHAR}, lying on his back in bed in {ROOM} with the lamp now off, staring at the ceiling, '
  'the only light is a phone resting on his chest, total silence, the room feels too big. ' + STYLE,
  '위에서 천천히 내려오기 (slow top-down drift)', '5초 → 5초', '왼쪽 위 "밤 12시"'),
 ('S6', '28~33초', 'AI + 그래픽', '습관처럼 "잘 자"를 치다가 멈춰요. 엄지가 아직 기억하는 거예요.',
  '입력창 위 엄지 클로즈업. 두 글자를 치다가 멈추고, 천천히 지워요.',
  'Macro close-up of a thumb typing on a smartphone keyboard in a dark bedroom, it types two letters, '
  'pauses, then slowly presses delete, screen glow on the bedsheet. ' + STYLE,
  '고정 (static macro)', '5초 → 5초', '"잘 자" 쓰다 지우기 그래픽 · 금색 강조: 엄지가 먼저 기억해요'),
 ('S7', '33~38초', 'AI', '새벽 2시. 그녀 프로필을 눌러봐요.',
  '옆으로 누워 화면을 내리는 그. 푸른 화면 빛. 협탁 위 디지털 시계 2:00.',
  f'{CHAR}, lying on his side in bed in the dark, scrolling slowly on his phone, blue screen light on his face, '
  'a plain digital clock on the nightstand shows 2:00, his eyes are restless. ' + STYLE,
  '천천히 다가가기 (slow dolly-in)', '5초 → 5초', '왼쪽 위 "새벽 2시" · 시계 숫자가 이상하면 시계를 화면 밖으로'),
 ('S8', '38~43초', 'AI', '사진이 그대로면 안심하고, 바뀌었으면 괜히 화가 나요. 헤어지자고 한 건 자기면서요.',
  '휴대폰을 침대에 엎어 놓고 팔로 눈을 가리는 그.',
  f'{CHAR}, in bed in the dark, abruptly turns his phone face down on the mattress and covers his eyes with his forearm, '
  'frustrated with himself, the room goes darker. ' + STYLE,
  '고정 (static)', '5초 → 5초', ''),
 ('S9', '43~50초', 'AI', '다음 날 친구가 물어요. "괜찮냐?" "어. 오히려 편해."',
  '다음 날 낮, 회사 근처 편의점 앞. 친구(뒷모습)와 서서 커피를 든 그, 어색하게 웃어요.',
  f'Daytime, overcast. {CHAR}, now in a navy coat, standing outside a convenience store holding a paper coffee cup, '
  'talking with a friend seen only from behind, he forces a casual smile and shrugs, '
  'cinematic, shot on 35mm, vertical 9:16, natural daylight, muted colors, shallow depth of field, '
  'no text, no logos, no store signs, no brand names',
  '살짝 손떨림 (handheld medium shot)', '5초 × 2 → 7초', '입 모양 맞추지 않기 · 자막만: 친구 "괜찮냐?" / 그 "어. 오히려 편해." · 간판이 생기면 다시 만들기(모자이크 X)'),
 ('S10', '50~57초', '실사', '그런데 이건 후회가 아니에요. 빈자리예요. 그래서 이 밤에 보내는 연락은 그의 결심만 굳혀요. 오늘은 아무것도 보내지 마세요.',
  '지훈님 정면 · S1과 같은 차 안', '', '고정', '7초', '조언은 지훈님 얼굴로 (신뢰) · 금색 강조: 후회가 아니라, 빈자리'),
 ('S11', '57~60초', 'AI', '일주일 뒤, 그는 모두에게 이렇게 말하기 시작해요. "나 진짜 괜찮아."',
  '아침, 엘리베이터 거울 앞. 표정을 정리하고 넥타이를 고쳐 매는 그. (EP.2 예고)',
  f'Morning. {CHAR}, now in a white shirt and dark tie, standing alone in a stainless steel elevator, '
  'looking at his reflection, he straightens his tie and practices a neutral, okay expression. '
  'cinematic, shot on 35mm, vertical 9:16, cool fluorescent light, soft film grain, no text, no logos',
  '천천히 다가가기 (slow push-in)', '5초 → 3초', '목소리 낮게 · 한 박자 쉬고'),
 ('S12', '60~65초', '실사', '남자가 하는 말이랑 행동, 남자 입장에서 매일 번역해서 올려요. 놓치기 싫으면 팔로우해두세요.',
  '지훈님 정면 · 같은 차 안', '', '고정', '5초', '마지막 2초 멈춤 · 이 줄은 빼지 말기'),
]

TIPS = [
 ('인물 먼저 고정', '「인물 기준 사진」 프롬프트로 그의 얼굴을 한 번 만들고, 마음에 드는 1장을 Soul ID(인물 고정)로 저장해요. 모든 AI 컷에서 이 인물을 불러와야 8화 내내 같은 얼굴이 돼요.'),
 ('사진 → 영상 순서', '컷마다 먼저 이미지를 만들고(구도 · 조명 확인), 마음에 들면 그 이미지로 영상을 만들어요. 바로 영상을 만들면 얼굴이 흔들리고 크레딧이 더 들어요.'),
 ('컷당 5초 · 2~3번까지만', '한 컷에 3번 넘게 다시 만들지 않기. 손가락 · 글자 · 시계 숫자가 이상하면 그 부분을 화면 밖으로 빼거나 그래픽으로 덮어요.'),
 ('입 모양은 쓰지 않기', 'AI 컷은 대사 없이, 지훈님 내레이션 + 자막으로. 립싱크는 어색함이 바로 보여요.'),
 ('색 맞추기', '편집에서 AI 컷과 실사 컷에 같은 필터(살짝 어둡게 · 청록 그림자 · 필름 그레인)를 씌워 한 영상처럼 보이게 해요.'),
 ('올릴 때', '게시 화면에서 「AI 정보」 라벨을 켜요. 캡션 첫 줄 "[헤어진 남자의 1년 · EP.1] 흔히 있는 이별을 한 커플로 재구성했어요."는 그대로 둬요.'),
]
DONT = ['그의 얼굴을 지훈님이나 유명인과 닮게 만들기', '그녀의 얼굴을 정면으로 보여주기 (EP.1은 그의 시점 · 실제 사람처럼 보일 위험)', '화면 속 카톡 글자를 AI로 만들기 (글자가 깨져요 → 그래픽으로)', '간판 · 로고 · 차 번호판이 크게 보이는 컷 (모자이크 대신 다시 만들기)']
