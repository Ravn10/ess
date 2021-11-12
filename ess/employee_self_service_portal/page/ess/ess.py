import frappe
from frappe.utils import get_link_to_form, now_datetime, nowdate, get_first_day, get_last_day
from frappe import _

@frappe.whitelist()
def get_employee_details(employee):
    if frappe.db.exists("Employee",employee):
        emp_details = frappe.db.sql('''select * from `tabEmployee` where name =%s ''',employee,as_dict=True)[0]
        # get employee leave balances
        # get holidays for this month
        emp_details.is_hr = frappe.db.get_value("Designation",emp_details.designation,'hr')
        if emp_details.is_hr:
            emp_details.admin_section = get_hr_admin_data()
        emp_details.connections = get_connections(employee)
        emp_details.approvals = get_approval_doc()
        return emp_details
    else:
        return []

def get_connections(employee):
    connections = []
    _connections = frappe.db.get_all('Global Search DocType',filters={'parent':'ESS Portal Setting'},fields=['document_type'])
    if _connections:
        connections = [list(x.values())[0] for x in _connections]
    return connections

@frappe.whitelist()
def checkin(employee,log_type):
    checkin_doc = frappe.new_doc("Employee Checkin")
    checkin_doc.employee = employee
    checkin_doc.log_type = log_type
    checkin_doc.time = now_datetime()
    try:
        checkin_doc.insert()
        checkin_link = get_link_to_form("Employee Checkin",checkin_doc.name)
        frappe.msgprint("{0} Created".format(checkin_link))
        return checkin_link
    except:
        error_log = frappe.log_error(frappe.get_traceback())
        error_log_link = get_link_to_form("Error Log",error_log.name)
        frappe.msgprint("{0} Created".format(error_log_link))
        return error_log_link

@frappe.whitelist()
def holiday_for_month(employee):
    holiday_list = frappe.db.get_value("Employee",employee,"holiday_list")
    month_first_date = get_first_day(nowdate())
    month_last_date = get_last_day(nowdate())
    frappe.db.get_value("Employee",employee,"holiday_list")
    months_holidays = frappe.db.sql('''
              select holiday_date, description
              from `tabHoliday`
              where holiday_date >= %(from)s and holiday_date <= %(to)s
              and parent = %(holiday_list)s
              order by holiday_date asc
              ''',{
                  "from":month_first_date,
                  "to":month_last_date,
                  "holiday_list":holiday_list
                  },as_dict=True)
    def get_day(data):
        print(data)
        data['day'] = data['holiday_date'].day
    list(map(get_day,months_holidays))
    return months_holidays


@frappe.whitelist()
def create_leave_application(info):
    info = frappe.parse_json(info)
    keys = ['employee','from_date','to_date','leave_approver','status','description']

    for key in keys:
        if key not in info:
            info[key] = None

    leave_application_doc = frappe.new_doc("Leave Application")
    leave_application_doc.update(info)
    leave_application_doc.leave_approver = frappe.get_value("Employee","HR-EMP-00001","leave_approver")
    try:
        leave_application_doc.insert()
        leave_application_doc_link = get_link_to_form("Leave Application",leave_application_doc.name)
        frappe.msgprint("{0} Created".format(leave_application_doc_link))
        return leave_application_doc_link
    except:
        error_log = frappe.log_error(frappe.get_traceback())
        error_log_link = get_link_to_form("Error Log",error_log.name)
        frappe.msgprint("{0} Created".format(error_log_link))
        return error_log_link

@frappe.whitelist()
def get_checkin(employee):
    today = nowdate()
    checkin_for_the_day = frappe.db.sql("""
                                        SELECT name, time , log_type
                                        from `tabEmployee Checkin`
                                        where date(time) BETWEEN date(%(today)s) AND date(%(today)s)
                                        AND log_type="IN"
                                        AND employee =%(employee)s
                                        order by time asc
                                        """,
                                        {"today":today,"employee":employee},as_dict=1)
    checkout_for_the_day = frappe.db.sql("""
                                        SELECT name, time , log_type
                                        from `tabEmployee Checkin`
                                        where date(time) BETWEEN date(%(today)s) AND date(%(today)s)
                                        AND log_type="OUT"
                                        AND employee =%(employee)s
                                        order by time asc
                                        """,
                                        {"today":today,"employee":employee},as_dict=1)
    check_in_out = {"checkin":checkin_for_the_day,"checkout":checkout_for_the_day,"checkin_count":len(checkin_for_the_day),"checkout_count":len(checkout_for_the_day)}
    return check_in_out

@frappe.whitelist()
def get_employee_with_birthday_this_month():
    conditions = ""
    month = frappe.utils.now_datetime().month
    conditions += " and month(date_of_birth) = '%s'" % month
    birthday_persons = frappe.db.sql("""select name, employee_name, date_of_birth
                                     from tabEmployee
                                     where status = 'Active' %s
                                     order by date_of_birth asc""" % conditions, as_dict=1)
    def get_day(data):
        print(data)
        data['day'] = data['date_of_birth'].day
    list(map(get_day,birthday_persons))
    return birthday_persons

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
        data['from'] = data['from_date'].day
        data['to'] = data['to_date'].day
    list(map(get_day,leave_info))
    return leave_info

def on_login():
    # frappe.msgprint(_(frappe.session.user))
    # frappe.local.flags.redirect_location = "/ess/"
    # frappe.local.response["location"] =  frappe.utils.get_url("/ess/")
    # frappe.msgprint(_(frappe.session.user))
    if frappe.session.user:
        frappe.msgprint(_(frappe.session.user))
        employee_docname = frappe.db.exists(
            {'doctype': 'Employee', 'user_id': frappe.session.user})
        if employee_docname:
            # frappe.db.exists returns a tuple of a tuple
            emp = frappe.get_doc('Employee', employee_docname[0][0])
            frappe.msgprint(_(emp.employee))
    #         frappe.local.flags.redirect_location = "/ess/"
    #         raise frappe.Redirect
    # else:
    #     frappe.msgprint("Couldn't Get your name")

@frappe.whitelist()
def get_approval_doc():
    approvals = []
    leave_applications = len(frappe.db.get_all("Leave Application",filters={'leave_approver':frappe.session.user,'status':'Open'}))
    todo = len(frappe.db.get_all("ToDo",filters={'owner':frappe.session.user,'status':'Open'}))
    claim = len(frappe.db.get_all("Expense Claim",filters={'expense_approver':frappe.session.user,'status':'Draft'}))
    return {"Leave Application":leave_applications,"ToDo":todo,"Expense Claim":claim}

@frappe.whitelist()
def get_hr_admin_data():
    head_count = frappe.db.count('Employee',{"status":"Active"})
    new_joiners =frappe.db.count('Job Applicant',{"status":"Accepted"})
    exits = frappe.db.sql('''select count(*) as count from `tabEmployee Separation` where boarding_status in ("Pending","In Process")''',as_dict=True)[0]['count'] #frappe.db.count('Employee Separation',{"status":["in",["Pending","In Process"]]})
    present = frappe.db.count('Attendance',{"status":"Present","attendance_date":frappe.utils.get_datetime().date()})
    on_leave = frappe.db.count('Attendance',{"status":"On Leave","attendance_date":frappe.utils.get_datetime().date()})
    on_duty = frappe.db.count('Attendance',{"status":"Work From Home","attendance_date":frappe.utils.get_datetime().date()})
    return {
                "head_count" : head_count,
                "new_joiners" : new_joiners,
                "exits" : exits,
                "present" : present,
                "on_leave" : on_leave,
                "on_duty" : on_duty
            }
