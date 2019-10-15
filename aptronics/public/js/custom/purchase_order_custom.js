frappe.ui.form.on("Purchase Order", {
	refresh: (frm) => {
		frm.set_df_property("drop_ship", "hidden", 0);
	},
	onload_post_render: (frm) => {
		frm.set_df_property("drop_ship", "hidden", false);
		// frm.remove_custom_button("Purchase Order", __('Create'));
		// frm.add_custom_button(__('Purchase Order'), () => {
		// 	console.log('trigger PO')
		// },
		// __('Create'));
	},
	// is_return: (frm) => {
	// 	toggleNamingSeries(frm);
	// }
});
