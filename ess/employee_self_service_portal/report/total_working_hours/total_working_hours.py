# Copyright (c) 2013, fitsterp and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import cint, get_datetime, flt

def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters)
    print("Printing Data")
    print(data)
    return columns, data

def get_columns(filters=None):
	return [
		{
			"label": _("Date"),
			"fieldtype": "Date",
			"fieldname": "attendance_date",
			"width": 90
		},
		{
			"label": _("Employee"),
			"fieldtype": "Link",
			"fieldname": "employee",
			"options": "Employee",
			"width": 100
		},
		{
			"label": _("Shift"),
			"fieldtype": "Data",
			"fieldname": "shift",
			"width": 100
		},
		{
			"label": _("Shift Length"),
			"fieldtype": "Float",
			"fieldname": "expected_working_hours",
			"width": 100
		},
		{
			"label": _("Worked Hours"),
			"fieldtype": "Float",
			"fieldname": "working_hours",
			"width": 100
		},
		{
			"label": _("Punch In"),
			"fieldtype": "Time",
			"fieldname": "in_time",
			"width": 100
		},
		{
			"label": _("Punch Out"),
			"fieldtype": "Time",
			"fieldname": "out_time",
			"width": 100
		},
		{
			"label": _("Overtime/Deficit"),
			"fieldtype": "Float",
			"fieldname": "overtime",
            "precision":2,
			"width": 90
		},
		{
			"label": _("Late Entry"),
			"fieldtype": "Check",
			"fieldname": "late_entry",
			"width": 90
		},
		{
			"label": _("Early Exit"),
			"fieldtype": "Check",
			"fieldname": "early_exit",
			"width": 90
		}
	]

def get_conditions(filters):
	conditions = ''
	if filters.get('employee'):
		conditions += "AND employee = %s" %frappe.db.escape(filters.employee)

	return conditions

def time_diff_in_hours(start, end):
    return round((end-start).total_seconds() / 3600, 1)

def get_data(filters=None):
    conditions = get_conditions(filters)
    attendance = frappe.db.sql('''select
                                        attendance_date,
                                        shift,
                                        employee,
                                        check_in_date_time,
                                        check_out_datetime,
                                        late_entry,
                                        early_exit,
                                        date_format(check_in_date_time, '%H:%i:%s') as 'in_time',
                                        date_format(check_out_datetime, '%H:%i:%s') as 'out_time'
                                        from `tabAttendance` where docstatus =1 {0} order by attendance_date DESC'''.format(conditions),as_dict=True)
    # attendance = frappe.db.sql('''select attendance_date, shift,employee, check_in_date_time, check_out_datetime, late_entry, early_exit from `tabAttendance` where docstatus =1 {0}'''.format(conditions),as_dict=True)
    list(map(update_shift_details, attendance))
    return attendance

def update_shift_details(attendance_dict):
    shift_time_in_hours = 0.0
    # get shift start and end time
    shift_start_time = frappe.db.get_value("Shift Type",attendance_dict['shift'],'start_time')
    shift_end_time = frappe.db.get_value("Shift Type",attendance_dict['shift'],'end_time')
    # calculate shift length if shift start and end time exists
    if shift_start_time and shift_end_time:
        shift_time_in_hours = time_diff_in_hours(shift_start_time,shift_end_time)
        attendance_dict['expected_working_hours'] = shift_time_in_hours
    else:
        attendance_dict['expected_working_hours'] = 0.0
        # attendance_dict['shift_time_in_hours'] = shift_time_in_hours
    # get pun in and punch out time
    checkin_time = attendance_dict.get('check_in_date_time')
    checkout_time = attendance_dict.get('check_out_datetime')
    # if checkin out both exists calculate worked hours
    if checkin_time and checkout_time:
        attendance_dict['working_hours'] = time_diff_in_hours(checkin_time,checkout_time)
    else:
        attendance_dict['working_hours'] = 0.0

    # get working hour deviation
    attendance_dict['overtime'] = attendance_dict['working_hours'] -attendance_dict['expected_working_hours']
    # update overtime / deficit
