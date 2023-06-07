<template>
    <div>
        <div class="flex justify-self">
            <h2 class="flex flex-row items-center justify-between font-bold text-lg text-gray-600 mb-4">
                Welcome {{ session.user }}!
            </h2>
            <h4>{{ loggesInUser.data }}</h4>
        </div>
        <Button @click="session.logout.submit()" appearance="danger">Logout</Button>
        <div class="grid grid-rows-4 grid-flow-col gap-4">
            <div>01</div>
            <div>09</div>
        </div>
        <ul>
            <li v-for="d in employee.data" :key="d">
                <Card :title="d.employee">
                    <div class="grid grid-cols-3" >
                        <div class="col-span-1 space-y-2">
                            <ul v-if="getCheckins.data.checkin_count !== 0">
                                <li v-for="(checkinLog, idx) in getCheckins.data.checkin" :key="checkinLog">
                                    <span>
                                        {{ idx+1 }} -
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
                                        {{ idx + 1 }} -
                                        <Button appearance="danger">{{ checkoutLog.name }}</Button>
                                        <br>
                                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<Badge color="yellow" >{{ checkoutLog.time }}</Badge>
                                    </span>
                                </li>
                            </ul>
                        </div>
                    </div>

                    <br>
                    <!-- checkin checkout buttons -->
                    {{ checkinData }}
                    {{ checkOutData }}
                    <div class="grid grid-cols-3 gap-4">
                        <Button v-if="getCheckins.data.checkin_count <= getCheckins.data.checkout_count" @click="addCheckINDialogShown = true" appearance="success">Check IN</Button>
                        <Button v-if="getCheckins.data.checkin_count >= getCheckins.data.checkout_count" @click="addCheckOUTDialogShown = true" appearance="danger">Check OUT</Button>
                    </div>
                    <Dialog :options="{
                                title: 'Add New Check In',
                                actions: [
                                    {
                                        label: 'Add Action',
                                        appearance: 'primary',
                                        handler: ({ close }) => {
                                            createCehckIn()
                                            getCheckins.fetch()
                                            close() // closes dialog
                                        },
                                    },
                                    { label: 'Cancel' },
                                ],
                            }" v-model="addCheckINDialogShown">
                            <template #body-content>
                                <div class="space-y-2">
                                Hello
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
                                            getCheckins.fetch()
                                            close() // closes dialog
                                        },
                                    },
                                    { label: 'Cancel' },
                                ],
                            }" v-model="addCheckOUTDialogShown">
                            <template #body-content>
                                <div class="space-y-2">
                                Hello
                                </div>
                            </template>
                    </Dialog>
                </Card>
                <Card :title="CheckedIN"></Card>
            </li>
        </ul>



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
    checkin_doc.reload()
    console.log(employee.data[0].name)
    checkin_doc.insert.submit(checkinData)
}

const createCehckOUT = () => {
    checkin_doc.reload()
    console.log(employee.data[0].name)
    checkin_doc.insert.submit(checkOutData)
}

//funtion to fetch checkin list for the day
let getCheckins = createResource({
    url: '/api/method/ess.employee_self_service_portal.page.ess.ess.get_checkin',
    cache: 'getCheckins',
})
getCheckins.fetch()

</script>
