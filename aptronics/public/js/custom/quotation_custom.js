{% include 'aptronics/public/js/bundling.js' %}

frappe.ui.form.on("Quotation", {
	before_cancel: (frm) => {
		aptronics.provide_cancellation_reason(frm);
	}
});
