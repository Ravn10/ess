# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
from calendar import month
from erpnext.hr.doctype.employee.employee import deactivate_sales_person
import frappe
from frappe.utils import getdate, nowdate
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate, get_link_to_form, \
	comma_or, get_fullname, add_days, nowdate, get_datetime_str
from frappe.utils import cstr, get_datetime, formatdate
from erpnext.hr.doctype.employee.employee import is_holiday
from datetime import timedelta, date
from datetime import datetime, timedelta
from datetime import date, time, datetime, timedelta
from frappe.utils import now
from frappe.utils import flt, now_datetime
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate, get_link_to_form, \
	comma_or, get_fullname, add_days, nowdate, get_datetime_str

class Attendance(Document):
	def validate(self):
		from erpnext.controllers.status_updater import validate_status
		validate_status(self.status, ["Present", "Absent", "On Leave", "On Duty (OD)", "Half Day", "Work From Home"])
		self.validate_attendance_date()
		self.validate_duplicate_record()
		self.check_leave_record()
		self.validate_attn_req()
		###Custom code for sending notification mail to reporting manager to approve the attendance record. once record gets submitted
		self.notification()

	def notification(self):
		if self.workflow_state == 'Submitted' and self.status != "On Duty (OD)":
			parent_doc = frappe.get_doc('Attendance', self.name)
			args = parent_doc.as_dict()

			#template = frappe.db.get_single_value('HR Settings', 'leave_approval_notification_template')
			#if not template:
			#	frappe.msgprint(_("Please set default template for Leave Approval Notification in HR Settings."))
			#	return
			mail_list = []
			reports_to = frappe.db.get_value('Employee',self.employee,'reports_to')
			la_approver = frappe.db.get_value('Employee',reports_to,'user_id')
			if la_approver not in mail_list:
				mail_list.append(la_approver)

			if self.attendance_approver not in mail_list:
				mail_list.append(self.attendance_approver)

			role_list = frappe.get_all("Has Role",filters={"role": "HR Manager", "parenttype": "User"},fields="parent")
			for k in role_list:
				if ((k.parent not in mail_list) and (k.parent != 'Administrator')):
					mail_list.append(k.parent)

			email_template = frappe.get_doc("Email Template", 'Attendance Regularization Approval')
			message = frappe.render_template(email_template.response, args)

			for l in mail_list:
				self.notify({
					# for post in messages
					"message": message,
					"message_to": l,
					# for email
					"subject": email_template.subject
				})

		if self.workflow_state == 'Pending Review':
			user_id = frappe.db.get_value("Employee",self.employee,'user_id')
			parent_doc = frappe.get_doc('Attendance', self.name)
			args = parent_doc.as_dict()

			email_template = frappe.get_doc("Email Template", 'Attendance Correction')
			message = frappe.render_template(email_template.response, args)


			self.notify({
				# for post in messages
				"message": message,
				"message_to": user_id,
				# for email
				"subject": email_template.subject
			})

	def notify(self, args):
		print('called')
		args = frappe._dict(args)
		# args -> message, message_to, subject
		if cint(self.follow_via_email):
			contact = args.message_to
			if not isinstance(contact, list):
				if not args.notify == "employee":
					print('IN')
					contact = frappe.get_doc('User', contact).email or contact
					print('CON '+str(contact))

			sender      	    = dict()
			sender['email']     = frappe.get_doc('User', frappe.session.user).email
			sender['full_name'] = frappe.utils.get_fullname(sender['email'])

			try:
				frappe.sendmail(
					recipients = contact,
					sender = sender['email'],
					subject = args.subject,
					message = args.message,
				)
				frappe.msgprint(_("Email sent to {0}").format(contact))
			except frappe.OutgoingEmailError:
				pass


	def validate_attendance_date(self):
		date_of_joining = frappe.db.get_value("Employee", self.employee, "date_of_joining")

		# leaves can be marked for future dates
		if self.status in ('Absent','Present','Half Day', 'Quarter Day','Work From Home') and self.absence_type in ('Forgot to punch', 'Machine fault', 'Injury in hand', 'Access card not working', 'Other') and not self.leave_application and getdate(self.attendance_date) > getdate(nowdate()):
			frappe.throw(_("Attendance can not be marked for future dates"))
		elif date_of_joining and getdate(self.attendance_date) < getdate(date_of_joining):
			frappe.throw(_("Attendance date can not be less than employee's joining date"))

	def validate_attn_req(self):
		if self.status == "On Duty (OD)":
			if not self.on_duty_reason:
				frappe.throw("On Duty Reason is mandatory.")
			if not self.from_date and not self.to_date:
				frappe.throw("From Date and To Date is mandatory.")
			if self.from_date and not self.to_date:
				frappe.throw("To Date is mandatory.")
			if not self.from_date and self.to_date:
				frappe.throw("From Date is mandatory.")

			if self.on_duty_reason == "Vessel Visit" and not self.vessel_visit_name:
				frappe.throw("Vessel Name is mandatory.")

			if self.half_day == 1 and not self.half_day_date:
				frappe.throw('Half Day Date is mandatory.')

			#validate_dates(self, self.from_date, self.to_date)
			if self.half_day:
				if not getdate(self.from_date)<=getdate(self.half_day_date)<=getdate(self.to_date):
					frappe.throw(_("Half day date should be in between from date and to date"))

			###Backdated Request cannot be selected
			backdate = frappe.db.get_single_value("Leave Management Settings", "restrict_backdated_leave_application")
			today = date.today()
			if backdate == 1 and getdate(self.from_date) < today and "HR Manager" not in frappe.get_roles(frappe.session.user):
				frappe.throw("Backdated can't be selected ")

			###Backdated Limit Validation
			backdate_limit = frappe.db.get_single_value("Leave Management Settings", 'backdated_limit')
			if backdate == 0:
				date_val = frappe.db.sql("""select Count(name), posting_date, from_date from `tabAttendance` where
					MONTH(posting_date) = MONTH(%s) and employee = %s """,(self.posting_date,self.employee))

				for i in date_val:
					if i[0] > backdate_limit:
						frappe.throw('Backdated Entries Crossed the Limit days '+str(backdate_limit))

			###Future Attendance Request entry validation should not cross value that mentioned in settings
			futrdays = frappe.db.get_single_value("Leave Management Settings", "future_days_at_req")
			d = today + timedelta(days=futrdays)

			days_diff = date_diff(d,self.from_date)
			###Future planned leave validation
			if futrdays < (abs(days_diff)):
				frappe.throw("Future date entries can be for maximum of  " + str(futrdays) +  " days only.")


			###custom code #On Submit of Attendance Request notification mail sent to leave approver
			if self.workflow_state == 'Submitted':
				parent_doc = frappe.get_doc('Attendance', self.name)
				args = parent_doc.as_dict()

				rc = []
				reports_to = frappe.db.get_value('Employee',self.employee,'reports_to')
				la_approver = frappe.db.get_value('Employee', reports_to, 'user_id')
				if la_approver not in rc:
					rc.append(la_approver)

				if self.attendance_approver not in rc:
					rc.append(self.attendance_approver)

				email_template = frappe.get_doc("Email Template", 'Attendance Request Approval')
				message = frappe.render_template(email_template.response, args)

				for j in rc:
					self.notify({
						# for post in messages
						"message": message,
						"message_to": j,
						# for email
						"subject": email_template.subject
					})

			###Approval of attendance request record send mail to corresponding employee who applied the attendance request
			if self.workflow_state == 'Approved':
				subj = 'Attendance Approved Notification '
				notification_message = 'Attendance has been Approved - <a href="desk#Form/Attendance/{0}" target="_blank">{1}</a> \
					for employee  {2} .'.format(self.name, self.name, self.employee_name)

				mail = frappe.db.get_value('Employee',self.employee,'user_id')
				frappe.sendmail(mail,subject=subj,\
					message = notification_message)

			if self.workflow_state == 'Rejected':
				subj = 'Attendance Rejected Notification '
				notification_message = 'Attendance has been Rejected - <a href="desk#Form/Attendance/{0}" target="_blank">{1}</a> \
					for employee  {2} .'.format(self.name, self.name, self.employee_name)

				mail = frappe.db.get_value('Employee',self.employee,'user_id')
				frappe.sendmail(mail,subject=subj,\
					message = notification_message)

			#if self.docstatus == '2':
			#	self.on_cancel

		if self.status != "On Duty (OD)":
			if not self.attendance_date:
				frappe.throw("Attendance Date is mandatory.")

	def on_submit(self):
		if self.status == 'On Duty (OD)':
			self.create_attendance()

	def create_attendance(self):
		request_days = date_diff(self.to_date, self.from_date) + 1
		for number in range(request_days):
			attendance_date = add_days(self.from_date, number)
			skip_attendance = self.validate_if_attendance_not_applicable(attendance_date)
			if not skip_attendance:
				attendance = frappe.new_doc("Attendance")
				attendance.employee = self.employee
				attendance.employee_name = self.employee_name
				if self.half_day and date_diff(getdate(self.half_day_date), getdate(attendance_date)) == 0:
					attendance.status = "Half Day"
				#elif self.reason == "Work From Home":
				#	attendance.status = "Work From Home"
				elif self.status == "On Duty (OD)":
					attendance.status = "On Duty (OD)"
					attendance.on_duty_reason = self.on_duty_reason
					attendance.vessel_visit_name = self.vessel_visit_name
					attendance.explanation = self.explanation
				else:
					attendance.status = "Present"
				attendance.attendance_date = attendance_date
				attendance.company = self.company
				#attendance.attendance_request = self.name
				attendance.save(ignore_permissions=True)
				attendance.submit()

	#def on_cancel(self):
	#	attendance_list = frappe.get_list("Attendance", {'employee': self.employee, 'attendance_request': self.name})
	#	if attendance_list:
	#		for attendance in attendance_list:
	#			attendance_obj = frappe.get_doc("Attendance", attendance['name'])
	#			attendance_obj.cancel()


	def validate_if_attendance_not_applicable(self, attendance_date):
		# Check if attendance_date is a Holiday
		if is_holiday(self.employee, attendance_date):
			frappe.msgprint(_("Attendance not submitted for {0} as it is a Holiday.").format(attendance_date), alert=1)
			return True

		# Check if employee on Leave
		leave_record = frappe.db.sql("""select half_day from `tabLeave Application`
			where employee = %s and %s between from_date and to_date
			and docstatus = 1""", (self.employee, attendance_date), as_dict=True)
		if leave_record:
			frappe.msgprint(_("Attendance not submitted for {0} as {1} on leave.").format(attendance_date, self.employee), alert=1)
			return True

		return False


	def validate_duplicate_record(self):
		if self.status != "On Duty (OD)":
			res = frappe.db.sql("""
				select name from `tabAttendance`
				where employee = %s
					and attendance_date = %s
					and name != %s
					and docstatus != 2
				""", (self.employee, getdate(self.attendance_date), self.name))
			if res:
				frappe.throw(_("Attendance for employee {0} is already marked for the date {1}").format(
					frappe.bold(self.employee), frappe.bold(self.attendance_date)))

	def check_leave_record(self):
		leave_record = frappe.db.sql("""
			select leave_type, half_day, half_day_date
			from `tabLeave Application`
			where employee = %s
				and %s between from_date and to_date
				and status = 'Approved'
				and docstatus = 1
		""", (self.employee, self.attendance_date), as_dict=True)
		if leave_record:
			for d in leave_record:
				self.leave_type = d.leave_type
				if d.half_day_date == getdate(self.attendance_date):
					self.status = 'Half Day'
					frappe.msgprint(_("Employee {0} on Half day on {1}")
						.format(self.employee, formatdate(self.attendance_date)))
				else:
					self.status = 'On Leave'
					frappe.msgprint(_("Employee {0} is on Leave on {1}")
						.format(self.employee, formatdate(self.attendance_date)))

		if self.status in ("On Leave", "Half Day"):
			if not leave_record:
				frappe.msgprint(_("No leave record found for employee {0} on {1}")
					.format(self.employee, formatdate(self.attendance_date)), alert=1)
		elif self.leave_type:
			self.leave_type = None
			self.leave_application = None

	def validate_employee(self):
		emp = frappe.db.sql("select name from `tabEmployee` where name = %s and status = 'Active'",
		 	self.employee)
		if not emp:
			frappe.throw(_("Employee {0} is not active or does not exist").format(self.employee))

