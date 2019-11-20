{% include 'aptronics/public/js/bundling.js' %}

frappe.ui.form.on("Sales Order", {
	refresh: (frm) => {
	 aptronics.buyer_filter(frm);
	 set_default_delivery_date(frm);
	},
	before_cancel: (frm) => {
		aptronics.provide_cancellation_reason(frm);
	},
	validate: (frm) => {
		set_default_delivery_date(frm);
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

function set_default_delivery_date(frm){
	frm.doc.items.forEach((row) => {
		if(row.delivery_date == undefined){
			row.delivery_date = moment().add(14, 'days').format('YYYY-MM-DD');
		}
	})
	if(frm.doc.delivery_date != undefined){
		return;
	}
	frm.doc.delivery_date = moment().add(14, 'days').format('YYYY-MM-DD');
	frm.refresh_field('items');
	frm.refresh_field('delivery_date');
}
