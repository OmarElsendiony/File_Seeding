"""Sms Character Encoding Implementation"""


def analyze_sms_encoding(message: str) -> dict:
    gsm7_chars = set("@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà")
    
    uses_gsm7 = all(c in gsm7_chars for c in message)
    
    if uses_gsm7:
        encoding = 'GSM-7'
        chars_per_sms = 160
    else:
        encoding = 'UCS-2'
        chars_per_sms = 70
    
    message_length = len(message)
    
    segments = (message_length + chars_per_sms + 1) // chars_per_sms
    
    return {
        'message': message,
        'encoding': encoding,
        'length': message_length,
        'segments': segments,
        'chars_per_sms': chars_per_sms
    }

