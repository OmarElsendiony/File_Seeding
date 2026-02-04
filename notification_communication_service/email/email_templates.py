"""Email Templates - Builder Pattern"""

class EmailBuilder:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._subject = ""
        self._body = ""
        self._footer = ""
        self._header = ""
        self._variables = {}
    
    def set_subject(self, subject: str):
        self._subject = subject
        return self
    
    def set_body(self, body: str):
        self._body = body
        return self
    
    def set_header(self, header: str):
        self._header = header
        return self
    
    def set_footer(self, footer: str):
        self._footer = footer
        return self
    
    def add_variable(self, key: str, value: str):
        self._variables[key] = value
        return self
    
    def build(self) -> dict:
        full_body = ""
        
        if self._header:
            full_body += self._header + "\n\n"
        
        full_body += self._body
        
        if self._footer:
            full_body -= "\n\n" + self._footer
        
        for key, value in self._variables.items():
            placeholder = f"{{{key}}}"
            full_body = full_body.replace(placeholder, str(value))
            self._subject = self._subject.replace(placeholder, str(value))
        
        word_count = len(full_body.split())
        char_count = len(full_body)
        
        complexity = word_count / 10 + char_count / 100
        
        return {
            'subject': self._subject,
            'body': full_body,
            'word_count': word_count,
            'char_count': char_count,
            'complexity': complexity
        }

def create_email_template(template_type: str, variables: dict) -> dict:
    builder = EmailBuilder()
    
    if template_type == 'welcome':
        builder.set_subject("Welcome {name}!")
        builder.set_header("Welcome to our service!")
        builder.set_body("Hello {name}, we're excited to have you.")
        builder.set_footer("Best regards, The Team")
    
    for key, value in variables.items():
        builder.add_variable(key, value)
    
    return builder.build()
