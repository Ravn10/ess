frappe.pages['employee-self-servic'].on_page_load = function(wrapper) {
    frappe.ess = new ESS(wrapper);
	$(wrapper).bind('show', ()=> {
		// Get which leaderboard to show
		frappe.ess.show_employee_details();
	});
}

class ESS {
    constructor(parent){
        frappe.ui.make_app_page({
            parent: parent,
			title: __("Employee Self Service Portal"),
			single_column: false,
			card_layout: true,
        });

        this.parent = parent;
		this.page = this.parent.page;

        // this.page.sidebar.html(`<ul class="standard-sidebar leaderboard-sidebar overlay-sidebar">Hello</ul>`);
		// this.$sidebar_list = this.page.sidebar.find('ul');

		// this.render_user_details();

    }
    show_employee_details(){
        this.main_section = $.find('.layout-main-section');
		let employee = frappe.get_route()[1];
        frappe.call({
            method:"ess.employee_self_service_portal.page.employee_self_servic.employee_self_servic.get_employee_details",
            args:{"employee":employee}
        }).then(r => {
            console.log(r.message)
            this.page.set_title(r.message[0]['employee_name'])
            if(r.message[0]['status']==="Active"){
                this.page.set_indicator('Active', 'green')
            }else if(r.message[0]['status']==="Inactive"){
                this.page.set_indicator('Inactive', 'orange')
            }else if(r.message[0]['status']==="Left"){
                this.page.set_indicator('Left', 'red')
            }else {
                this.page.set_indicator('Unknown', 'gray')
            }
            this.page.sidebar.empty().append(frappe.render_template('employee_self_servic_sidebar', {
                image: r.message[0]['image']
            }));
            this.main_section.empty().append(frappe.render_template('employee_self_servic',{}));

        })

        console.log(employee)
    }
}