@frappe.whitelist()
def get_events(start, end, filters=None):
	events = []

	employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user})

	if not employee:
		return events

	from frappe.desk.reportview import get_filters_cond
	conditions = get_filters_cond("Attendance", filters, [])
	add_attendance(events, start, end, conditions=conditions)
	return events

def add_attendance(events, start, end, conditions=None):
	query = """select name, attendance_date, status
		from `tabAttendance` where
		attendance_date between %(from_date)s and %(to_date)s
		and docstatus < 2"""
	if conditions:
		query += conditions

	for d in frappe.db.sql(query, {"from_date":start, "to_date":end}, as_dict=True):
		e = {
			"name": d.name,
			"doctype": "Attendance",
			"start": d.attendance_date,
			"end": d.attendance_date,
			"title": cstr(d.status),
			"docstatus": d.docstatus
		}
		if e not in events:
			events.append(e)

def mark_attendance(employee, attendance_date, status, shift=None, leave_type=None, ignore_validate=False):
	if not frappe.db.exists('Attendance', {'employee':employee, 'attendance_date':attendance_date, 'docstatus':('!=', '2')}):
		company = frappe.db.get_value('Employee', employee, 'company')
		attendance = frappe.get_doc({
			'doctype': 'Attendance',
			'employee': employee,
			'attendance_date': attendance_date,
			'status': status,
			'company': company,
			'shift': shift,
			'leave_type': leave_type
		})
		attendance.flags.ignore_validate = ignore_validate
		attendance.insert()
		attendance.submit()
		return attendance.name

