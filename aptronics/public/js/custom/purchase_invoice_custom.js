frappe.ui.form.on("Purchase Invoice", {
	refresh: (frm) => {
		aptronics.buyer_filter(frm);
		aptronics.disallow_attachment_delete(frm);
	},
	is_return: (frm) => {
		toggleNamingSeries(frm);
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
		frm.doc.naming_series = 'PCR.#######';
	} else {
		frm.doc.naming_series = 'PIH.#######';
	}
	frm.refresh_field('naming_series');
}
