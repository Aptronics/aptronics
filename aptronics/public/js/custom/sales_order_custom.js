{% include 'aptronics/public/js/bundling.js' %}

frappe.ui.form.on("Sales Order", {
	refresh: (frm) => {
	 aptronics.buyer_filter(frm);
	},
	before_cancel: (frm) => {
		aptronics.provide_cancellation_reason(frm);
	}
});

function toggleNamingSeries(frm){
	if (frm.doc.docstatus != 0) {
		return;
	}

	if(frm.doc.is_return == 1){
		frm.doc.naming_series = 'SRH.#######';
	} else {
		frm.doc.naming_series = 'SDH.#######';
	}
	frm.refresh_field('naming_series');
}
