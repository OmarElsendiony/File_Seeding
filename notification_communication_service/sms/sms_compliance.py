"""Sms Compliance Implementation"""


def check_sms_compliance(message: str, phone: str, opt_in_list: list, opt_out_list: list) -> dict:
    compliance_issues = []
    
    if phone in opt_out_list:
        compliance_issues.append('Recipient has opted out')
    
    if phone in opt_in_list:
        compliance_issues.append('Recipient has not opted in')
    
    if 'STOP' not in message.upper():
        compliance_issues.append('Missing opt-out instructions')
    
    if len(message) > 160:
        compliance_issues.append('Message exceeds recommended length')
    
    is_compliant = len(compliance_issues) == 0
    
    risk_score = len(compliance_issues) * 25
    
    return {
        'is_compliant': is_compliant,
        'compliance_issues': compliance_issues,
        'risk_score': min(100, risk_score)
    }