@frappe.whitelist()
def get_atn_approver(employee):
	leave_approver, department = frappe.db.get_value("Employee",
		employee, ["leave_approver", "department"])

	if not leave_approver and department:
		leave_approver = frappe.db.get_value('Department Approver', {'parent': department,
			'parentfield': 'leave_approvers', 'idx': 1}, 'approver')

	return leave_approver

@frappe.whitelist()
def leave_app(doctype, txt, searchfield, start, page_len, filters):
  #  name = filters.get('parent_helpdesk_category')
#	a = []
#	l = frappe.db.sql("""select leave_approver from `tabEmployee` where leave_approver IS NOT NULL""",as_dict=1)
#	for i in l:
#		a.append(i.leave_approver)

#	dep = ' '.join(a).split()
	#frappe.msgprint("DEP" + str(l))
	#frappe.msgprint(str(dep))
#	if dep:
#		return l
	#if not dep:
	#	return frappe.db.sql("""select name from tabDepartment where name != 'All Departments'""")
	return frappe.db.sql("""select leave_approver from `tabEmployee` where leave_approver IS NOT NULL""",as_dict=1)


@frappe.whitelist()
def checkin_attendance_creation(data):
	import json
	if isinstance(data, str):
		data = json.loads(data)
	data = frappe._dict(data)
	checkin_from = ''
	if data.office == 1:
		checkin_from = "From Office"
	elif data.home == 1:
		checkin_from = "Work From Home"

	emp_check_in = frappe.new_doc("Employee Checkin")
	eid = frappe.db.sql("""select name,employee_name,company from `tabEmployee` where user_id = %s""",(frappe.session.user),as_dict=1)

	for i in eid:
		emp_check_in.employee = i.name
		emp_check_in.employee_name = i.employee_name
		emp_check_in.company = i.company
		emp_check_in.check_infrom = checkin_from
		from datetime import datetime
		# datetime object containing current date and time
		now = datetime.now()

		# dd/mm/YY H:M:S
		dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
		emp_check_in.check_in_date_time = dt_string
		emp_check_in.lg_in = 1
		emp_check_in.save()

		atn = frappe.new_doc("Attendance")
		atn.employee = 	emp_check_in.employee
		atn.checkin_from = emp_check_in.checkin_from
		atn.check_in_date_time = emp_check_in.check_in_date_time
		atn.employee_checkin = emp_check_in.name

		atn.employee_name = emp_check_in.employee_name
		atn.attendance_date = now.strftime("%Y-%m-%d")
		atn.status = "Present"
		atn.company = emp_check_in.company
		atn.flags.ignore_validate = True
		atn.insert(ignore_permissions=True)
		atn.submit()

