frappe.call({
    method: "frappe.desk.query_report.run",
    async: false,
    args: {
        report_name:'Total Working Hours'
    }
}).then(r => {
    console.log(r.message.columns)
    const datatable_options = {
        columns: r.message.columns,
        data: r.message.result,
        dynamicRowHeight: true,
        checkboxColumn: false,
        inlineFilters: true,
    };
    datatable = new frappe.DataTable(
        // this.$reconciliation_tool_dt.get(0),
        datatable_options
    );
    let find = document.querySelector('.report-container');
    let html = datatable;
    let div = document.createElement('div');
    div.innerHTML = html;
    find.appendChild(div);
})


callback: function(r) {
    console.log(r.message)
    const datatable_options = {
        columns: r.message.columns,
        data: r.message.result,
        dynamicRowHeight: true,
        checkboxColumn: false,
        inlineFilters: true,
    };
    datatable = new frappe.DataTable(
        // this.$reconciliation_tool_dt.get(0),
        datatable_options
    );
    let find = document.querySelector('.report-container');
    // let html = frappe.render_template("ess_table",{data:r.message['leave_allocation']});
    let div = document.createElement('div');
    div.innerHTML = datatable;
    find.appendChild(div);
}



frappe.call({
    method: "frappe.desk.query_report.run",
    async: false,
    args: {
        report_name:'Total Working Hours'
    }
}).then(r => {
    console.log("values")
    var res = []
    array.forEach(element => {

    });
    r.message.forEach(c => {
    if(typeof c === 'object') {
        console.log(Object.values(c))
        res.push(Object.values(c))
        }
    else{
        res.push(c)
    }
    console.log("print res")
    console.log(res)
})

})


frappe.call({
    method: "frappe.desk.query_report.run",
    async: false,
    args: {
        report_name:'Total Working Hours'
    }
}).then(r => {
    console.log("values")
    var res = []
    r.message.result.forEach(c => {
    if(typeof c === 'object') {
        console.log(Object.values(c))
        res.push(Object.values(c))
        }
    else{
        res.push(c)
    }
    console.log("print res")
    console.log(res)
})

})
