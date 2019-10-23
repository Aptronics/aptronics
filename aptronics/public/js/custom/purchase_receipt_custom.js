frappe.ui.form.on("Purchase Receipt", {
	refresh: (frm) => {
		toggleNamingSeries(frm);
		aptronics.buyer_filter(frm);
	},
	is_return: (frm) => {
		toggleNamingSeries(frm);
	},
	before_cancel: (frm) => {
		aptronics.provide_cancellation_reason(frm);
	}
});

function toggleNamingSeries(frm){
	if(frm.doc.is_return == 1){
		frm.doc.naming_series = 'PNH.#######';
	} else {
		frm.doc.naming_series = 'PRC.#######';
	}
	frm.refresh_field('naming_series');
}
