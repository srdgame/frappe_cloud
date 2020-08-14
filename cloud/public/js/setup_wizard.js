frappe.provide("cloud.setup");

frappe.pages['setup-wizard'].on_page_load = function(wrapper) {
	if(frappe.sys_defaults.company) {
		frappe.set_route("desk");
		return;
	}
};

frappe.setup.on("before_load", function () {
	cloud.setup.slides_settings.map(frappe.setup.add_slide);
});

cloud.setup.slides_settings = [
	{
		// Company
		name: 'cloud_company',
		icon: "fa fa-bookmark",
		title: __("Cloud Company"),
		// help: __('Default Cloud Company.'),
		fields: [
			{
				fieldname: 'company_name',
				label: __('Company Name'),
				fieldtype: 'Data',
				reqd: 1
			},
			{
				fieldname: 'company_full_name',
				label: __('Company Full Name'),
				fieldtype: 'Data'
			},
			{
				fieldname: 'company_domain',
				label: __('Company Domain'),
				fieldtype: 'Data',
				reqd: 1
			}
		]
	}
];