@frappe.whitelist()
def checkout_attendance_updation(data):
	import json
	if isinstance(data, str):
		data = json.loads(data)
	data = frappe._dict(data)

	checkout_from = ''
	if data.office == 1:
		checkout_from = "From Office"
	elif data.home == 1:
		checkout_from = "Work From Home"

	eid = frappe.db.sql("""select name,employee_name,company from `tabEmployee` where user_id = %s""",(frappe.session.user),as_dict=1)

	for j in eid:
		emp = frappe.db.sql("""select name from `tabEmployee Checkin` where employee = %s""",(j.name),as_dict=1)

		for i in emp:
			e_check = frappe.get_doc("Employee Checkin", i.name)
			from datetime import datetime
			# datetime object containing current date and time
			now = datetime.now()

			# dd/mm/YY H:M:S
			dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
			e_check.check_out_date_time = dt_string
			e_check.lg_out = 1
			e_check.save()

			atn = frappe.db.sql("""update `tabAttendance` set check_out_datetime = %s, checkoutfrom = %s where employee_checkin = %s""",(dt_string,checkout_from,i.name))

@frappe.whitelist()
def mark_bulk_attendance(data):
	import json
	from pprint import pprint
	if isinstance(data, frappe.string_types):
		data = json.loads(data)
	data = frappe._dict(data)
	company = frappe.get_value('Employee', data.employee, 'company')
	if not data.unmarked_days:
		frappe.throw(_("Please select a date."))
		return

	for date in data.unmarked_days:
		doc_dict = {
			'doctype': 'Attendance',
			'employee': data.employee,
			'attendance_date': get_datetime(date),
			'status': data.status,
			'company': company,
		}
		attendance = frappe.get_doc(doc_dict).insert()
		attendance.submit()


