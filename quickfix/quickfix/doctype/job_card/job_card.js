// Copyright (c) 2026, Nishok and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Card", {
	// setup:function(frm){
    //     frm.set_query("assigned_technician",function(){
    //         return{
    //             filters:{
    //                 status:"Active",
    //                 specialization:frm.doc.device_type
    //             }
    //         }
    //     })
    // },
    refresh:function(frm){
        let status=frm.doc.status;
        let color = "gray";
        if(status==="Draft")
            {
                color="gray";
            }else if(status==="Pending Diagnosis"){
                color="orange";
            }
            else if(status==="Awaiting Customer"){
                color="yellow";
            }
            else if(status==="In Repair"){
                color="blue";
            }
            else if(status==="Ready for Delivery"){
                color="purple";
            }
            else if(status==="Delivered"){
                color="green";
            }
            else if(status==="Cancelled"){
                color="red";
            }
            frm.dashboard.add_indicator(status,color);
            if(frm.doc.status === "Ready for Delivery" && frm.doc.docstatus ===1){
                frm.add_custom_button("Mark as Delivered",function(){
                    frm.set_value("status","Delivered");
                    frm.set_value("delivered_date",frappe.datetime.get_today());
                    frm.save();
                });
            }

    }
});
