{% include 'aptronics/public/js/bundling.js' %}

frappe.ui.form.on("Quotation", {
	refresh: (frm) =>{
		aptronics.disallow_attachment_delete(frm)
	},
	before_cancel: (frm) => {
		aptronics.provide_cancellation_reason(frm);
	}
});
