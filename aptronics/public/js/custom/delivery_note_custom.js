frappe.ui.form.on("Delivery Note", {
	onload: (frm) => {
		frm.fields_dict.items.grid.get_field('expense_account').get_query =
			function() {
				return { filters: { account_type: ["in", ["Asset", "Expense"]]}};
			};
	},
	refresh: (frm) =>{
		// confirm_posting_date(frm);
		git_read_only(frm);
	},
	before_submit: (frm) => {
		create_invoice(frm);
	}
});

function create_invoice(frm){
	if(frm.doc.last_workflow_action == 'Delivered and Create Invoice'){
		frappe.validated = false;
		frappe.run_serially([
			() => confirm_posting_date(frm),
			() => frm.doc.last_workflow_action = 'Submitted',
			() => frappe.db.set_value("Delivery Note", frm.doc.name, 'last_workflow_action', 'Submitted',	() => {}),
			() => frappe.model.open_mapped_doc({
				method: "erpnext.stock.doctype.delivery_note.delivery_note.make_sales_invoice",
				frm: frm
			}),
			() => frappe.validated = true
		]);
	} else if(frm.doc.last_workflow_action == 'Goods Delivered with Invoice'){
		frappe.run_serially([
			() => confirm_posting_date(frm),
			() => frm.doc.last_workflow_action = 'Submitted',
			() => frappe.db.set_value("Delivery Note", frm.doc.name, 'last_workflow_action', 'Submitted',	() => {}),
			() => frappe.validated = true
		]);
	}
}

function git_read_only(frm){
	if(frm.doc.workflow_state == 'Goods in Transit' || frm.doc.workflow_state == 'Delivered'){
		frm.set_read_only(1);
	}
}

function confirm_posting_date(frm){
	var d = new frappe.ui.Dialog({
		title: __("Confirm Posting Date and Time"),
		fields: [
			{'fieldname': 'posting_date', 'fieldtype': 'Date',
				"label": "Posting Date (today)", 'default': moment()},
			{'fieldname': 'posting_time', 'fieldtype': 'Time',
				"label": "Posting Time (now)", 'default': moment().format('HH:mm:sss')},
			{'fieldname': 'update_posting', 'fieldtype': 'HTML'},
		]
	});
	d.confirm_dialog = true;
	d.current_posting_date = frm.doc.posting_date;
	d.current_posting_time = frm.doc.posting_time;
	d.show();
	d.fields_dict.update_posting.$wrapper.html(posting_actions);
	d.$wrapper.find(".modal-header .btn-primary").hide();
	d.$wrapper.find("[data-action=\"update_posting\"]").on("click", function(){
		update_posting(frm, d);
		d.hide();
	});
	d.$wrapper.find("[data-action=\"dont_update_posting\"]").on("click", () => {
		dont_update_posting(frm, d);
		d.hide();
	});
}

let posting_actions = '<div class="col text-center">\
<button type="button" data-action="update_posting" class="btn btn-primary btn-sm" aria-expanded="false">Update Posting Date and Time</button> \
 <button type="button" data-action="dont_update_posting" class="btn btn-warning btn-sm" aria-expanded="false">Don\'t Update Posting Date and Time</button>';

function update_posting(frm, d){
	let values = d.get_values();
	frm.doc.set_posting_time = 1;
	frm.doc.posting_date = values.posting_date;
	frm.doc.posting_time = values.posting_time;
	frm.refresh_field('set_posting_time');
	frm.refresh_field('posting_date');
	frm.refresh_field('posting_time');
	d.hide();
}

function dont_update_posting(frm, d){
	frm.doc.set_posting_time = 0;
	frm.doc.posting_date = d.current_posting_date;
	frm.doc.posting_time = d.current_posting_time;
	frm.refresh_field('set_posting_time');
	frm.refresh_field('posting_date');
	frm.refresh_field('posting_time');
	d.hide();
}
