# B2c — Dangerous Patterns - document lifecycle bugs

### The snippet below has two bugs related to document lifecycle. Identify both and write the corrected version in README_internals.md:
```
  def validate(self):
  self.total = sum(r.amount for r in self.items)
    self.save()
    other = frappe.get_doc("Spare Part", self.part)
    other.stock_qty -= self.qty
    other.save()
```
## Answer
```
def validate(self):
    self.total = sum(r.amount for r in self.items)-
def on_update(self):
    other = frappe.get_doc("Spare Part", self.part)
    other.stock_qty -= self.qty
    other.save()
```
- ` The calculations should be done on the validations and the db related things should be done on the on_update`

# B2d — Concurrency, One Question - optimistic locking
### In README_internals.md: why would you see a "Document has been modified after you have opened it" error, and how does Frappe prevent concurrent overwrites? (One paragraph.)

## ANSWER
-` This error comes up when two people open the same document at the same time,and one of them saves first. Every document has a "modified" time. When we open a doc,frappe will have the time.when we save,frappe checks if the time is still the same. If someone else already saved in between, the time changed, so frappe blocks your save instead of overwriting their changes by mistake.Frappe does not lock the document while it is open, it only checks for conflicts at the time of saving.`

# C3 — Part Usage Entry & Service Invoice
### rename a test Technician record. Does assigned_technician on linked Job Cards update automatically? Why or why not?

## ANSWER 
- `Yes, it updates automatically. Because frappe.rename_doc() also looks at other doctypes that have a link field to technician.Job Card's assigned_technician field is one of them.So when I rename a technician,frappe finds all Job Cards using the old name and changes them to the new name by itself. I did not have to fix anything manually.`

# D2 — Row-Level Filtering & Data Leaks
### why is frappe.get_all dangerous in a whitelisted method exposed to low-privilege users?

# ANSWER
- `frappe.get_all() never check for the permissions and when it is used in the whitelisted methods , it will leads everyone to access it.`

# E1 — Complete Lifecycle
### on_update() 
### Call self.save() inside on_update and observe what breaks. Explain it and correct the pattern in README_internals.md.

## ANSWER
- `When self.save() inside the on update is used , the save will call the update method , as the upadation is made the on_update function is called again , thus this reccursively call the save . This results in the reccursive hell.`


# E2 — autoname & Renaming

### Call frappe.rename_doc("Technician", old, new, merge=False) in a utility function and show linked fields update automatically. Explain when merge=True would be dangerous.
## ANSWER
- ` when we call the frappe.rename_doc , it automatically change the name by searching the other linked documents too. when the merge = True , if there is a document  exists already and the same document name is renamed to a existing one , then the document values will be merged and the data will be lost.`


# E3 — One Performance Judgment Call
### frappe.db.get_value vs get_doc
### In the Spare Part controller's on_update, which pattern would you use and why?
```
 doc = frappe.get_doc("QuickFix Settings", "QuickFix Settings")
 threshold = doc.low_stock_threshold
 threshold = frappe.db.get_value("QuickFix Settings", None, "low_stock_threshold")
```
## ANSWER
- `The best one is threshold = frappe.db.get_value("QuickFix Settings", None, "low_stock_threshold") because frappe.get_doc() load the entire document and its fields and everything it is related to and even the permissions too. But in the frappe.get_value() it straightly go to the db and fetch the value related to the field.As same for the spare part controller's on_update , the frappe.get_vlaue() is used as it is about to check the threshold alone and not accessing the complete document.`

# H1 — Job Card Form Script

## ANSWER
- `The validate event in Frappe does not support asynchronous operation because the form submission is synchronous and does not wait for promises.If an async call is made in validate,the browser submit the form immediately, often before the server response is received, leading to race conditions or ignored validations.But the onload and refresh events handle asynchronous data fetching because they occur during the form rendering time, where the UI can wait for data.`

# I1 — Query Report: Open Job Cards
### SQL parameterization
### Selects name, customer_name, device_type, status, assigned_technician, estimated_cost, creation. Filter: status NOT IN ("Delivered","Cancelled"), optional device_type filter using %(device_type)s. In README_internals.md: show the f-string version side by side with the parameterized version, and explain why the latter is always preferred.

## ANSWER
- `In f-string whatever the user type in the device type , filter is pasted into SQl string as text before the query runs.But in the parametrized like %()s it is not string, as the frappe.db.sql() send the query as same as the user sent.`

# J1 — Job Card Receipt
### explain the difference between putting a frappe.get_all() call directly inside the Jinja template versus pre-computing in before_print() and referencing doc.precomputed_field.

