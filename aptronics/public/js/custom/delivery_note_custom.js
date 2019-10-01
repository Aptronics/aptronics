frappe.ui.form.on("Delivery Note", {
	refresh: (frm) => {
		get_gita_wh(frm);
	},
	onload: (frm) => {
		get_gita_wh(frm);
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

function get_gita_wh(frm, cdt, cdn){
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
