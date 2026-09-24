import frappe
from frappe.utils import today,now_datetime
def check_low_stock():
    prev= frappe.db.get_value("Audit Log",{"action":"low_stock_check","document_name":today()},"name")
    if prev:
        return
    s= frappe.get_single("QuickFix Settings")
    if not s.low_stock_alert_enabled:
        return
    low_stock_p =frappe.get_all("Spare Part",filters={"is_active":1},fields=["name","part_name","stock_qty","reorder_level"])
    low_parts=[]
    for p in low_stock_p:
        if p.stock_qty <=p.reorder_level:
            low_parts.append(p)
    if low_parts:
        msg="The following part qty is low <br>"
        for p in low_parts:
            msg=msg + p.part_name+"-Qty:"+ str(p.stock_qty)+ "<br>"
        frappe.sendmail(recipients=[s.manager_email],subject="Low stocks",message=msg,delayed=False)
    l=frappe.new_doc("Audit Log")
    l.doctype_name="Spare Part"
    l.document_name=today()
    l.action="low_stock_check"
    l.user="Administrator"
    l.timestamp=now_datetime()
    l.insert(ignore_permissions=True)
