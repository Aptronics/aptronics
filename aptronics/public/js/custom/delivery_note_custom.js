// frappe.ui.form.on("Delivery Note Item", {
// 	refresh: (frm) => {
//
// 		frm.set_query("expense_account", function() {
// 			return { filters: { root_type: "Stock" } };
// 		});
// 	}
// });

frappe.ui.form.on("Delivery Note", {
	onload: (frm) => {
		frm.fields_dict.items.grid.get_field('expense_account').get_query =
			function() {
				return { filters: { account_type: "Stock" } };
			};
	}
});
