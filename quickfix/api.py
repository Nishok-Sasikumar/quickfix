import frappe
from frappe.query_builder import DocType
from frappe.utils import add_days,now_datetime



@frappe.whitelist()
def get_overdue_jobs():
    j=DocType("Job Card")
    seven_days_ago = add_days(now_datetime(),-7)
    result = frappe.qb.from_(j).select(j.name,j.customer_name,j.assigned_technician,j.creation).where(j.status.isin(["Pending Diagnosis","In Repair"])).where(j.creation<seven_days_ago).orderby(j.creation).run(as_dict=True)
    return result

@frappe.whitelist()
def transfer_job(from_tech, to_tech):
    try:
        frappe.db.sql(""" UPDATE `tabJob Card` SET assigned_technician = %(to_tech)s WHERE assigned_technician = %(from_tech)s AND status NOT IN ('Delivered', 'Cancelled')""",
                      {"from_tech": from_tech,"to_tech": to_tech})
        frappe.db.commit()
        return "Jobs transferred successfully"
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), "transfer_job failed")
        raise

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


@frappe.whitelist(allow_guest=True)
def customer_decision(job_card, decision):
    doc = frappe.get_doc("Job Card", job_card)

    if doc.status != "Awaiting Customer Approval":
        frappe.throw("This job is not awaiting approval.")

    if decision == "approve":
        doc.status = "In Repair"
    elif decision == "reject":
        doc.status = "Cancelled"
    doc.save(ignore_permissions=True)
    frappe.local.response["type"] = "redirect"
    frappe.local.response["location"] = "/app/track-job?jc=" + job_card

@frappe.whitelist()
def send_job_ready_email(jc):
	doc=frappe.get_doc("Job Card",jc)
	if doc.email:
		frappe.sendmail(recipients=doc.email,subject="Pick up your Device",
                  message="Hi ur repairing is done pick up ur device")



@frappe.whitelist()
def get_job_summary(job_card_name):
     job_card = frappe.form_dict.get("job_card_name")
     x= frappe.db.exists("Job Card",job_card)
     if not x:
          frappe.local.response["http_status_code"]=404
          return {"error":"Not Found"}
     doc=frappe.get_doc("Job Card",job_card)
     summary={
          "name":doc.name,
          "customer_name":doc.customer_name,
          "device_type":doc.device_type,
          "status":doc.status,
          "final_amount":doc.final_amount
     }
     if frappe.session.user != "Guest":
          summary["email"] = doc.email
     return summary

# 21f3f4a3ca05eb2

# 5dd585cf155bd4a