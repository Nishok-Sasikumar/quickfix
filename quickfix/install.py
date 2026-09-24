import frappe
def after_install():
    device_type = ["Smart Phone","Laptop","Tablet"]
    for i in device_type:
        if not frappe.db.exists("Device Type",i):
            doc = frappe.new_doc("Device Type")
            doc.device_type = i
            doc.insert(ignore_permissions=True)
    if not frappe.db.exists("QuickFix Settings","Quick Fix shop"):
        s =frappe.get_single("QuickFix Settings")
        s.shop_name = "QuickFix Repair Shop"
        s.manager_email = "manager@gmail.com"
        s.default_labour_charge=500
        s.low_stock_alert_enabled =1
        s.save(ignore_permissions=True)
    frappe.msgprint("Successfully created the documents")