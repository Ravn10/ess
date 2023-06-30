<template>
    <div>
        <!-- Navbar Starts -->
        <nav class="fixed top-0 z-50 w-full bg-white border-b border-gray-200 dark:bg-gray-800 dark:border-gray-700">
        <div class="px-3 py-3 lg:px-5 lg:pl-3">
            <div class="flex items-center justify-between">
            <div class="flex items-center justify-start">
                <button data-drawer-target="logo-sidebar" data-drawer-toggle="logo-sidebar" aria-controls="logo-sidebar" type="button" class="inline-flex items-center p-2 text-sm text-gray-500 rounded-lg sm:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600">
                    <span class="sr-only">Open sidebar</span>
                    <svg class="w-6 h-6" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path clip-rule="evenodd" fill-rule="evenodd" d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"></path>
                    </svg>
                </button>
                <a href="https://flowbite.com" class="flex ml-2 md:mr-24">
                <img src="https://flowbite.com/docs/images/logo.svg" class="h-8 mr-3" alt="FlowBite Logo" />
                <span class="self-center text-xl font-semibold sm:text-2xl whitespace-nowrap dark:text-white">{{ company }}</span>
                </a>
            </div>
            <div class="flex items-center">
                <div class="flex items-center ml-3">
                    <div>
                    <button type="button" class="flex text-sm bg-gray-800 rounded-full focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600" aria-expanded="false" data-dropdown-toggle="dropdown-user">
                        <span class="sr-only">Open user menu</span>
                        <img class="w-8 h-8 rounded-full" src="https://flowbite.com/docs/images/people/profile-picture-5.jpg" alt="user photo">
                    </button>
                    </div>
                    <div class="z-50 hidden my-4 text-base list-none bg-white divide-y divide-gray-100 rounded shadow dark:bg-gray-700 dark:divide-gray-600" id="dropdown-user">
                    <div class="px-4 py-3" role="none">
                        <p class="text-sm text-gray-900 dark:text-white" role="none">
                        Neil Sims
                        </p>
                        <p class="text-sm font-medium text-gray-900 truncate dark:text-gray-300" role="none">
                        neil.sims@flowbite.com
                        </p>
                    </div>
                    <ul class="py-1" role="none">
                        <li>
                        <a href="/CheckinHome.vue" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-600 dark:hover:text-white" role="menuitem">Dashboard</a>
                        </li>
                        <li>
                        <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-600 dark:hover:text-white" role="menuitem">Settings</a>
                        </li>
                        <li>
                        <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-600 dark:hover:text-white" role="menuitem">Earnings</a>
                        </li>
                        <li>
                        <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-600 dark:hover:text-white" role="menuitem">Sign out</a>
                        </li>
                    </ul>
                    </div>
                </div>
                </div>
            </div>
        </div>
        </nav>
        <!-- Navbar Ends -->
        <!-- Sidebar Starts -->
        <aside id="logo-sidebar" class="fixed top-0 left-0 z-40 w-64 h-screen pt-20 transition-transform -translate-x-full bg-white border-r border-gray-200 sm:translate-x-0 dark:bg-gray-800 dark:border-gray-700" aria-label="Sidebar">
        <div class="h-full px-3 pb-4 overflow-y-auto bg-white dark:bg-gray-800">
            <ul class="space-y-2 font-medium">
                <li>
                    <a href="#" class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                    <svg aria-hidden="true" class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"></path><path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"></path></svg>
                    <span class="ml-3">Dashboard</span>
                    </a>
                </li>
                <li>
                    <a href="#" class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                    <svg aria-hidden="true" class="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
                    <span class="flex-1 ml-3 whitespace-nowrap">Kanban</span>
                    <span class="inline-flex items-center justify-center px-2 ml-3 text-sm font-medium text-gray-800 bg-gray-200 rounded-full dark:bg-gray-700 dark:text-gray-300">Pro</span>
                    </a>
                </li>
                <li>
                    <a href="#" class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                    <svg aria-hidden="true" class="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M8.707 7.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l2-2a1 1 0 00-1.414-1.414L11 7.586V3a1 1 0 10-2 0v4.586l-.293-.293z"></path><path d="M3 5a2 2 0 012-2h1a1 1 0 010 2H5v7h2l1 2h4l1-2h2V5h-1a1 1 0 110-2h1a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V5z"></path></svg>
                    <span class="flex-1 ml-3 whitespace-nowrap">Inbox</span>
                    <span class="inline-flex items-center justify-center w-3 h-3 p-3 ml-3 text-sm font-medium text-blue-800 bg-blue-100 rounded-full dark:bg-blue-900 dark:text-blue-300">3</span>
                    </a>
                </li>
                <li>
                    <a href="#" class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                    <svg aria-hidden="true" class="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path></svg>
                    <span class="flex-1 ml-3 whitespace-nowrap">Users</span>
                    </a>
                </li>
                <li>
                    <a href="#" class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                    <svg aria-hidden="true" class="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 2a4 4 0 00-4 4v1H5a1 1 0 00-.994.89l-1 9A1 1 0 004 18h12a1 1 0 00.994-1.11l-1-9A1 1 0 0015 7h-1V6a4 4 0 00-4-4zm2 5V6a2 2 0 10-4 0v1h4zm-6 3a1 1 0 112 0 1 1 0 01-2 0zm7-1a1 1 0 100 2 1 1 0 000-2z" clip-rule="evenodd"></path></svg>
                    <span class="flex-1 ml-3 whitespace-nowrap">Products</span>
                    </a>
                </li>
                <li>
                    <a href="#" class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                    <svg aria-hidden="true" class="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd"></path></svg>
                    <span class="flex-1 ml-3 whitespace-nowrap">Sign In</span>
                    </a>
                </li>
                <li>
                    <a href="#" class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                    <svg aria-hidden="true" class="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clip-rule="evenodd"></path></svg>
                    <span class="flex-1 ml-3 whitespace-nowrap">Sign Up</span>
                    </a>
                </li>
            </ul>
        </div>
        </aside>
        <!-- Sidebar Ends -->
        <!-- Body Starts -->


        <div class="p-4 sm:ml-64 m-9">
            <!-- employee info starts -->
            <div class="py-4">
                <Card title="Employee Info" subtitle="">
                    <div class="grid grid-col-3 lg:grid-cols-3 gap-1 mb-6">
                        <div class="col-span-1 w-3/12">
                            <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="A">
                        </div>
                    <div class="grid grid-cols-3 lg:grid-cols-2 col-span-2 gap-1 mb-6 justify-start">
                        <div v-for="(value, key) in employee_doc.data" :key="key">
                            <div class="flow-root " v-if="value !== null">
                                <p class="text-sm  float-left text-green-600 m-2">
                                    {{ key }}
                                </p>
                                <p class="text-sm  float-left text-green-800 m-2">
                                    {{ value }}
                                </p>
                            </div>
                        </div>


                    </div>
                    </div>
                </Card>

            </div>
            <!-- employee info ends -->
            <!-- section 2 starts -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <!-- attendance Card starts -->
                <div class="flex flex-col justify-between">
                    <Card title="Attendance" subtitle="Mark Your Checkin">
                    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                        <Button appearance="warning" @click="employee_checkins.insert.submit(checkinWFH)" :loading="employee_checkins.loading">WFH</Button>
                        <Button appearance="primary" @click="getLocation" :loading="employee_checkins.loading">In Field</Button>
                        <Button appearance="success" @click="employee_checkins.insert.submit(checkinOffice)" :loading="employee_checkins.loading">Office</Button>
                        <Button appearance="danger" @click="employee_checkins.insert.submit(checkOutWFH)" :loading="employee_checkins.loading">WFH OUT</Button>
                        <Button appearance="danger" @click="employee_checkins.insert.submit(checkOutField)" :loading="employee_checkins.loading">Field OUT</Button>
                        <Button appearance="danger" @click="employee_checkins.insert.submit(checkOutOffice)" :loading="employee_checkins.loading">Office OUT</Button>
                    </div>

                        <div class="relative overflow-x-auto h-60 overflow-y-visible  shadow-md sm:rounded-lg ">
                            <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                                <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                                    <tr>
                                        <th scope="col" class="px-6 py-3">
                                            Checkin From
                                        </th>
                                        <th scope="col" class="px-6 py-3">
                                            Type
                                        </th>
                                        <th scope="col" class="px-6 py-3">
                                            Time
                                        </th>
                                    </tr>
                                </thead>
                                <tbody class="h-10 overflow-y-visible">
                                    <tr class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 "  v-for="employee_checkin in employee_checkins.data" :key="employee_checkin.name">
                                        <th scope="row" class="px-6  font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                            {{ employee_checkin.work_from }}
                                        </th>
                                        <td class="px-6 ">
                                            {{ employee_checkin.log_type }}
                                        </td>
                                        <td class="px-6 ">
                                            {{ employee_checkin.time }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </Card>
                </div>
                <!-- attendance Card ends -->
                <!-- In Office Members Card starts -->
                <div class="flex flex-col justify-between">
                    <Card title="In Office Members" subtitle="Today">
                        <div class="relative overflow-x-auto h-60 overflow-y-visible  shadow-md sm:rounded-lg ">
                            <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                                <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                                    <tr>
                                        <th scope="col" class="px-6 py-3">
                                            Employee Name
                                        </th>
                                        <th scope="col" class="px-6 py-3">
                                            Work From
                                        </th>

                                    </tr>
                                </thead>
                                <tbody class="h-10 overflow-y-visible">
                                    <tr class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 "  v-for="present_employee in present_employees.data" :key="present_employee.name">
                                        <th scope="row" class="px-6  font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                            {{ present_employee.employee_name }}
                                        </th>
                                        <td class="px-6 ">
                                            {{ present_employee.work_from }}
                                        </td>

                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </Card>
                </div>
                <!-- In Office Members Card ends -->
            </div>
             <!-- section 2 ends -->
             <!-- section 3 starts -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <!-- attendance Card starts -->
                <div class="flex flex-col justify-between">
                    <Card title="Birthday" subtitle="This Month">
                        <div class="relative overflow-x-auto h-80 overflow-y-visible  shadow-md sm:rounded-lg ">
                            <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                                <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                                    <tr>
                                        <th scope="col" class="px-6 py-3">
                                            Employee
                                        </th>
                                        <th scope="col" class="px-6 py-3">
                                            Birth Day
                                        </th>
                                    </tr>
                                </thead>
                                <tbody class="h-10 overflow-y-visible">

                                    <tr class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 "  v-for="birthday in birthdays.data" :key="birthday.name">
                                        <th scope="row" class="px-6  font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                            {{ birthday.employee_name }}
                                        </th>
                                        <td class="px-6 ">
                                            {{ birthday.day }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </Card>
                </div>
                <!-- attendance Card ends -->
                <!-- In Office Members Card starts -->
                <div class="flex flex-col justify-between">
                    <Card title="Holiday's" subtitle="This Month">
                        <div class="relative overflow-x-auto h-80 overflow-y-visible  shadow-md sm:rounded-lg ">
                            <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                                <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                                    <tr>
                                        <th scope="col" class="px-6 py-3">
                                            Date
                                        </th>
                                        <th scope="col" class="px-6 py-3">
                                            Holiday
                                        </th>

                                    </tr>
                                </thead>
                                <tbody class="h-10 overflow-y-visible">
                                    <div v-if="holiday_for_month.data">
                                        <tr class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 "  v-for="holiday in holiday_for_month.data" :key="holiday.day">
                                            <th scope="row" class="px-6  font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                                {{ holiday.day }}
                                            </th>
                                            <td class="px-6 ">
                                                {{ holiday.description }}
                                            </td>

                                        </tr>
                                    </div>
                                    <tr v-else>   No Holiday's This Month  </tr>
                                </tbody>
                            </table>
                        </div>
                    </Card>
                </div>
                <!-- In Office Members Card ends -->
                <!-- In Office Members Card starts -->
                <div class="flex flex-col justify-between">
                    <Card title="Week Off's" subtitle="This Month">
                        <div class="relative overflow-x-auto h-80 overflow-y-visible  shadow-md sm:rounded-lg ">
                            <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                                <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                                    <tr>
                                        <th scope="col" class="px-6 py-3">
                                            Date
                                        </th>
                                        <th scope="col" class="px-6 py-3">
                                            Description
                                        </th>

                                    </tr>
                                </thead>
                                <tbody class="h-10 overflow-y-visible">
                                    <tr class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 "  v-for="week_off in week_off_for_month.data" :key="week_off.day">
                                        <th scope="row" class="px-6  font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                            {{ week_off.day }}
                                        </th>
                                        <td class="px-6 ">
                                            {{ week_off.description }}
                                        </td>

                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </Card>
                </div>
                <!-- In Office Members Card ends -->
            </div>
            <!-- section 3 ends -->
        </div>
    </div>
</template>

<script setup>
import {ref, computed , reactive } from "vue";
import { Avatar, createListResource, createResource, Input ,Button, Card, FeatherIcon, createDocumentResource} from 'frappe-ui';
import { session } from "../data/session";
import { employeeResource } from "../data/employee";

const checkinOffice = reactive({
    log_type: 'IN',
    work_from:"Office",
    longitude:null,
    latitude:null
})
const checkinWFH = reactive({
    log_type: 'IN',
    work_from:"Work From Home",
    longitude:null,
    latitude:null
})
const checkinField = reactive({
    log_type: 'IN',
    work_from:"On Field",
    longitude:null,
    latitude:null
})
const checkOutOffice = reactive({
    log_type: 'OUT',
    work_from:"Office",
    longitude:null,
    latitude:null
})
const checkOutWFH = reactive({
    log_type: 'OUT',
    work_from:"Work From Home",
    longitude:null,
    latitude:null
})
const checkOutField = reactive({
    log_type: 'OUT',
    work_from:"On Field",
    longitude:null,
    latitude:null
})
const checkOutData = reactive({
    log_type: 'OUT ',
})

//Get logged in user
let loggesInUser = createResource({
    url: '/api/method/frappe.auth.get_logged_user'
})
loggesInUser.fetch()

//Get employee from user
let employee_doc = createResource({
    url: '/api/method/ess.api.employee.get_employee_from_user'

})
employee_doc.fetch()

//Get employee birthdays from user
let birthdays = createResource({
    url: '/api/method/ess.employee_self_service_portal.page.ess.ess.get_employee_with_birthday_this_month'
})
birthdays.fetch()

//Get employee holiday_for_month from user
let holiday_for_month = createResource({
    url: '/api/method/ess.employee_self_service_portal.page.ess.ess.holiday_for_month'
})
holiday_for_month.fetch()

//Get employee week off from user
let week_off_for_month = createResource({
    url: '/api/method/ess.employee_self_service_portal.page.ess.ess.week_off_for_month',
    // params:{
    //     'employee':employee.name
    // }
})
week_off_for_month.fetch()

//Get present employee from
let present_employees = createResource({
    url: '/api/method/ess.api.employee.get_presenty'
})
present_employees.fetch()

//Get Employee from logged in User
const employee = createListResource({
    doctype: 'Employee',
    fields: ["*"],
    cache: 'employee',
})

employee.reload()


//Get Employee Checkin from logged in User
const employee_checkins = createListResource({
    doctype: 'Employee Checkin',
    filters:[["time","between",(new Date(),new Date())]],
    fields: ["*"],
    cache: 'employee_checkins',
})

employee_checkins.reload()

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      handleSuccess,
      handleError
    );
  } else {
    locationError = "Geolocation is not supported by this browser.";
  }
};
function handleSuccess(position) {
  const latitude = position.coords.latitude;
  const longitude = position.coords.longitude;
  checkinField.latitude = position.coords.latitude;
  checkinField.longitude = position.coords.longitude;
  employee_checkins.insert.submit(checkinField)
};
function handleError(error) {
  switch (error.code) {
    case error.PERMISSION_DENIED:
      this.locationError = "User denied the request for geolocation.";
      break;
    case error.POSITION_UNAVAILABLE:
      this.locationError = "Location information is unavailable.";
      break;
    case error.TIMEOUT:
      this.locationError = "The request to get location timed out.";
      break;
    case error.UNKNOWN_ERROR:
      this.locationError = "An unknown error occurred.";
      break;
  }
};


</script>
