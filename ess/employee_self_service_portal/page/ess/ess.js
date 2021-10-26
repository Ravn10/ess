frappe.pages['ess'].on_page_load = function(wrapper) {
    new ESS(wrapper);
    console.log(wrapper)

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

    // bind event to all buttons on page
    bind_events: function() {
		let btns = document.querySelectorAll('#leave_application');
        for (i of btns) {
        i.addEventListener('click', function(me) {
            console.log(this.value);
            console.log(me);
            // leave application dialog

		let edit_profile_dialog = new frappe.ui.Dialog({
			title: __('Leave Application'),
			fields: [
                {
					fieldtype: 'Link',
					fieldname: 'employee',
					label: 'Employee',
                    options: 'Employee',
                    default:this.employee
				},
                {
                    fieldtype: 'Date',
                    fieldname: 'from_date',
                    label: 'From Date'
                },
				{
                    fieldtype: 'Column Break'
				},
                {
                    fieldtype: 'Link',
                    fieldname: 'leave_type',
                    label: 'Leave Type',
                    options: 'Leave Type',
                    default: this.value
                },
				{
					fieldtype: 'Date',
					fieldname: 'to_date',
					label: 'To Date',
				},
				{
					fieldtype: 'Section Break',
					fieldname: 'Approver',
				},
                {
					fieldtype: 'Link',
					fieldname: 'approver',
					label: 'Approver',
                    options: 'Employee'
				},
                {
					fieldtype: 'Small Text',
					fieldname: 'description',
					label: 'Reason'
				},

			],
			primary_action: values => {
				edit_profile_dialog.disable_primary_action();
				frappe.xcall('ess.employee_self_service_portal.page.ess.ess.create_leave_application', {
					info: values
				}).then(r => {
					console.log(r.message)
				}).finally(() => {
					edit_profile_dialog.hide();
				});
			},
			primary_action_label: __('Save')
		});

		edit_profile_dialog.set_values({
			employee: frappe.get_route()[1],
		});
		edit_profile_dialog.show();
        });
        }
	},

    // make page
    make: function(){
        // grab the class
        let me = $(this);
        // push dom element to page
        $(frappe.render_template("ess_body",{})).appendTo(this.page.main)
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
        console.log(this)
        // this.leaveApplication()
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
                this.get_checkin()
                this.checkin()
                this.checkout()
                setInterval(() => {
                    this.showTime()
                    frappe.datetime.refresh_when();
                }, 1000);
                this.get_balance_leaves()
                this.bind_events()
                this.get_holiday_list()
                this.get_employee_with_birthday_this_month()
                this.get_employee_on_leave_this_month()
                this.get_approvals_list()
                console.log("printing me")
                console.log(me)
                console.log(me.curr_month)

        })
    },

    // Get Holiday List
    get_holiday_list: function(){
        frappe.call({
            method: "ess.employee_self_service_portal.page.ess.ess.holiday_for_month",
            async: false,
            args: {
                employee:"HR-EMP-00001"
            },
            callback: function(r) {
                console.log(r.message)
                frappe.render_template('ess_list',{'data':r.message})
                let find = document.querySelector('.holiday');
                let html = frappe.render_template('ess_list',{'data':r.message});
                let div = document.createElement('div');
                div.innerHTML = html;
                find.appendChild(div);
            }
        });
    },
    // Get Leave Balances
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
        console.log(this)
        // this.leaveApplication()
    },
    // cheakin button action
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

    // get checkin and checkout
    get_checkin: function(){
        frappe.call({
            method:"ess.employee_self_service_portal.page.ess.ess.get_checkin",
            args:{"employee":frappe.get_route()[1]}
        }).then(r => {
            console.log(r.message)
            if(r.message['checkin_count']>0 || r.message['checkout_count']>0 ){
                console.log('checkin')
                console.log(r.message['checkin'])
                if (r.message['checkin']){
                    let find = document.querySelector('#attendance-text');
                    let html = '<b>Checkin</b>'
                    r.message['checkin'].forEach(element => {
                        html+="<br>"+element['name']
                    });
                    let div = document.createElement('div');
                    div.innerHTML = html;
                    div.style="color:green"
                    find.appendChild(div);
                    // document.getElementById("checkin").disabled = true;
                }
                if(r.message['checkout']){
                    let find = document.querySelector('#attendance-text');
                    let html = '<b>Checkout</b>'
                    r.message['checkout'].forEach(element => {
                        html+="<br>"+element['name']
                    });
                    let div = document.createElement('div');
                    div.innerHTML = html;
                    div.style="color:red"
                    find.appendChild(div);
                    // document.getElementById("checkout").disabled = true;
                    // document.getElementById("checkin").disabled = false;

                }
                console.log('checkout')
                console.log(r.message['checkout'])
            }
            else{
                alert("Not Checked In Yet!!!")
                frappe.confirm(
                    'Do You want to Checked In Now??',
                    function(){
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
                        window.close();
                    },
                    function(){
                        show_alert('Thanks for continue here!')
                    }
                )
            }

        })
    },
    // get_employee_with_birthday_this_month
    get_employee_with_birthday_this_month: function(){
        frappe.call({
            method:"ess.employee_self_service_portal.page.ess.ess.get_employee_with_birthday_this_month"
        }).then(r => {
            let find = document.querySelector('.birthday');
            let html = frappe.render_template('birthday',{'data':r.message});
            let div = document.createElement('div');
            div.innerHTML = html;
            find.appendChild(div);
        })
    },
    // get_employee_on_leave_this_month
    get_employee_on_leave_this_month: function(){
        frappe.call({
            method:"ess.employee_self_service_portal.page.ess.ess.get_employee_on_leave_this_month"
        }).then(r => {
            let find = document.querySelector('.onleave');
            let html = frappe.render_template('leave',{'data':r.message});
            let div = document.createElement('div');
            div.innerHTML = html;
            find.appendChild(div);
        })
    },
    // approvals list
    get_approvals_list: function(){
        // frm.add_custom_button(__('Ledger'), function() {
        //     frappe.route_options = {
        //         "voucher_no": frm.doc.name,
        //         "from_date": frm.doc.posting_date,
        //         "to_date": frm.doc.posting_date,
        //         "company": frm.doc.company,
        //         "show_cancelled_entries": frm.doc.docstatus === 2
        //     };
        //     frappe.set_route("query-report", "General Ledger");
        // }, __('View'));
        let find = document.querySelector('.approvals');
        let html =  frappe.render_template(`<button type="button" class="btn btn-danger" href="#/apps/leave-application">
                        Profile <span class="badge badge-light">{{ open_la }}</span>
                        <span class="sr-only">unread messages</span>
                    </button>`,{'open_la':2})
        let div = document.createElement('div');
        div.innerHTML = html;
        div.onclick = function(){
            frappe.route_options = {
                "status": "Open"
            };
            frappe.set_route("Form", "Leave Application");
            }
        find.appendChild(div);
    },
    // timer function
    showTime: function(){

        document.getElementById("date").innerText = frappe.datetime.get_datetime_as_string();
        document.getElementById("date").textContent = frappe.datetime.get_datetime_as_string();

        // setTimeout(showTime, 1000);
    }
})
