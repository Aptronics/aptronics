frappe.ui.form.on("Delivery Note", {
	refresh: (frm) => {
		get_gita_wh(frm);
		toggleNamingSeries(frm);
	},
	onload_post_render: (frm) => {
		get_gita_wh(frm);
		frm.remove_custom_button("Sales Invoice", __('Create'));
		frm.add_custom_button(__('Sales Invoice'), () => {
			make_sales_invoice(frm);
		},
		__('Create'));
	},
	is_return: (frm) => {
		toggleNamingSeries(frm);
	}
});

frappe.ui.form.on("Delivery Note Item", {
	items_add: (frm, cdn, cdt) => {
		get_gita_wh(frm, cdn, cdt);
	},
	warehouse: (frm, cdt, cdn) => {
		get_gita_wh(frm, cdt, cdn);
	}
});

function toggleNamingSeries(frm){
	if(frm.doc.is_return == 1){
		frm.doc.naming_series = 'SRH.#######';
	} else {
		frm.doc.naming_series = 'SDH.#######';
	}
	frm.refresh_field('naming_series');
}

function get_gita_wh(frm, cdt, cdn){
	if(frm.doc.is_return == 1){
		return;
	}
	if(cdn == undefined){
		frm.doc.items.forEach((d) => {
			frappe.db.get_value("Company", frm.doc.company, 'default_goods_in_transit_warehouse', (r) => {
				if(!d.target_warehouse){
					frappe.model.set_value("Delivery Note Item", d.name, "target_warehouse",
						r.default_goods_in_transit_warehouse);
				}
			});
		});
	} else {
		let d = locals[cdt][cdn];
		frappe.db.get_value("Company", frm.doc.company, 'default_goods_in_transit_warehouse', (r) => {
			if(!d.target_warehouse){
				frappe.model.set_value("Delivery Note Item", d.name, "target_warehouse",
					r.default_goods_in_transit_warehouse);
			}
		});
	}
}

function make_sales_invoice(frm) {
	frappe.model.open_mapped_doc({
		method: "aptronics.overrides.make_aptronics_sales_invoice",
		frm: frm
	});
}
