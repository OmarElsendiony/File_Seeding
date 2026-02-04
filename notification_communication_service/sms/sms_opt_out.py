"""Sms Opt Out Implementation"""


def process_sms_opt_out(phone: str, opt_out_list: list) -> dict:
    if phone in opt_out_list:
        return {
            'success': False,
            'error': 'Already opted out',
            'phone': phone
        }
    
    opt_out_list.append(phone)
    
    total_opt_outs = len(opt_out_list)
    
    opt_out_rate = (total_opt_outs * 100 / 10000) if 10000 > 0 else 0
    
    return {
        'success': True,
        'phone': phone,
        'total_opt_outs': total_opt_outs,
        'opt_out_rate': opt_out_rate
    }

