<template>
    <div>
        <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-xl font-bold mb-4">Employee Self Service Portal</h2>
            <p class="text-gray-700">{{ employee.data[0].employee_name }}</p>
        </div>

        <div class="grid grid-cols-1 gap-4">
            <div class="grid grid-cols-2 gap-3">
                <div class="bg-gray-200 p-4">
                    Welcome {{ session.user }}!

                    <h4>{{ loggesInUser.data }}</h4>
                </div>
                <div class="bg-gray-200 p-4">
                    <Button @click="session.logout.submit()" appearance="danger">Logout</Button>
                </div>
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <div class="flex items-center justify-center">
                        <Avatar imageURL="https://placekitten.com/200" label="Felix" size="lg" />
                        <Avatar imageURL="" label="Felix" size="lg" />
                    </div>
                    <div class="text-center mt-4">
                        <h2 class="text-xl font-bold">{{ employee.data[0].employee_name }}</h2>
                        <p class="text-gray-600">{{ employee.data[0].designation  }}</p>
                    </div>
                    <div class="mt-6">
                        <ul class="flex justify-center space-x-4">
                            <li>
                                <a href="#" class="text-blue-500 hover:text-blue-700">Twitter</a>
                            </li>
                            <li>
                                <a href="#" class="text-blue-500 hover:text-blue-700">LinkedIn</a>
                            </li>
                            <li>
                                <a href="#" class="text-blue-500 hover:text-blue-700">GitHub</a>
                            </li>
                        </ul>
                    </div>
                </div>

            </div>
        </div>
        <div class="grid grid-cols-2 gap-4" v-for="d in employee.data" :key="d">
            <div class="p-4">
                <Card title="Attendance" subtitle="Employee Checkin">
                    <div class="grid grid-cols-2">
                        <div class="col-span-1 space-y-2">
                            <ul v-if="getCheckins.data.checkin_count !== 0">
                                <li v-for="(checkinLog, idx) in getCheckins.data.checkin" :key="checkinLog">
                                    <span>
                                        <Button appearance="primary">{{ idx + 1 }} </Button>&nbsp;
                                        <Button appearance="success">{{ checkinLog.name }}</Button>
                                        <br>
                                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<Badge color="yellow">{{ checkinLog.time }}</Badge>
                                    </span>
                                </li>
                            </ul>
                        </div>
                        <div class="col-span-1">
                            <ul v-if="getCheckins.data.checkout_count !== 0">
                                <li v-for="(checkoutLog, idx) in getCheckins.data.checkout" :key="checkoutLog">
                                    <span>
                                        <Button appearance="primary">{{ idx + 1 }} </Button>&nbsp;
                                        <Button appearance="danger">{{ checkoutLog.name }}</Button>
                                        <br>
                                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<Badge color="yellow">{{ checkoutLog.time }}</Badge>
                                    </span>
                                </li>
                            </ul>
                        </div>
                    </div>

                    <br>
                    <!-- checkin checkout buttons -->
                    <div class="grid grid-cols-3 gap-4">
                        <Button v-if="getCheckins.data.checkin_count <= getCheckins.data.checkout_count"
                            @click="addCheckINDialogShown = true" appearance="success">Check IN</Button>
                        <Button v-if="getCheckins.data.checkin_count >= getCheckins.data.checkout_count"
                            @click="addCheckOUTDialogShown = true" appearance="danger">Check OUT</Button>
                    </div>
                    <Dialog :options="{
                        title: 'Add New Check IN',
                        actions: [
                            {
                                label: 'Add Action',
                                appearance: 'primary',
                                handler: ({ close }) => {
                                    createCehckIn()
                                    close() // closes dialog
                                },
                            },
                            { label: 'Cancel' },
                        ],
                    }" v-model="addCheckINDialogShown">
                        <template #body-content>
                            <div class="space-y-2">
                                <Input label="Work From" type="select" :options="['Work From Home', 'In Field', 'Office']" />
                            </div>
                        </template>
                    </Dialog>
                    <Dialog :options="{
                        title: 'Add New Check Out',
                        actions: [
                            {
                                label: 'Add Action',
                                appearance: 'primary',
                                handler: ({ close }) => {
                                    createCehckOUT()
                                    close() // closes dialog
                                },
                            },
                            { label: 'Cancel' },
                        ],
                    }" v-model="addCheckOUTDialogShown">
                        <template #body-content>
                            <div class="space-y-2">
                                <Input label="Work From" type="select" :options="['Work From Home', 'In Field', 'Office']" />
                            </div>
                        </template>
                    </Dialog>
                </Card>
            </div>
            <div class="bg-gray-200 p-4">Item 2</div>
            <div class="bg-gray-200 p-4">Item 3</div>
            <div class="bg-gray-200 p-4">Item 4</div>
            <div class="bg-gray-200 p-4">Item 5</div>
            <div class="bg-gray-200 p-4">Item 6</div>
        </div>

    </div>
</template>

<script setup>
import { Button, Dialog, createListResource, Card, Input, createResource } from 'frappe-ui'
import { session } from '../data/session'
// reactive variable to store user import
import { reactive, ref } from 'vue';
import { Badge } from 'frappe-ui'

//Get logged in user
let loggesInUser = createResource({
    url: '/api/method/frappe.auth.get_logged_user'
})
loggesInUser.fetch()

//Get Employee from logged in User
const employee = createListResource({
    doctype: 'Employee',
    fields: ["*"],
    cache: 'employee',
})

employee.reload()

//checkin dialog
const addCheckINDialogShown = ref(false); //refence
const addCheckOUTDialogShown = ref(false); //refence

const checkinData = reactive({
    log_type: 'IN',
})
const checkOutData = reactive({
    log_type: 'OUT ',
})

//function to create checkin
const checkin_doc = createListResource({
    doctype: 'Employee Checkin',
    fields: ['name'],
    limit: 100,
})
checkin_doc.reload()

const createCehckIn = () => {
    console.log(employee.data[0].name)
    checkin_doc.insert.submit(checkinData)
    getCheckins.fetch()
    console.log("checkin fetched")
}

const createCehckOUT = () => {
    console.log(employee.data[0].name)
    checkin_doc.insert.submit(checkOutData)
    getCheckins.fetch()
    console.log(getCheckins.data)
}

//funtion to fetch checkin list for the day
let getCheckins = createResource({
    url: '/api/method/ess.employee_self_service_portal.page.ess.ess.get_checkin',

})
getCheckins.fetch()


</script>
