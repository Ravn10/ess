import frappe
from frappe.utils import get_link_to_form, now_datetime

@frappe.whitelist()
def get_employee_details(employee):
    if frappe.db.exists("Employee",employee):
        emp_details = frappe.db.sql('''select * from `tabEmployee` where name =%s ''',employee,as_dict=True)[0]
        # get employee leave balances
        # get holidays for this month

        return emp_details
    else:
        return []

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
