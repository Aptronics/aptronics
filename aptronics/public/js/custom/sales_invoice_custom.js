{% include 'aptronics/public/js/bundling.js' %}

frappe.ui.form.on("Sales Invoice", {
	refresh: (frm) => {
		frm.cscript.delivery_note_btn = patchDeliveryNoteBtn(frm);
		toggleNamingSeries(frm);
	},
	is_return: (frm) => {
		toggleNamingSeries(frm);
	},
	before_cancel: (frm) => {
		aptronics.provide_cancellation_reason(frm);
	}
});

frappe.ui.form.on("Sales Invoice Item", {
	items_add: (frm, cdn, cdt) => {
		get_gita_wh(frm, cdn, cdt);
	}
});

function toggleNamingSeries(frm){
	if(frm.doc.is_return == 1){
		frm.doc.naming_series = 'SCR.########';
	} else {
		frm.doc.naming_series = 'SIH.########';
	}
	frm.refresh_field('naming_series');
}

function get_gita_wh(frm, cdt, cdn){
	if(frm.doc.is_return == 1){
		return;
	}
	if(cdn == undefined){
		frm.doc.items.forEach((d) => {
			frappe.db.get_value("Delivery Note Item", d.dn_detail, 'target_warehouse', (r) => {
				if(r){
					frappe.model.set_value("Sales Invoice Item", d.name, "warehouse",
						r.target_warehouse);
				}
			});
		});
	}
}


function patchDeliveryNoteBtn(frm) {
	frm.add_custom_button(__('Delivery Notes'),
		function() {
			erpnext.utils.map_current_doc({
				method: "aptronics.overrides.make_aptronics_sales_invoice",
				source_doctype: "Delivery Note",
				target: frm,
				date_field: "posting_date",
				setters: {
					customer: frm.doc.customer || undefined
				},
				get_query: function() {
					var filters = {
						docstatus: 1,
						company: frm.doc.company,
						is_return: 0
					};
					if(frm.doc.customer) filters["customer"] = frm.doc.customer;
					return {
						query: "erpnext.controllers.queries.get_delivery_notes_to_be_billed",
						filters: filters
					};
				}
			});
		}, __("Get items from"));
}
