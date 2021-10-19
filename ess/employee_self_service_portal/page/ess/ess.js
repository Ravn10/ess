frappe.pages['ess'].on_page_load = function(wrapper) {
    new ESS(wrapper);

}

//Page content
ESS = Class.extend({
    init: function(wrapper){
        this.page = frappe.ui.make_app_page({
            parent: wrapper,
            title: 'Employee Self Service Portal',
            single_column: false
        });
        // this.make()
        this.make_sidebar()

    },
    // make page
    make: function(){
        // grab the class
        let me = $(this);

        // body content
        let body = `<h1>Hello WORLD</h1>`

        // push dom element to page
        $(frappe.render_template("ess_body",{})).appendTo(this.page.main)
        // $(frappe.render_template(body, this)).appendTo(this.page.main)
    },

    // make sidebar
    make_sidebar: function(){
        // grab the class
        let me = $(this);
        console.log(me)
        console.log(this.page)
        // me.page.set_title("Hemml")
        // get employee details
        frappe.call({
            method:"ess.employee_self_service_portal.page.ess.ess.get_employee_details",
            args:{"employee":frappe.get_route()[1]}
        }).then(r => {
                console.log(r.message)
                $(frappe.render_template("ess_sidebar",
                                                        {
                                                            "employee_name":r.message['employee_name'],
                                                            "image":r.message['image']
                                                        })).appendTo(this.page.sidebar)

                $(frappe.render_template("ess_body",r.message)).appendTo(this.page.main)
                this.page.set_title(r.message['employee_name'])
                if(r.message['status']==="Active"){
                    this.page.set_indicator('Active', 'green')
                }else if(r.message['status']==="Inactive"){
                    this.page.set_indicator('Inactive', 'orange')
                }else if(r.message['status']==="Left"){
                    this.page.set_indicator('Left', 'red')
                }else {
                    this.page.set_indicator('Unknown', 'gray')
                }
                this.checkin()
                this.checkout()
                // me.page.sidebar.empty().append(frappe.render_template('ess_sidebar', {
                //     image: r.message['image']
                // }));
                // me.main_section.empty().append(frappe.render_template('employee_self_servic',{}));

        })

        // push dom element to page
        // $(frappe.render_template("ess_sidebar", {"employee_name":"Aniket","image":'/files/avatar.png'})).appendTo(this.page.sidebar)
    },
    // button action
    checkin: function(){

        document.querySelector('.checkin').addEventListener("click", function() {
            console.log("Checkin")
            frappe.call({
                method:"ess.employee_self_service_portal.page.ess.ess.checkin",
                args:{"employee":frappe.get_route()[1],"log_type":"IN"}
            }).then(r => {
                console.log(r)
                let find = document.querySelector('#attendance-text');
                let html = r.message;
                let div = document.createElement('div');
                div.innerHTML = html;

                find.appendChild(div);
            })
          });
    },
    checkout: function(){
        document.querySelector('.checkout').addEventListener("click", function() {
            console.log("Check Out")
            frappe.call({
                method:"ess.employee_self_service_portal.page.ess.ess.checkin",
                args:{"employee":frappe.get_route()[1],"log_type":"OUT"}
            })
          });
    }
})
