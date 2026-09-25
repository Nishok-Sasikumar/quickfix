// Copyright (c) 2026, Nishok and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Card", {


    setup: function(frm) {
        frm.set_query("assigned_technician", function() {
            return {
                filters: {
                    status: "Active",
                    specialization: frm.doc.device_type
                }
            };
        });
    }
,
	refresh(frm){
    let status =frm.doc.status;
    let c= "gray";
    if(status ==="Draft"){
        c="gray";
    }else if(status ==="Pending Diagnosis"){
        c="orange";
    }else if(status ==="Awaiting Customer Approval"){
        c="yellow";
    }else if(status ==="In Repair"){
        c="blue";
    }else if(status ==="Ready for Delivery"){
        c="purple";
    }else if(status ==="Delivered"){
        c="green";
    }else if(status==="Cancelled"){
        c="red";
    }

    frm.dashboard.add_indicator(status,c);
    if(frm.doc.status ==="Ready for Delivery" && frm.doc.docstatus ===1){
        frm.add_custom_button("Mark as Delivered",()=>{
            frm.set_value("status","Delivered");
            frm.set_value("delivery_date",frappe.datetime.get_today());
            frm.save();
        });
    }


    if(frm.doc.status !=="Delivered" && frm.doc.status !=="Cancelled"){
        frm.add_custom_button("Reject Job", ()=>{
            let dialog =new frappe.ui.Dialog({
                title:"Reject Job Card",
                fields:[{
                        label:"Rejection Reason",
                        fieldname:"rejection_reason",
                        fieldtype:"Small Text",
                        reqd:1
                    }
                ],
                primary_action_label:"Reject",
                primary_action(val){
                    frm.set_value("status","Cancelled");
                    frm.set_value("remarks",val.rejection_reason);
                    frm.save();
                    dialog.hide();
                }
            });
            dialog.show();
        });
    }

    if(frm.doc.assigned_technician){
        frm.add_custom_button("Transfer Technician",()=>{
            frappe.prompt({
                    label:"New Technician",
                    fieldname:"new_technician",
                    fieldtype:"Link",
                    options:"Technician",
                    reqd:1
                },
                function(val){
                    frappe.confirm("Are you sure you want to transfer this job to "+val.new_technician,
                        function(){frappe.call({
                                method:"frappe.client.set_value",
                                args:{
                                    doctype: "Job Card",
                                    name: frm.doc.name,
                                    fieldname: "assigned_technician",
                                    value: val.new_technician
                                },
                                callback(r){
                                    frm.reload_doc();
                                    frm.trigger("assigned_technician");
                                }});
                        });
                },"Transfer Technician","Transfer"
            );});
    }
    // const manager = frappe.user.has_role('QE Manager');
    // frm.toggle_display('customer_phone',manager);

},

    assigned_technician(frm){
        if(!frm.doc.assigned_technician){
            return;
        }
        frappe.call({
            method:"frappe.client.get_value",
            args:{
                doctype:"Technician",
                filters: frm.doc.assigned_technician,
                fieldname:"specialization"
            },
            callback(r){
                let spec =r.message.specialization;
                if(spec && spec !== frm.doc.device_type){
                    frappe.msgprint("Technician specialization ("+spec+")does not match device type ("+frm.doc.device_type+")");
                }
            }
        });
    }

});


frappe.ui.form.on("Part Usage Entry",{
    quantity(frm,cdt,cdn){
        let row =locals[cdt][cdn];
        let total =row.quantity*row.unit_price;
        frappe.model.set_value(cdt,cdn,"total_price",total);
    }
});