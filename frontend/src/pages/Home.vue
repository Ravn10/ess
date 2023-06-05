<template>
    <div>
        <div class="flex justify-self">
            <h2 class="flex flex-row items-center justify-between font-bold text-lg text-gray-600 mb-4">
                Welcome {{ session.user }}!
            </h2>
            <h4>{{ loggesInUser.data }}</h4>
        </div>
        <Button @click="session.logout.submit()" appearance="danger">Logout</Button>
        <ul>
            <li v-for="d in employee.data" :key="d">
                <Card :title="d.employee">
                    {{ d.time }}
                    <br>
                    {{ employee.data[0].name }}
                    {{ getCheckins.data.checkin_count }}
                    <div class="row" v-if="getCheckins.data.checkin_count==0 && getCheckins.data.checkout_count==0">
                        <div class="col-6">
                            <ul v-if="getCheckins.data.checkin_count !== 0">
                                <li v-for="checkinLog in getCheckins.data.checkin" :key="checkinLog">
                                    <span>
                                        <Badge color="green">{{ checkinLog.name }}</Badge>
                                        <br>
                                        <Badge color="yellow">{{ checkinLog.time }}</Badge>
                                    </span>
                                </li>
                            </ul>
                        </div>
                        <div class="col-6">
                            <ul v-if="getCheckins.data.checkout_count !== 0">
                                <li v-for="checkoutLog in getCheckins.data.checkout" :key="checkoutLog">
                                    <span>
                                        <Badge color="red">{{ checkoutLog.name }}</Badge>
                                        <br>
                                        <Badge color="yellow">{{ checkoutLog.time }}</Badge>
                                    </span>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="row" v-else>
                        Not Checked In Yet
                    </div>
                    <br>
                    <div class="flex flex-row space-y-2 items-center justify-between">
                        <Button v-if="getCheckins.data.checkin_count < getCheckins.data.checkout_count" @click="addActionDialogShown = true" appearance="danger">Check OUT</Button>
                        <Button v-if="getCheckins.data.checkin_count >= getCheckins.data.checkout_count" @click="addActionDialogShown = true" appearance="success">Check IN</Button>
                        <Button @click="addActionDialogShown = true" icon-left="plus">New Action</Button>
                    {{ addActionDialogShown }}
                    </div>
                    <Dialog :options="{
                                title: 'Add New Action',
                                actions: [
                                    {
                                        label: 'Add Action',
                                        appearance: 'primary',
                                        handler: ({ close }) => {
                                            close() // closes dialog
                                        },
                                    },
                                    { label: 'Cancel' },
                                ],
                            }" v-model="addActionDialogShown">
                            <template #body-content>
                                <div class="space-y-2">
                                Hello
                                </div>
                            </template>
                    </Dialog>
                </Card>
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
const addActionDialogShown = ref(false); //refence

const checkinData = reactive({
    log_type: 'IN',
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
}

//funtion to fetch checkin list for the day
let getCheckins = createResource({
    url: '/api/method/ess.employee_self_service_portal.page.ess.ess.get_checkin',
    cache: 'getCheckins',
})
getCheckins.fetch()


</script>
