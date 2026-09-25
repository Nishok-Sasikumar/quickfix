# Copyright (c) 2026, Nishok and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

def before_print(doc, method=None, print_settings=None):
	doc.print_summary = (f"{doc.customer_name} - "f"{doc.device_type} {doc.device_model}")


class JobCard(Document):
	def validate(self):
		if len(self.customer_phone)!=10:
			frappe.throw("Phone number must be 10 digits")
		if self.status in ["In Repair","Ready for Delivery","Delivered","Cancelled"]:
			if not self.assigned_technician:
				frappe.throw("The technician should be there")
		sum=0
		for i in self.parts_used:
			i.total_price = i.quantity * i.unit_price
			sum +=i.total_price
		self.parts_total=sum

		if not self.labour_charge:
			s = frappe.get_single("QuickFix Settings")
			self.labour_charge=s.default_labour_charge
		self.final_amount = self.parts_total+self.labour_charge

	def before_submit(self):
		if not  self.status == "Ready for Delivery":
			frappe.throw("Cannot sumbit, it must be Ready for delivery")
		for i in self.parts_used:
			stq = frappe.db.get_value("Spare Part",i.part,"stock_qty")
			if stq <= i.quantity:
				frappe.throw("No enough stock")
	def on_submit(self):
		for i in self.parts_used:
			cqty =frappe.db.get_value("Spare Part",i.part,"stock_qty")
			nqty = cqty - i.quantity
			frappe.db.set_value("Spare Part",i.part,"stock_qty",nqty)
			# this is a system action that happen automatically 
			# when job card is submited as the technician have permission to 
			# submit the doc, they do not need seperate permission on spare part
		if not frappe.db.exists("Service Invoice",{"job_card":self.name}):
			inv=frappe.new_doc("Service Invoice")
			inv.job_card=self.name
			inv.labour_charge=self.labour_charge
			inv.parts_total=self.parts_total
			inv.total_amount=self.final_amount
			inv.payment_status="Unpaid"
			inv.insert(ignore_permissions=True)
			frappe.enqueue("quickfix.api.send_job_ready_email",jc=self.name)

	

	def on_cancel(self):
		self.status="Cancelled"
		for i in self.parts_used:
			cqty =frappe.db.get_value("Spare Part",i.part,"stock_qty")
			nqty=cqty+i.quantity
			frappe.db.set_value("Spare Part",i.part,"stock_qty",nqty)
			invn=frappe.db.get_value("Service Invoice",{"job_card":self.name},"name")
			if invn:
				invoice=frappe.get_doc("Service Invoice",invn)
				if invoice.docstatus==1:
					invoice.cancel()
	def on_trash(self):
		if self.status !="Cancelled" and self.status != "Draft":
			frappe.throw("Cannot delete as it should be in cancelled or in draft state")
	# def on_update(self):
	# 	self.save()
