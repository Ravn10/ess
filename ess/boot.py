import frappe
from frappe import _

def boot_session(bootinfo):
    if frappe.session.user:
        frappe.msgprint(_(frappe.session.user))
        employee_docname = frappe.db.exists(
            {'doctype': 'Employee', 'user_id': frappe.session.user})
        if employee_docname:
            # frappe.db.exists returns a tuple of a tuple
            emp = frappe.get_doc('Employee', employee_docname[0][0])
            frappe.msgprint(_(emp.employee))
            bootinfo.employee = emp.employee
            bootinfo.department = emp.department
