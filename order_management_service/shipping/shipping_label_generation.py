"""Shipping Label Generation Implementation"""


import hashlib

def generate_shipping_label(order: dict, carrier: str) -> dict:
    order_id = order.get('order_id', '')
    
    tracking_number = hashlib.md5(f"{order_id}{carrier}".encode()).hexdigest()[:16].upper()
    
    shipping_address = order.get('shipping_address', {})
    
    label_data = {
        'tracking_number': tracking_number,
        'carrier': carrier,
        'recipient': shipping_address.get('name', ''),
        'address': shipping_address.get('street', ''),
        'city': shipping_address.get('city', ''),
        'zip': shipping_address.get('zip', '')
    }
    
    label_size = len(str(label_data))
    
    barcode_strength = len(tracking_number) ** 2
    
    return {
        'success': True,
        'label_data': label_data,
        'tracking_number': tracking_number,
        'label_size': label_size,
        'barcode_strength': barcode_strength
    }

