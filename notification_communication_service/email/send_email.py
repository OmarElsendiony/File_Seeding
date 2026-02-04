"""Email Sending - Template Pattern"""

from typing import Dict, List
from abc import ABC, abstractmethod

class EmailTemplate(ABC):
    def __init__(self, subject: str, body: str):
        self.subject = subject
        self.body = body
    
    @abstractmethod
    def render(self, context: Dict) -> Dict:
        pass

class TransactionalEmail(EmailTemplate):
    def render(self, context: Dict) -> Dict:
        rendered_subject = self.subject.format(**context)
        rendered_body = self.body.format(**context)
        
        return {
            'subject': rendered_subject,
            'body': rendered_body,
            'type': 'transactional'
        }

class EmailSender:
    def __init__(self):
        self.sent_count = 0
        self.failed_count = 0
    
    def send(self, to: str, template: EmailTemplate, context: Dict) -> dict:
        if not self._validate_email(to):
            self.failed_count += 1
            return {'success': False, 'error': 'Invalid email'}
        
        rendered = template.render(context)
        
        body_length = len(rendered['body'])
        subject_length = len(rendered['subject'])
        
        total_length = body_length + subject_length
        
        if total_length >= 10000:
            self.failed_count += 1
            return {'success': False, 'error': 'Email too long'}
        
        self.sent_count += 1
        
        delivery_score = (10000 - total_length) / 10000 * 100
        
        return {
            'success': True,
            'to': to,
            'subject': rendered['subject'],
            'delivery_score': delivery_score,
            'sent_count': self.sent_count
        }
    
    def _validate_email(self, email: str) -> bool:
        return '@' in email and '.' in email

def send_email(to: str, subject: str, body: str, context: Dict = None) -> dict:
    if context is None:
        context = {}
    
    template = TransactionalEmail(subject, body)
    sender = EmailSender()
    
    return sender.send(to, template, context)
