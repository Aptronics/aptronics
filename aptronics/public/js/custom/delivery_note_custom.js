frappe.ui.form.on("Delivery Note", {
	onload: (frm) => {
		frm.fields_dict.items.grid.get_field('expense_account').get_query =
			function() {
				return { filters: { account_type: ["in", ["Asset", "Expense"]]}};
			};
	},
	refresh: (frm) =>{
		create_invoice(frm);
		git_read_only(frm);
	}
});

function create_invoice(frm){
	if(frm.doc.last_workflow_action == 'Delivered and Create Invoice'){
		frm.doc.last_workflow_action = 'Submitted';
		frappe.db.set_value("Delivery Note", frm.doc.name, 'last_workflow_action', 'Submitted',
			() => {});
		frappe.model.open_mapped_doc({
			method: "erpnext.stock.doctype.delivery_note.delivery_note.make_sales_invoice",
			frm: frm
		});
	}
}
function git_read_only(frm){
	if(frm.doc.workflow_state == 'Goods in Transit' || frm.doc.workflow_state == 'Delivered'){
		frm.set_read_only(1);
	}
}
