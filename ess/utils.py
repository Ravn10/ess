import frappe

def jinja_methods(doctype,name,template):
    document = frappe.get_doc(doctype,name)
    return frappe.render_template(template,document.as_dict())
    # return "Hello!!"
