import frappe
from frappe.query_builder import DocType
def get_overdue_jobs():
    result = frappe.qb.from_('Job Card').select('name','customer_name','technician','creation')