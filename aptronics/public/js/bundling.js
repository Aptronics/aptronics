frappe.ui.form.on("Sales Invoice", {
  refresh: (frm) => {
      console.log('bundling file included')
  }
});

frappe.ui.form.on("Sales Invoice Item", {
	items_add: (frm, cdn, cdt) => {
		get_gita_wh(frm, cdn, cdt);
	},
	items_remove: (frm, cdt, cdn) => {
		get_gita_wh(frm, cdt, cdn);
	},

});

// <i class="octicon octicon-package" style="color: rgb(141, 153, 166); font-size: 18px; margin-right: 8px;"></i>
// <i class="octicon octicon-package" style="color: rgb(152, 216, 91); font-size: 18px; margin-right: 10px;"></i>
