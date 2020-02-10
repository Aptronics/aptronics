{% include 'aptronics/public/js/bundling.js' %}

frappe.provide("aptronics");

frappe.ui.form.on("Sales Invoice", {
	refresh: (frm) => {
		frm.cscript.delivery_note_btn = patchDeliveryNoteBtn;
		toggleNamingSeries(frm);
		aptronics.disallow_attachment_delete(frm)
	},
	is_return: (frm) => {
		toggleNamingSeries(frm);
	},
	validate: (frm) => {
		confirm_non_git_items(frm);
	},
	before_submit: (frm) => {
		confirm_non_git_items(frm);
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
	if (frm.doc.docstatus != 0) {
		return;
	}

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

function patchDeliveryNoteBtn() {
	cur_frm.add_custom_button(__('Delivery Notes'),
		function() {
			erpnext.utils.map_current_doc({
				method: "aptronics.overrides.make_aptronics_sales_invoice",
				source_doctype: "Delivery Note",
				target: cur_frm,
				date_field: "posting_date",
				setters: {
					customer: cur_frm.doc.customer || undefined
				},
				get_query: function() {
					var filters = {
						docstatus: 1,
						company: cur_frm.doc.company,
						is_return: 0
					};
					if(cur_frm.doc.customer) filters["customer"] = cur_frm.doc.customer;
					return {
						query: "erpnext.controllers.queries.get_delivery_notes_to_be_billed",
						filters: filters
					};
				}
			});
		}, __("Get items from"));
}

function confirm_non_git_items(frm){
	let non_git_rows = '';
	frappe.db.get_value("Company", frm.doc.company, 'default_goods_in_transit_warehouse', (r) => {
		let git_wh = r.default_goods_in_transit_warehouse;
		frm.doc.items.forEach((row) => {
			if(row.warehouse != git_wh){
				let s = "Row " + row.idx + ": (" + row.qty + ") " + row.item_code + " <b>" + row.warehouse + "</b><br>";
				non_git_rows += s;
			}
		})
		if(non_git_rows.length > 0){
			var d = new frappe.ui.Dialog({
				title: __("The following rows are not sourcing from " + git_wh),
				fields: [
		        {'fieldname': 'ht', 'fieldtype': 'HTML'},
		    ],
		    primary_action: function(){

			  }
			});
			d.get_primary_btn().hide();
			d.fields_dict.ht.$wrapper.html(non_git_rows);
			d.show();
		}
	})
}
