import frappe
from hrms.hr.doctype.upload_attendance.upload_attendance import get_active_employees
from frappe.utils import nowdate, get_first_day


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
                    {"today":nowdate()},as_dict=1)

@frappe.whitelist()
def members_on_leave():
    pass
