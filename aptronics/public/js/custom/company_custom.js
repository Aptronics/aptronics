frappe.ui.form.on("Company", {
	onload: (frm) => {
		frm.set_query("default_expense_account", function() {
			return { filters: { root_type: "Asset" } };
		});
	}
});
