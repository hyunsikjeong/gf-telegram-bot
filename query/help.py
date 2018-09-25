HELP_MESSAGE = """사용법:
/ㅇㅎ OR /doll - 제조에 걸리는 시간
예) /인형 0022 OR /doll 0022

/ㅈㅂ OR /equip - 제조에 걸리는 시간
예) /장비 0005 OR /equip 0005

/ㄱㅅ OR /search - 인형 이름 OR 별명으로 기본 정보 검색
예) /검색 스프링필드 OR /ㄱㅅ 춘전이

/ㅅㅌ OR /stat - 인형 이름 OR 별명으로 능력치 검색
예) /스탯 스프링필드 OR /ㅅㅌ 춘전이

/ㅂㅍ OR /buff - 인형 이름 OR 별명으로 버프 진형 검색
예) /버프 스프링필드 OR /ㅂㅍ 춘전이

/ㅅㅋ OR /skill - 인형 이름 OR 별명으로 스킬 검색
예) /스킬 스프링필드 OR /ㅅㅋ 춘전이

/ㄱㅈ OR /upgrade - 인형 이름 OR 별명으로 개장 정보 검색
예) /개장 스프링필드 OR /ㄱㅈ 춘전이

/pin, /unpin - 소녀전선 공식 트위터의 새 트윗이 올라오면 알림 받기, 알림 받지 않기 (기본 설정은 알림 받지 않음)

모든 명령어는 / 대신 !의 사용이 가능합니다."""

def help(bot, update):
    update.message.reply_text(HELP_MESSAGE)