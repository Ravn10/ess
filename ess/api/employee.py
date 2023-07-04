import frappe
from hrms.hr.doctype.upload_attendance.upload_attendance import get_active_employees
from frappe.utils import nowdate, get_first_day
from frappe.desk.query_report import run
from hrms.hr.doctype.leave_application.leave_application import get_leave_details

@frappe.whitelist()
def get_employee_from_user():
    employee_data_ = frappe._dict({})
    employee_data = frappe._dict({})
    if frappe.session.user != "Administrtor":
        if frappe.db.exists("Employee",{'user_id':frappe.session.user}):
            employee_name = frappe.db.get_all("Employee",{'user_id':frappe.session.user},pluck='name')[0]
            employee_data_= frappe.db.get_all("Employee",
                              {'employee':employee_name},
                              [
                                  "employee_name",
                                  "date_of_birth",
                                  "department" ,
                                  "grade",
                                  "date_of_joining",
                                  "name",
                                  "company_email",
                                  "personal_email",
                                  "reports_to",
                                  "cell_number",
                                  "gender",
                                  "branch",
                                  "default_shift",
                                  "expense_approver",
                                  "leave_approver",
                                  "shift_request_approver",
                                  "company"
                              ])
            for k,v in employee_data_[0].items():
                employee_data[splitCapitalize(k)] = v
    return employee_data

def splitCapitalize(string):
    out = ''
    for d in string.split('_'):
        out += d.capitalize() + ' '
    return out.strip()

@frappe.whitelist()
def get_employee_on_leave_this_month():
    month_first_date = get_first_day(nowdate())
    leave_info = frappe.db.sql('''select employee_name, from_date, to_date, half_day
                                    from `tabLeave Application`
                                    where docstatus=1
                                    and  status='Approved'
                                    and from_date >=%(from_date)s
                                    order by from_date asc
                                    ''',
                                    {'from_date':month_first_date},
                                    as_dict=1
                                )
    def get_day(data):
        data['from'] = data['from_date'].strftime('%d-%m')
        data['to'] = data['to_date'].strftime('%d-%m')

    list(map(get_day,leave_info))
    absent_today = frappe.db.get_all("Attendance",filters={'status':"Absent",'attendance_date':frappe.utils.get_datetime().date()},fields=['employee_name'])
    employee = get_active_employees()
    for emp in employee:
        if frappe.db.count('Attendance',filters={'employee':emp.name,'attendance_date':frappe.utils.get_datetime().date()}) == 0:
            absent_today.append({'employee_name':emp.employee_name,})
    return leave_info

@frappe.whitelist()
def get_presenty():
    return  frappe.db.sql("""
                    SELECT  employee_name, time , log_type, work_from
                    from `tabEmployee Checkin`
                    where date(time) BETWEEN date(%(today)s) AND date(%(today)s)
                    AND log_type="IN"
                    group by employee
                    order by time asc
                    """,
                    {"today":frappe.utils.format_date(frappe.utils.nowdate(),'YYYY-MM-dd')},as_dict=1)

@frappe.whitelist()
def members_on_leave():
    pass

@frappe.whitelist()
def members_in_office_status():
    employees = get_active_employees()
    emp_in_office = []
    emp_out_of_office = []
    emp_absent = []
    for employee in employees:
        emp_checkin = frappe.db.sql("""
                            SELECT  `tabEmployee Checkin`.employee_name, 
                                    `tabEmployee Checkin`.time , 
                                    `tabEmployee Checkin`.log_type, 
                                    `tabEmployee Checkin`.work_from,
                                    `tabEmployee`.branch
                            from `tabEmployee Checkin`
                            left join
                            `tabEmployee`
                            on `tabEmployee`.name = `tabEmployee Checkin`.employee
                            where date(`tabEmployee Checkin`.time) BETWEEN date(%(today)s) AND date(%(today)s)
                            AND `tabEmployee Checkin`.employee = %(employee)s
                            AND `tabEmployee Checkin`.work_from = "Office"
                            order by date(time)
                            """,
                            {"today":frappe.utils.format_date(frappe.utils.nowdate(),'YYYY-MM-dd'),"employee":employee.name},as_dict=1)

        if emp_checkin:
            if emp_checkin[-1]['log_type'] == "IN":
                emp_in_office.append(employee)
            else:
                emp_out_of_office.append(employee)
        else:
            emp_absent.append(employee)
            print(emp_absent)
    return {
            "emp_absent":emp_absent,
            "emp_out_of_office":emp_out_of_office,
            "emp_in_office":emp_in_office
            }

# @frappe.whitelist()
# def eom_report_data():
#     report_name = 'End Of Month Attendance'
#     filters= { 'month': "July", 'year': "2023", 'company': "ALUMIL SYSTEMS INDIA PVT LTD" }
#     data = frappe.desk.query_report.run(report_name, filters)
#     return data

@frappe.whitelist()
def eom_report_data():
    data = run(
                report_name='End Of Month Attendance',
                filters={'month': str(frappe.utils.now_datetime().month), 'year': str(frappe.utils.now_datetime().year), 'company': frappe.utils.get_defaults()['company']}
            )
    # data = get_data({})
    return data

@frappe.whitelist()
def total_working_hours_data():
    data = run(
                report_name='Total Working Hours'
            )
    # data = get_data({})
    return data

@frappe.whitelist()
def leave_report_data():
    data = run(
                report_name='Employee Leave Balance Summary',
                filters={'date': frappe.utils.nowdate(), 'company': frappe.utils.get_defaults()['company']}
            )
    # data = get_data({})
    return data

@frappe.whitelist()
def leave_details():
    employee = get_employee_from_user()['Name']
    data = get_leave_details(employee,frappe.utils.nowdate())
    result = []
    leave_allocation_data =frappe._dict({})
    for row in data.get('leave_allocation'):
        for k,v in data['leave_allocation'][row].items():
            leave_allocation_data[splitCapitalize(k)] = v
        data['leave_allocation'][row] = leave_allocation_data
    return data

@frappe.whitelist()
def session_defaults():
    return frappe.utils.get_defaults()