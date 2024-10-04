from django.core.cache import cache


def increment_failed_attemps_otp(phone_number):
    key = f'failed_attempts_{phone_number}'
    attemps = cache.get(key, 0)
    cache.set(key, attemps + 1, timeout=300)  # ttl 5 minute


def is_blocked(phone_number):
    attemps = cache.get(f'failed_attempts_{phone_number}', 0)
    if attemps >= 5:
        return True
    return False

def send_sms(phone_number):
    print('sms sent')