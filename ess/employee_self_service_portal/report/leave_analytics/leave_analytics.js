// Copyright (c) 2016, fitsterp and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Leave Analytics"] = {
	"filters": [
		{
			fieldname:"employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee"
		}
	]
};
