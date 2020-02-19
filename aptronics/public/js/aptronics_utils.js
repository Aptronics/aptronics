frappe.provide("aptronics");

aptronics.buyer_filter = function (frm){
	frm.set_query("buyer", () => {
		return {
			query: "aptronics.queries.buyer_permissions"
		};
	});
	frappe.ui.form.on(frm.doc.doctype, {
		buyer: (frm) =>{
			if(frm.doc.buyer == undefined){
				frm.doc.buyer_name = "";
				frm.refresh_field('buyer_name');
			}
		}
	});
};

aptronics.clear_buyer_name = function (frm){
	if(frm.doc.buyer == undefined){
		frm.doc.buyer_name = "";
		frm.refresh_field('buyer_name');
	}
};

aptronics.cancellation_reason_dialog = function (frm) {
	return new Promise(resolve => {
		let dialog = new frappe.ui.Dialog({
			title: __("Please provide a cancellation reason"),
			fields: [
				{"fieldtype": "Text",
					"label": __("Cancellation Reason"),
					"fieldname": "cancellation_reason",
					"reqd": 1
				},
			],
			primary_action: function() {
				let values = dialog.get_values();
				resolve({
					doctype: frm.doc.doctype,
					docname: frm.doc.name,
					cancellation_reason: values.cancellation_reason,
					user: frappe.session.user
				});
			},
			primary_action_label: __('Submit')
		});
		dialog.show();
		dialog.get_close_btn().hide();
	});
};

aptronics.provide_cancellation_reason = async function(frm){
	let args = await aptronics.cancellation_reason_dialog(frm);
	frappe.call({
		method: 'aptronics.workflows.provide_cancellation_reason',
		args: args,
		async: false,
	}).done(() => {
		cur_dialog.hide();
		frm.reload_doc();
	});
};

aptronics.disallow_attachment_delete = function(frm){
	if(frm.doc.docstatus == 1){
		frm.$wrapper.find('.attachment-row').find('.close').hide()
	}
}

aptronics.get_radical_iref = function(frm){
	let docflow = {
		'Sales Order': 'Quotation',
		'Delivery Note': 'Sales Order',
		'Sales Invoice': 'Delivery Note',
		'Purchase Order': 'Sales Order',
		'Purchase Receipt': 'Purchase Order',
		'Purchase Invoice': 'Purchase Receipt'
	}
	if(frm.doc.radical_iref)
		return

	frappe.db.get_value(docflow[frm.doc.doctype], "!!!!docname", "radical_iref", r  => {
			frm.doc.radical_iref = r.radical_iref
		})
}
