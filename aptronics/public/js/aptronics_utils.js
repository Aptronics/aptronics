function buyer_filter(frm){
	frm.set_query("buyer", () => {
		return {
			query: "aptronics.queries.buyer_permissions"
		};
	});
}

function cancellation_reason_dialog(frm) {
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
			primary_action_label: __('Cancel')
		});
		dialog.show();
		dialog.get_close_btn().hide();
	});
}

async function provide_cancellation_reason(frm){
	let args = await cancellation_reason_dialog(frm);
	frappe.call({
		method: 'aptronics.workflows.provide_cancellation_reason',
		args: args,
		async: false,
	}).done(() => {
		cur_dialog.hide();
		frm.reload_doc();
	});
}
