// Copyright (c) 2026, Nishok and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Card", {

    device_type(frm){
        tech_filter();
    },
    onload(frm){
        tech_filter();
    },
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
                },
                "Transfer Technician","Transfer"
            );});
    }
},
});
function tech_filter(frm){
    frm.set_df_property("assigned_technician","filters",{
        status:"Active",specalization:frm.doc.device_type
    });
}
