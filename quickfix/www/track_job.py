import frappe
def get_context(c):
    c.no_cache=1
    jcn=frappe.form_dict.get("jc")
    if not jcn:
        c.job_card=None
        return c
    if not frappe.db.exists("Job Card",jcn):
        c.job_card=None
        return c
    doc=frappe.get_doc("Job Card",jcn)
    c.job_card =doc
    return c