## ANSWER
- `Calling the frappe.get_all directly inside a jinja template perform db work  during the rendering process it collapse in the reading process thus we are using a python function to get the values.`
i
# K2 — Spot the N+1 - bulk fetch vs per-row query
### The snippet below has an N+1 query problem. Identify it and rewrite it:
### N+1 PROBLEM - fix this

```
job_cards = frappe.get_all("Job Card", fields=["name","assigned_technician"])
for jc in job_cards:
    tech = frappe.get_doc("Technician", jc.assigned_technician)
    print(tech.technician_name, tech.phone) 
```

### Bulk operations, manual indexing, and report query-profiling are real skills too — they're in Bonus once this pattern is second nature.

## ANSWER
```
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
```
- `Here only two times the query is running and no n+1 problem , in this he duplicates are removed using list and then they are filtred using the filters and displayed.`

# L1 — Custom Whitelisted Method
### Test the standard /api/resource/Job Card CRUD once with curl and document one request/response pair. 

## ANSWER
### REQUEST:
```
curl http://127.0.0.1:8000/api/resource/Job%20Card -H "Authorization: token 21f3f4a3ca05eb2:5dd585cf155bd4a"
```
### RESPONSE:
```
{"data":[{"name":"JC-2026-00001"},{"name":"JC-2026-00002"},{"name":"JC-2026-00003"},{"name":"JC-2026-00004"},{"name":"JC-2026-00005"},{"name":"JC-2026-00006"},{"name":"JC-2026-00007"},{"name":"JC-2026-00006-1"}]}
```
### Then write get_job_summary(job_card_name) in api.py that reads via frappe.form_dict (not direct Python args), returns a specific dict of fields — never the whole doc, never customer_email to unauthenticated callers — and returns {"error": "Not found"} with HTTP 404 if the job card doesn't exist.

## ANSWER:
### request
 `http://127.0.0.1:8000/api/method/quickfix.api.get_job_summary?job_card_name=JC-2026-00003`
### response
```
{
  "message": {
    "name": "JC-2026-00003",
    "customer_name": "mohit",
    "device_type": "Tablet",
    "status": "Delivered",
    "final_amount": 380,
    "email": "nishok2005kuro@gmail.com"
  }
}
```
# N1 — ignore_permissions Audit & JS-Hiding Pitfall
### justify every bypass, security theater
`List every place in your code using ignore_permissions=True; for each, write a one-sentence justification (system action, not user-initiated).Add a JS field hide that hides customer_phone for non-managers on the Job Card form — then show that a direct API call can still retrieve the field. Explain in README_internals.md why hiding a field in JavaScript is not a security measure.`

# ANSWER:

`The place where the ignore_permissions=True are used in the :`
```
1.Service Invoice - job_card.py -> it is autogenerated so it require write permission
2.Audit Log Entry - audit.py -> it runs all over the system , so it require permission to who dont have access to that.
3.Default device type - install.py -> as it is done automatically once during the app installation , it also require permissions for that
4.Quickfix setting - install.py -> it is done automatically and it is not user triggered one
5.Customer approve/reject - api.py ->it is a guest user so they dont have permission to modify the status , thus the permission is provided.
```
```the api call can retrieve the field
curl -X GET \ "http://127.0.0.1:8000/api/resource/Job Card/JC-2026-00008" \ -H "Authorization: token 21f3f4a3ca05eb2:5dd585cf155bd4a" 
```
## THE OUTPUT :
```
{
  "data": {
    "name": "JC-2026-00008",
    "owner": "Administrator",
    "creation": "2026-09-25 16:27:06.291331",
    "modified": "2026-09-25 16:29:04.625720",
    "modified_by": "Administrator",
    "docstatus": 2,
    "idx": 0,
    "customer_name": "Vinodth",
    "customer_phone": "9087654321",
    "email": "nishok2005kuro@gmail.com",
    "device_type": "Laptop",
    "problem_description": "\u003Cdiv class=\"ql-editor read-mode\"\u003E\u003Cp\u003Egvb\u003C/p\u003E\u003C/div\u003E",
    "estimated_cost": 0,
    "priority": "Normal",
    "assigned_technician": "TECH-0003",
    "parts_total": 250,
    "labour_charge": 500,
    "final_amount": 750,
    "payment_status": "Unpaid",
    "status": "Ready for Delivery",
    "doctype": "Job Card",
  }

  }

  The toggle never used the hiding of the db , and done only the ui , thus the api call can easily retrive the data.
```

# life cycle of the Job Card
- `https://drive.google.com/file/d/10NG5dk4sAHcnHDHc41djrE29vLFG03A4/view?usp=sharing`