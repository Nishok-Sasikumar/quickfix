import frappe

def get_context(context):
    job_card_name = frappe.form_dict.get("jc")

    if job_card_name and frappe.db.exists("Job Card", job_card_name):
        context.job_card = frappe.get_doc("Job Card", job_card_name)
    else:
        context.job_card = None