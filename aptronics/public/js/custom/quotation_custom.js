{% include 'aptronics/public/js/aptronics_utils.js' %}
{% include 'aptronics/public/js/bundling.js' %}

frappe.ui.form.on("Quotation", {
	before_cancel: (frm) => {
		provide_cancellation_reason(frm);
	}
});
