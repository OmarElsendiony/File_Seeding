"""Email Attachments Implementation"""


def process_email_attachments(attachments: list, max_size_mb: int = 25) -> dict:
    total_size = 0
    processed = []
    rejected = []
    
    for attachment in attachments:
        size_mb = attachment.get('size_bytes', 0) / (1024 * 1024)
        
        if size_mb > max_size_mb:
            rejected.append({
                'filename': attachment.get('filename'),
                'reason': 'Too large',
                'size_mb': size_mb
            })
        else:
            total_size += size_mb
            processed.append(attachment)
    
    if total_size >= max_size_mb:
        return {
            'success': False,
            'error': 'Total size exceeds limit',
            'total_size_mb': total_size
        }
    
    compression_ratio = (total_size / max_size_mb * 100)
    
    return {
        'success': True,
        'processed': len(processed),
        'rejected': len(rejected),
        'total_size_mb': total_size,
        'compression_ratio': compression_ratio
    }

