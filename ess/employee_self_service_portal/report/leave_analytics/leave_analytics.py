# Copyright (c) 2013, fitsterp and contributors
# For license information, please see license.txt

# import frappe
# Copyright (c) 2013, fitsterp and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import cint, get_datetime

def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters)
    print("Printing Data")
    print(data)
    return columns, data

def get_conditions(filters):
	conditions = ''
	if filters.get('employee'):
		conditions += "AND employee = %s" %frappe.db.escape(filters.employee)

	return conditions

def get_data(filters=None):
    conditions = get_conditions(filters)
    leave_application = frappe.db.sql('''select leave_type, from_date,to_date, total_leave_days, status, description, leave_approver from `tabLeave Application` where docstatus =1 {0}'''.format(conditions),as_dict=True)
    return leave_application


def get_columns(filters=None):
	return [
		{
			"label": _("Leave Type"),
			"fieldtype": "Data",
			"fieldname": "leave_type",
			"width": 120
		},
		{
			"label": _("From"),
			"fieldtype": "Date",
			"fieldname": "from_date",
			"width": 100
		},
		{
			"label": _("To"),
			"fieldtype": "Date",
			"fieldname": "to_date",
			"width": 100
		},
		{
			"label": _("No Of Days"),
			"fieldtype": "Float",
			"fieldname": "total_leave_days",
			"width": 50
		},
		{
			"label": _("Reason"),
			"fieldtype": "Data",
			"fieldname": "description",
			"width": 100
		},
		{
			"label": _("Status"),
			"fieldtype": "Data",
			"fieldname": "status",
			"width": 100
		},
		
		{
			"label": _("Approved By"),
			"fieldtype": "Link",
			"fieldname": "leave_approver",
			"options":"User",
			"width": 140
		}
	]






