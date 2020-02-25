{% include 'aptronics/public/js/bundling.js' %}

frappe.provide("aptronics");

frappe.ui.form.on("Contract", {
	refresh: (frm) => {
		aptronics.disallow_attachment_delete(frm)
	},
	before_cancel: (frm) => {
		aptronics.provide_cancellation_reason(frm);
	}
});
