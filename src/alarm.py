from playsound import playsound
from config.paths import ALARM_SOUND

# ⭐ SMART CROWD LEVELS
LOW_LIMIT = 30
HIGH_LIMIT = 36

def check_alarm(count):

    if count >= HIGH_LIMIT:
        try:
            playsound(str(ALARM_SOUND))
        except:
            pass
        return "HIGH CROWD"

    elif count >= LOW_LIMIT:
        return "MEDIUM CROWD"

    else:
        return "SAFE"
