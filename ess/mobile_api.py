import frappe
from frappe import auth
from erpnext import get_default_company

@frappe.whitelist( allow_guest = True)
def login(usr, pwd):
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()
    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response["message"] = {
            "success_key":False,
            "message":"Authentication Error!"
        }

        return

    api_generate = custom_generate_keys(frappe.session.user)

    frappe.error_log("Api Key",api_generate)
    frappe.response["message"] = {
        "success_key":True,
        "message":"Authentication success",
        "sid":frappe.session.sid,
        "api_key":frappe.db.get_value("User",frappe.session.user,"api_key"),
        "api_secret":api_generate
    }

@frappe.whitelist(allow_guest=True)
def custom_generate_keys(user):
    user_details = frappe.get_doc('User', user)
    api_secret = frappe.generate_hash(length=15)

    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        frappe.db.set_value("User",user,"api_key",api_key)
        user_details.api_key = api_key

    frappe.db.set_value("User",user,"api_secret",api_secret)
    frappe.db.commit()

    return api_secret
