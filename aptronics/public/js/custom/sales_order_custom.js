frappe.ui.form.on("Sales Order", {
	refresh: (frm) => {
	  // this.frm.add_custom_button(__('Purchase Order'), () => this.make_purchase_order(), __('Create'));
	}
	// onload_post_render: (frm) => {
	// 	frm.remove_custom_button("Purchase Order", __('Create'));
	// 	frm.add_custom_button(__('Purchase Order'), () => {
	// 		make_purchase_order(frm);
	// 	},
	// 	__('Create'));
	// },
	// is_return: (frm) => {
	// 	toggleNamingSeries(frm);
	// }
});

function toggleNamingSeries(frm){
	if(frm.doc.is_return == 1){
		frm.doc.naming_series = 'SRH.#######';
	} else {
		frm.doc.naming_series = 'SDH.#######';
	}
	frm.refresh_field('naming_series');
}
//
// function make_purchase_order(frm){
//   frappe.model.open_mapped_doc({
// 		method: "aptronics.overrides.make_aptronics_purchase_order",
// 		frm: frm
// 	});
// }