def get_month_map():
	return frappe._dict({
		"January": 1,
		"February": 2,
		"March": 3,
		"April": 4,
		"May": 5,
		"June": 6,
		"July": 7,
		"August": 8,
		"September": 9,
		"October": 10,
		"November": 11,
		"December": 12
		})

@frappe.whitelist()
def get_unmarked_days(employee, month):
	print('called')
	import calendar
	month_map = get_month_map()

	today = get_datetime()

	dates_of_month = ['{}-{}-{}'.format(today.year, month_map[month], r) for r in range(1, calendar.monthrange(today.year, month_map[month])[1] + 1)]

	length = len(dates_of_month)
	month_start, month_end = dates_of_month[0], dates_of_month[length-1]


	records = frappe.get_all("Attendance", fields = ['attendance_date', 'employee'] , filters = [
		["attendance_date", ">=", month_start],
		["attendance_date", "<=", month_end],
		["employee", "=", employee],
		["docstatus", "!=", 2]
	])

	marked_days = [get_datetime(record.attendance_date) for record in records]
	unmarked_days = []

	for date in dates_of_month:
		date_time = get_datetime(date)
		if today.day == date_time.day and today.month == date_time.month:
			break
		if date_time not in marked_days:
			unmarked_days.append(date)

	return unmarked_days

@frappe.whitelist()
def payroll_cutoff_notify():
	receiver = []
	rec = []
	import datetime
	cur_date = date.today()
	x = cur_date.strftime("%d")

	payroll_days = frappe.db.get_single_value("Leave Management Settings", "attendance_payroll_cutoff")


	if x == payroll_days:
		attn_req = frappe.db.sql(""" select name, employee, employee_name, workflow_state from `tabAttendance`
			where docstatus=%s """, ("0"))


		subj = 'Payroll Cutoff Notification Reminder'
		content = 'Following Attendance is Pending for Your Approval:'
		content = """
				<table style="margin-left: auto; margin-right: auto;" border: 1px solid black>
				<tbody>
				<tr>
				<td>Name</td>
				<td>Employee Name</td>
				<td>Status</td>
				</tr>"""
		for i in attn_req:
			content = content +"""<tr>
				<td>"""+i[0]+"""</td>
				<td>"""+i[2]+"""</td>
				<td>"""+i[3]+"""</td>
				</tr>"""
		content = content + """ </tbody>
				</table>"""

		la_appr = frappe.db.get_value("Employee", i[1], 'leave_approver')
		rec.append(la_appr)
		for n in rec:
			frappe.sendmail(n,subject=subj,\
				message = content)


