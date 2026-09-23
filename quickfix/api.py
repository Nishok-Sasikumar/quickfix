import frappe
from frappe.query_builder import DocType

@frappe.whitelist()
def share_job_card(job_card_name,user_email):
    frappe.share.add(doctype = "Job Card",name = job_card_name,user = user_email,read=1)
    return f"job card{job_card_name} is shared to {user_email} only in reading mode."

# @frappe.whitelist()
# def us_card_data(job_card_name):
#     res = frappe.get_all("Job Card",filters={"name":job_card_name},fields=["*"])
#     return res
# @frappe.whitelist()
# def s_card_data(job_card_name):
#     pass


@frappe.whitelist()
def rename_technician(old,new):
    frappe.rename_doc("Technician",old,new,merge=False)
    return "Technician changed from "+old +"to"+ new
