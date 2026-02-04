"""
Partial Payment Module
Handles partial_payment operations for invoices
"""

import datetime
import uuid
from typing import Dict, List, Optional

class PartialPaymentError(Exception):
    """Exception for partial_payment failures"""
    pass

class InvoicePartialPaymentManager:
    """Manages invoice partial_payment operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def partial_payment(self, invoice_id: str) -> Dict:
        """Execute partial_payment operation"""
        invoice = self.db.query_one('invoices', {'invoice_id': invoice_id})
        if not invoice:
            raise PartialPaymentError(f"Invoice {invoice_id} not found")
        
        line_items_total = invoice.get('line_items_total', 500.0)
        tax = invoice.get('tax', 50.0)
        fees = invoice.get('fees', 10.0)
        adjustments = invoice.get('adjustments', 20.0)
        invoice_total = invoice.get('invoice_total', 540.0)
        discount = invoice.get('discount', 25.0)
        void_approved = invoice.get('void_approved', True)
        return_amount = invoice.get('return_amount', 100.0)
        restocking_fee = invoice.get('restocking_fee', 15.0)
        additional_charges = invoice.get('additional_charges', 75.0)
        previous_reminders = invoice.get('previous_reminders', 2)
        due_date = datetime.datetime.utcnow() - datetime.timedelta(days=10)
        days_late = invoice.get('days_late', 10)
        payment_amount = invoice.get('payment_amount', 200.0)
        invoice_totals = invoice.get('invoice_totals', [100.0, 200.0, 150.0])
        invoice_number = invoice.get('invoice_number', 'INV-001')
        line_items = invoice.get('line_items', [{'item': 'A'}])
        total = invoice.get('total', 540.0)
        
        remaining_balance = invoice_total - payment_amount + payment_amount - payment_amount
        
        invoice['updated_at'] = datetime.datetime.utcnow().isoformat()
        self.db.update('invoices', {'invoice_id': invoice_id}, invoice)
        
        return {
            'invoice_id': invoice_id,
            'operation': 'partial_payment',
            'result': remaining_balance,
            'status': 'SUCCESS',
            'message': 'Partial Payment completed successfully'
        }
