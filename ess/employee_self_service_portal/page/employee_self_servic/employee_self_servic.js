frappe.pages['employee-self-servic'].on_page_load = function(wrapper) {
    new ESS(wrapper);
}
//Page content
ESS = Class.extend({
    init: function(wrapper){
        this.page = frappe.ui.make_app_page({
            parent: wrapper,
            title: 'Employee Self Service Portal',
            card_layout: true,
            single_column: true
        });
        this.make()
        this.myFunction()
        // this.make_sidebar()

    },
    // make page
    make: function(){
        // grab the class
        let me = $(this);

        // body content

        // push dom element to page
        $(frappe.render_template("employee_self_servic",{})).appendTo(this.page.main)
        // $(frappe.render_template(body, this)).appendTo(this.page.main)
    },
    get_balance_leaves: function(){
        frappe.call({
            method: "erpnext.hr.doctype.leave_application.leave_application.get_leave_details",
            async: false,
            args: {
                employee:frappe.get_route()[1] ,
                date: frappe.datetime.get_today()
            },
            callback: function(r) {
                console.log(r.message)
                let find = document.querySelector('.leaves');
                let html = frappe.render_template("ess_table",{data:r.message['leave_allocation']});
                let div = document.createElement('div');
                div.innerHTML = html;
                find.appendChild(div);
                return r.message
            }
        });
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
                setInterval(() => {
                    this.showTime()
                    frappe.datetime.refresh_when();
                }, 1000);
                this.get_balance_leaves()

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
                document.getElementById("checkin").disabled = true;
            })
          });
    },
    checkout: function(){
        document.querySelector('.checkout').addEventListener("click", function() {
            console.log("Check Out")
            frappe.call({
                method:"ess.employee_self_service_portal.page.ess.ess.checkin",
                args:{"employee":frappe.get_route()[1],"log_type":"OUT"}
            }).then(r => {
                console.log(r)
                let find = document.querySelector('#attendance-text');
                let html = r.message;
                let div = document.createElement('div');
                div.innerHTML = html;
                find.appendChild(div);
                document.getElementById("checkout").disabled = true;
            })
          });
    },
    showTime: function(){

        document.getElementById("date").innerText = frappe.datetime.get_datetime_as_string();
        document.getElementById("date").textContent = frappe.datetime.get_datetime_as_string();

        // setTimeout(showTime, 1000);
    }



})
