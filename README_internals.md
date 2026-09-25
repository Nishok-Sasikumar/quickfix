# B2c — Dangerous Patterns - document lifecycle bugs

## The snippet below has two bugs related to document lifecycle. Identify both and write the corrected version in README_internals.md:
```
  def validate(self):
  self.total = sum(r.amount for r in self.items)
    self.save()
    other = frappe.get_doc("Spare Part", self.part)
    other.stock_qty -= self.qty
    other.save()
```
# Answer

def validate(self):
    self.total = sum(r.amount for r in self.items)-
def on_update(self):
    other = frappe.get_doc("Spare Part", self.part)
    other.stock_qty -= self.qty
    other.save()
` The calculations should be done on the validations and the db related things should be done on the on_update`

# B2d — Concurrency, One Question - optimistic locking
## In README_internals.md: why would you see a "Document has been modified after you have opened it" error, and how does Frappe prevent concurrent overwrites? (One paragraph.)

## ANSWER
-` This error comes up when two people open the same document at the same time, and one of them saves first. Every document has a "modified" timestamp. When you open a doc, Frappe remembers that timestamp. When you save, Frappe checks if the timestamp is still the same. If someone else already saved in between, the timestamp changed, so Frappe blocks your save instead of overwriting their changes by mistake.Frappe does not lock the document while it is open, it only checks for conflicts at the time of saving.`

# C3 — Part Usage Entry & Service Invoice
## rename a test Technician record. Does assigned_technician on linked Job Cards update automatically? Why or why not?

# ANSWER 
- `Yes, it updates automatically. Because frappe.rename_doc() also looks at other doctypes that have a link field to technician.Job Card's assigned_technician field is one of them.So when I rename a technician,frappe finds all Job Cards using the old name and changes them to the new name by itself. I did not have to fix anything manually.`

# E1 — Complete Lifecycle
## on_update() 
## Call self.save() inside on_update and observe what breaks. Explain it and correct the pattern in README_internals.md.

# ANSWER
- `When self.save() inside the on update is used , the save will call the update method , as the upadation is made the on_update function is called again , thus this reccursively call the save . This results in the reccursive hell.`


# E2 — autoname & Renaming

## Call frappe.rename_doc("Technician", old, new, merge=False) in a utility function and show linked fields update automatically. Explain when merge=True would be dangerous.
# ANSWER
- ` when we call the frappe.rename_doc , it automatically change the name by searching the other linked documents too. when the merge = True , if there is a document  exists already and the same document name is renamed to a existing one , then the document values will be merged and the data will be lost.`


# E3 — One Performance Judgment Call
## frappe.db.get_value vs get_doc
## In the Spare Part controller's on_update, which pattern would you use and why?

## doc = frappe.get_doc("QuickFix Settings", "QuickFix Settings")
## threshold = doc.low_stock_threshold

## threshold = frappe.db.get_value("QuickFix Settings", None, "low_stock_threshold")

## ANSWER
- `The best one is threshold = frappe.db.get_value("QuickFix Settings", None, "low_stock_threshold") because frappe.get_doc() load the entire document and its fields and everything it is related to and even the permissions too. But in the frappe.get_value() it straightly go to the db and fetch the value related to the field.As same for the spare part controller's on_update , the frappe.get_vlaue() is used as it is about to check the threshold alone and not accessing the complete document.`

# H1 — Job Card Form Script

# ANSWER
- `The validate event in Frappe does not support asynchronous operation because the form submission is synchronous and does not wait for promises.If an async call is made in validate,the browser submit the form immediately, often before the server response is received, leading to race conditions or ignored validations.But the onload and refresh events handle asynchronous data fetching because they occur during the form rendering time, where the UI can wait for data.`

# I1 — Query Report: Open Job Cards
## SQL parameterization
## Selects name, customer_name, device_type, status, assigned_technician, estimated_cost, creation. Filter: status NOT IN ("Delivered","Cancelled"), optional device_type filter using %(device_type)s. In README_internals.md: show the f-string version side by side with the parameterized version, and explain why the latter is always preferred.

# ANSWER
- `In f-string whatever the user type in the device type , filter is pasted into SQl string as text before the query runs.But in the parametrized like %()s it is not string, as the frappe.db.sql() send the query as same as the user sent.`


# K2 — Spot the N+1 - bulk fetch vs per-row query
## The snippet below has an N+1 query problem. Identify it and rewrite it:
## N+1 PROBLEM - fix this

`job_cards = frappe.get_all("Job Card", fields=["name","assigned_technician"])`
`for jc in job_cards:`
`    tech = frappe.get_doc("Technician", jc.assigned_technician)`
`    print(tech.technician_name, tech.phone)`
`Bulk operations, manual indexing, and report query-profiling are real skills too — they're in Bonus once this pattern is second nature.`

# ANSWER

job_cards =frappe.get_all("Job Card", fields=["name","assigned_technician"])
technician_names =[]
for jc in job_cards:
    if jc.assigned_technician and jc.assigned_technician not in technician_names:
        technician_names.append(jc.assigned_technician)
tech= frappe.get_all("Technician",filters={"name":["in", technician_names]},fields=["name","technician_name", "phone"])
tech_lookup = {}
for t in tech:
    tech_lookup[tech.name] =t
for j in job_cards:
    t =tech_lookup.get(j.assigned_technician)
    if t:
        print(t.technician_name,t.phone)
 `Here only two times the query is running and no n+1 problem`