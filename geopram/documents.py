"""Document data validation helpers."""
from datetime import date
def validate_invoice(data):
    if not data.get("customer_name") and not data.get("student_name"): raise ValueError("Customer or student name is required")
    amount=float(data.get("amount",0))
    if amount < 0: raise ValueError("Amount cannot be negative")
    return {**data,"amount":round(amount,2),"currency":data.get("currency","KES"),"document_type":"receipt"}
def validate_certificate(data):
    if not (data.get("recipient_name") or data.get("student_name")): raise ValueError("Recipient name is required")
    if not (data.get("course_name") or data.get("program")): raise ValueError("Course or programme is required")
    return {**data,"issue_date":data.get("issue_date",date.today().isoformat())}
