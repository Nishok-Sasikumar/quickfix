import frappe
from frappe.utils import now_datetime
def log_change(doc,method):
    if doc.doctype == "Audit Log":
        return
    log = frappe.new_doc("Audit Log")
    log.doctype_name = doc.doctype
    log.document_name = doc.name
    log.action=method
    log.user=frappe.session.user
    log.timestamp=now_datetime
    log.insert(ignore_permissions=True)