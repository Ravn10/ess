// Copyright (c) 2016, fitsterp and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Total Working Hours"] = {
	"filters": [
        {
			fieldname:"employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee"
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data.overtime >0) {
			value = $(`<span>${value}</span>`);
				var $value = $(value).css("font-weight", "bold");
                $value.addClass("text-success");
				if (data[column.fieldname] > 0) {
				}

				value = $value.wrap("<p></p>").parent().html();

		}
        else if (data.overtime <0) {
			value = $(`<span>${value}</span>`);
				var $value = $(value).css("font-weight", "bold");
                $value.addClass("text-danger");
				if (data[column.fieldname] > 0) {
				}

				value = $value.wrap("<p></p>").parent().html();

		}
		return value;
	}
};