@frappe.whitelist()
def attendance_not_marked():
	#from datetime import datetime
	#now = datetime.now()
	#cur_month = str(now.month)
	#print(str(cur_month))

	#print(str(now))
	#offset = (4-now.weekday()) % 7
	#print('offset '+str(offset))
	#friday = now + timedelta(days=offset)
	#print(str(friday))

	#print (now.strftime("%Y-%m-%d %H:%M:00 %p"))
	#dt_time = now.strftime("%Y-%m-%d %H:%M:00 %p")

	#c = now.strftime("%Y-%m-%d 04:00:00 PM")
	#print("C "+str(c))
	#if now == friday and c == dt_time:
	emp_list = frappe.db.sql("""select name, employee_name, user_id from `tabEmployee` where status = %s""",('Active'),as_dict=1)
	print('EMP '+str(emp_list))
	for i in emp_list:
		import calendar
		month_map = cur_month

		today = get_datetime()

		dates_of_month = ['{}-{}-{}'.format(today.year, int(month_map), r) for r in range(1, calendar.monthrange(today.year, int(month_map))[1] + 1)]
		print('DM '+str(dates_of_month))
		length = len(dates_of_month)
		print('LEn '+str(length))
		month_start, month_end = dates_of_month[0], dates_of_month[length-1]
		print('MS '+str(month_start) + ' ME '+str(month_end))

		for j in dates_of_month:
			records = frappe.get_all("Attendance", fields = ['attendance_date', 'employee', 'name', 'follow_via_email'] , filters = [
				["attendance_date", ">=", j],
				["attendance_date", "<=", friday],
				["employee", "=", i.name],
				["docstatus", "!=", 2]
			])
			print('rec '+str(records))
			marked_days = [get_datetime(record.attendance_date) for record in records]
			print('MD '+str(marked_days))
			unmarked_days = []

			for date in dates_of_month:
				date_time = get_datetime(date)
				print('DDT '+str(date_time.day) + ' TO '+str(today.day))
				if today.day == date_time.day and today.month == date_time.month:
					break
				if date_time not in marked_days:
					unmarked_days.append(date)
				print('UD '+str(unmarked_days))

			for atn in records:
				parent_doc = frappe.get_doc('Attendance', atn.name)
				args = parent_doc.as_dict()
				email_template = frappe.get_doc("Email Template", 'Weekly absent status')
				message = frappe.render_template(email_template.response, args)
				mail_id = frappe.db.get_value('Employee',atn.employee,'user_id')

				parent_doc.notify({
						# for post in messages
						"message": message,
						"message_to": mail_id,
						# for email
						"subject": email_template.subject
				})


@frappe.whitelist()
def manager_attendance_not_approved():
	from datetime import datetime
	now = datetime.now()
	print('NOW '+str(now))
	cur_month = str(now.month)
	print(str(cur_month))

	print(str(now))
	offset = (2-now.weekday()) % 7
	print('offset '+str(offset))
	wednesday = now + timedelta(days=offset)
	print(str(wednesday))

	print (now.strftime("%Y-%m-%d %H:%M:00 %p"))
	dt_time = now.strftime("%Y-%m-%d %H:%M:00 %p")

	c = now.strftime("%Y-%m-%d 04:00:00 PM")
	print("C "+str(c))
	if now == wednesday and c == dt_time:
		attn_list = frappe.db.sql("""select name from `tabAttendance` where docstatus = '0' and workflow_state != %s""",('Approved'),as_dict=1)
		print('ATT '+str(attn_list))
		for i in attn_list:
			parent_doc = frappe.get_doc('Attendance', i.name)
			args = parent_doc.as_dict()
			la_approver = frappe.db.get_value('Employee',i.employee,'leave_approver')
			email_template = frappe.get_doc("Email Template", 'Attendance Regularization Manager Approval')
			message = frappe.render_template(email_template.response, args)

			parent_doc.notify({
				# for post in messages
				"message": message,
				"message_to": la_approver,
				# for email
				"subject": email_template.subject,
				"notify": la_approver
			})
###Notification to HR when employee has not marked attendance on two days of continued absence
#@frappe.whitelist()
#def attendance_leave():
#		emp_list = []
#		cr_date = getdate(now())
#		pre_date1 = (cr_date - timedelta(days = 1))
#		pre_date2 = (cr_date - timedelta(days = 2))
#		emp = frappe.db.sql("""select name,employee_name from `tabEmployee` where status = 'Active'""",as_dict=1)
#		for x in emp:
#			attendance_sheet1 = frappe.db.sql("""select name,attendance_date,employee,employee_name from `tabAttendance` where employee_name = %s and attendance_date = %s""",(x.employee_name,pre_date1),as_dict=1)
#			attendance_sheet2 = frappe.db.sql("""select name,attendance_date,employee,employee_name from `tabAttendance` where employee_name = %s and attendance_date = %s""",(x.employee_name,pre_date2),as_dict=1)
#			if not attendance_sheet1 and not attendance_sheet2 and cr_date:
#					role = frappe.db.get_value("Employee",x.name,'reports_to')
#					role_l = frappe.db.get_value("Employee", role, 'user_id')
#					if role_l not in emp_list:
#						emp_list.append(role_l)

