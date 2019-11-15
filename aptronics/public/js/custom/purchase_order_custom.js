frappe.ui.form.on("Purchase Order", {
	refresh: (frm) => {
		frm.set_df_property("drop_ship", "hidden", 0);
		aptronics.buyer_filter(frm);
	},
	onload_post_render: (frm) => {
		frm.set_df_property("drop_ship", "hidden", 0);
	},
	before_cancel: (frm) => {
		aptronics.provide_cancellation_reason(frm);
	}
});
