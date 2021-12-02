import frappe

@frappe.whitelist()
def get_employee_details(employee):
    return frappe.get_all("Employee",filters={'name':employee},fields=['name','employee_name','status','image'])