#					role_list = frappe.get_all("Has Role",filters={"role": "HR Manager", "parenttype": "User"},fields="parent")
#					for k in role_list:
#						if ((k.parent not in emp_list) and (k.parent != 'Administrator')):
#							emp_list.append(k.parent)


			#from datetime import datetime
			#ow = datetime.now()
			#print('NOW '+str(now))
			#dt_time = now.strftime("%Y-%m-%d %H:%M:00 %p")

			#c = now.strftime("%Y-%m-%d 10:00:00 PM")
			#print("C "+str(c))
			#if c == dt_time:
		#	subj = 'Attendance Sheet Notification ' +  ' for ' + x.employee_name
		#	notification_message =  'Hi, Attendance sheet not yet filled for past two days'
		#	print(emp_list)
		#	for receiver in emp_list:
		#		frappe.sendmail(receiver,subject=subj,\
		#			message = notification_message)

@frappe.whitelist()
def weakly_leave_alert():
#	today = date.today()
#	print(str(today))
#	offset = (2-today.weekday()) % 7
#	print('offset '+str(offset))
#	wednesday = today + timedelta(days=offset)
#	print(str(wednesday))

#	from datetime import datetime
#	now = datetime.now()
#	print('NOW '+str(now))
#	cur_month = str(now.month)
#	print(str(cur_month))

#	print(str(now))
#	offset = (2-now.weekday()) % 7
#	print('offset '+str(offset))
#	wednesday = now + timedelta(days=offset)
#	print(str(wednesday))

#	print (now.strftime("%Y-%m-%d %H:%M:00 %p"))
#	dt_time = now.strftime("%Y-%m-%d %H:%M:00 %p")

#	c = now.strftime("%Y-%m-%d 04:00:00 PM")
#	print("C "+str(c))
#	if now == wednesday and c == dt_time:
	print('in if')
	act_leave_application = frappe.db.sql(""" select name, employee, employee_name, attendance_approver, status from `tabAttendance`
		where workflow_state=%s """, ("Submitted"), as_dict=True)
	print('la '+str(act_leave_application))


	for i in act_leave_application:
		parent_doc = frappe.get_doc('Attendance', i.name)
		args = parent_doc.as_dict()

		rc = []
		reports_to = frappe.db.get_value('Employee', parent_doc.employee,'reports_to')
		la_approver = frappe.db.get_value('Employee', reports_to, 'user_id')
		if not la_approver in rc:
			rc.append(la_approver)

		if not parent_doc.attendance_approver in rc:
			rc.append(parent_doc.attendance_approver)

		email_template = frappe.get_doc("Email Template", 'Weekly Attendance Request Approval')
		message = frappe.render_template(email_template.response, args)

		for j in rc:
			parent_doc.notify({
				# for post in messages
				"message": message,
				"message_to": j,
				# for email
				"subject": email_template.subject,
				"notify": j
			})

@frappe.whitelist()
def payroll_notify():
	receiver = []
	rec = []
	import datetime
	cur_date = date.today()
	print(str(cur_date))
	x = cur_date.strftime("%d")
	print(str(x))

	payroll_days = frappe.db.get_single_value("Leave Management Settings", "attendance_payroll_cutoff")
	print(str(payroll_days))

	if x == payroll_days:
		attn_req = frappe.db.sql(""" select name, employee, employee_name, docstatus, attendance_approver, status from `tabAttendance`
			where docstatus=%s """, ("0"))

		print('la '+str(attn_req))

		subj = 'Payroll Cutoff Notification Reminder'
		content = 'Following Attendance is Pending for Your Approval:'
		content = """
				<table style="margin-left: auto; margin-right: auto;" border: 1px solid black>
				<tbody>
				<tr>
				<td>Name</td>
				<td>Employee Name</td>
				</tr>"""
		for i in attn_req:
			content = content +"""<tr>
				<td>"""+i[0]+"""</td>
				<td>"""+i[2]+"""</td>
				</tr>"""
		content = content + """ </tbody>
				</table>"""



		if i[5] == 'On Duty (OD)':
			reports_to = frappe.db.get_value('Employee',i[1],'reports_to')
			la_approver = frappe.db.get_value('Employee', reports_to, 'user_id')
			if not la_approver in rc:
				rc.append(la_approver)

			if not i[4]:
				rc.append(i[4])

			for n in rec:
				print(str(n))
				frappe.sendmail(n,subject=subj,\
					message = content)
