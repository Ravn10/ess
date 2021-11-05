frappe.pages['ess-experience'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'ESS Experience',
		single_column: true,
        card_layout: true
	});
}
