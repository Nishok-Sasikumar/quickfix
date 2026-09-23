# E1 — Complete Lifecycle
## on_update() 
## Call self.save() inside on_update and observe what breaks. Explain it and correct the pattern in README_internals.md.
- `When self.save() inside the on update is used , the save will call the update method , as the upadation is made the on_update function is called again , thus this reccursively call the save . This results in the reccursive hell.`


# E2 — autoname & Renaming

## Call frappe.rename_doc("Technician", old, new, merge=False) in a utility function and show linked fields update automatically. Explain when merge=True would be dangerous.

- ` when we call the frappe.rename_doc , it automatically change the name by searching the other linked documents too. when the merge = True , if there is a document  exists already and the same document name is renamed to a existing one , then the document values will be merged and the data will be lost.`


# E3 — One Performance Judgment Call
## frappe.db.get_value vs get_doc
## In the Spare Part controller's on_update, which pattern would you use and why?

## doc = frappe.get_doc("QuickFix Settings", "QuickFix Settings")
## threshold = doc.low_stock_threshold

## threshold = frappe.db.get_value("QuickFix Settings", None, "low_stock_threshold")
## ANSWER
- `The best one is threshold = frappe.db.get_value("QuickFix Settings", None, "low_stock_threshold") because frappe.get_doc() load the entire document and its fields and everything it is related to and even the permissions too. But in the frappe.get_value() it straightly go to the db and fetch the value related to the field.As same for the spare part controller's on_update , the frappe.get_vlaue() is used as it is about to check the threshold alone and not accessing the complete document.`

# I1 — Query Report: Open Job Cards
## SQL parameterization
## Selects name, customer_name, device_type, status, assigned_technician, estimated_cost, creation. Filter: status NOT IN ("Delivered","Cancelled"), optional device_type filter using %(device_type)s. In README_internals.md: show the f-string version side by side with the parameterized version, and explain why the latter is always preferred.

- `In f-string whatever the user type in the device type , filter is pasted into SQl string as text before the query runs.But in the parametrized like %()s it is not string, as the frappe.db.sql() send the query as same as the user sent.`