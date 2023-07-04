<script setup>
import { ref, computed, reactive } from "vue";

import {
  Avatar,
  createListResource,
  createResource,
  Input,
  Button,
  Card,
  FeatherIcon,
  createDocumentResource,
} from "frappe-ui";
import { session } from "../data/session";
import { employeeResource } from "../data/employee";
import { Drawer } from "flowbite";
import { onMounted } from "vue";
import { initFlowbite } from "flowbite";

import NavbarComponent from "../components/Navbar.vue";
import SidebarComponent from "../components/Sidebar.vue";

// options with default values

// initialize components based on data attribute selectors
onMounted(() => {
  initFlowbite();
});

const center = { lat: 45.508, lng: -73.587 };
const location = reactive({
  html: null,
  loaded: false,
});
const checkinOffice = reactive({
  location_html: null,
  log_type: "IN",
  work_from: "Office",
  longitude: null,
  latitude: null,
});
const checkinWFH = reactive({
  location_html: null,
  log_type: "IN",
  work_from: "Work From Home",
  longitude: null,
  latitude: null,
});
const checkinField = reactive({
  location_html: null,
  log_type: "IN",
  work_from: "On Field",
  longitude: null,
  latitude: null,
});
const checkOutOffice = reactive({
  location_html: null,
  log_type: "OUT",
  work_from: "Office",
  longitude: null,
  latitude: null,
});
const checkOutWFH = reactive({
  location_html: null,
  log_type: "OUT",
  work_from: "Work From Home",
  longitude: null,
  latitude: null,
});
const checkOutField = reactive({
  location_html: null,
  log_type: "OUT",
  work_from: "On Field",
  longitude: null,
  latitude: null,
});
const checkOutData = reactive({
  location_html: null,
  log_type: "OUT ",
});

//Get logged in user
let loggesInUser = createResource({
  url: "/api/method/frappe.auth.get_logged_user",
});
loggesInUser.fetch();

//Get employee from user
let employee_doc = createResource({
  url: "/api/method/ess.api.employee.get_employee_from_user",
});
employee_doc.fetch();

let employee_in_office = createResource({
  url: "/api/method/ess.api.employee.members_in_office_status",
});
employee_in_office.fetch();

//Get employee birthdays from user
let birthdays = createResource({
  url:
    "/api/method/ess.employee_self_service_portal.page.ess.ess.get_employee_with_birthday_this_month",
});
birthdays.fetch();

//Get employee holiday_for_month from user
let holiday_for_month = createResource({
  url: "/api/method/ess.employee_self_service_portal.page.ess.ess.holiday_for_month",
});
holiday_for_month.fetch();

//Get employee week off from user
let week_off_for_month = createResource({
  url: "/api/method/ess.employee_self_service_portal.page.ess.ess.week_off_for_month",
  // params:{
  //     'employee':employee.name
  // }
});
week_off_for_month.fetch();

//Get present employee from
let present_employees = createResource({
  url: "/api/method/ess.api.employee.get_presenty",
});
present_employees.fetch();

//Get present employee from
let eom_report = createResource({
  url: "/api/method/ess.api.employee.eom_report_data",
});
eom_report.fetch();

//Get present employee from
let leave_report = createResource({
  url: "/api/method/ess.api.employee.leave_report_data",
});
leave_report.fetch();

//Get leave details
let leave_details = createResource({
  url: "/api/method/ess.api.employee.leave_details",
});
leave_details.fetch();

//Get total_working_hours_data
let total_working_hours = createResource({
  url: "/api/method/ess.api.employee.total_working_hours_data",
});
total_working_hours.fetch();

//Get Employee from logged in User
const employee = createListResource({
  doctype: "Employee",
  fields: ["*"],
  cache: "employee",
});

employee.reload();

//Get Employee Checkin from logged in User
const employee_checkins = createListResource({
  doctype: "Employee Checkin",
  filters: [["time", "between", (new Date(), new Date())]],
  fields: ["*"],
  cache: "employee_checkins",
});

employee_checkins.reload();

function checkin(work_from) {
  employee_checkins.insert.submit({
    log_type: "IN",
    work_from: work_from,
  });
  employee_in_office.fetch();
}
function checkOut(work_from) {
  employee_checkins.insert.submit({
    location_html: null,
    log_type: "OUT",
    work_from: work_from,
    longitude: null,
    latitude: null,
  });
  employee_in_office.fetch();
}

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(handleSuccess, handleError);
  } else {
    locationError = "Geolocation is not supported by this browser.";
  }
}
function handleSuccess(position) {
  const latitude = position.coords.latitude;
  const longitude = position.coords.longitude;
  checkinField.latitude = position.coords.latitude;
  checkinField.longitude = position.coords.longitude;

  location.loaded = true;
  location.html =
    `<iframe src="https://www.google.com/maps/embed?pb=!1m17!1m12!1m3!1d3769.669609454357!2d` +
    position.coords.longitude +
    `!3d` +
    position.coords.latitude +
    `4!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m2!1m1!2zMTnCsDA3JzE5LjciTiA3M8KwMDAnMzkuMyJF!5e0!3m2!1sen!2sin!4v1688387438794!5m2!1sen!2sin"
            width="100%"
            height="100%"
            style="border: 1"
            allowfullscreen=""
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"
          ></iframe>`;
  checkin("On Field");
}
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
}
</script>
<template>
  <div class="antialiased bg-gray-50 dark:bg-gray-900">
    <NavbarComponent :company='employee_doc.data["Company"]' />

    <!-- Sidebar -->
    <SidebarComponent />

    <main class="p-4 md:ml-64 h-auto pt-20">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
        <!-- profile picture card starts -->
        <div
          class="border-2 border-solid border-gray-300 rounded-lg dark:border-gray-600 h-32 md:h-64"
        >
          <div class="flex flex-col items-center pt-10 pb-10">
            <img
              class="w-24 h-24 mb-3 rounded-full shadow-lg"
              src="https://bootdey.com/img/Content/avatar/avatar7.png"
              alt="Bonnie image"
            />
            <h5 class="mb-1 text-xl font-medium text-gray-900 dark:text-white">
              {{ employee_doc.data["Employee Name"] }}
            </h5>
            <span class="text-sm text-gray-500 dark:text-gray-400">{{
              employee_doc.data["Name"]
            }}</span>
            <span class="text-sm text-gray-500 dark:text-gray-400">{{
              employee_doc.data["Designation"]
            }}</span>
            <!-- <div class="flex mt-4 space-x-3 md:mt-6">
              <a
                href="#"
                class="inline-flex items-center px-4 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                >Add friend</a
              >
              <a
                href="#"
                class="inline-flex items-center px-4 py-2 text-sm font-medium text-center text-gray-900 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 focus:ring-4 focus:outline-none focus:ring-gray-200 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-700 dark:focus:ring-gray-700"
                >Message</a
              >
            </div> -->
          </div>
        </div>
        <!-- profile picture card ends -->
        <!-- Personal info card starts -->
        <div
          class="border-2 border-solid rounded-lg border-gray-300 dark:border-gray-600 h-32 md:h-64"
        >
          <div class="flex items-center justify-center mb-2">
            <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white pt-4">
              Personal Info
            </h5>
          </div>
          <div class="flow-root">
            <ul role="list" class="divide-y divide-gray-200 dark:divide-gray-700">
              <li class="py-3 sm:py-4 pl-5">
                <div class="flex items-center space-x-4">
                  <div class="flex-shrink-0">
                    <FeatherIcon name="at-sign" class="h-6 w-6" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium truncate text-gray-900 dark:text-white">
                      {{ employee_doc.data["Personal Email"] || "Not Available" }}
                    </p>
                    <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                      Personal Email
                    </p>
                  </div>
                </div>
              </li>
              <li class="py-3 sm:py-4 pl-5">
                <div class="flex items-center space-x-4">
                  <div class="flex-shrink-0">
                    <FeatherIcon name="phone" class="h-6 w-6" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium truncate text-gray-900 dark:text-white">
                      {{ employee_doc.data["Cell Number"] || "Not Available" }}
                    </p>
                    <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                      Personal Phone
                    </p>
                  </div>
                </div>
              </li>
              <li class="py-3 sm:py-4 pl-5">
                <div class="flex items-center space-x-4">
                  <div class="flex-shrink-0">
                    <FeatherIcon name="home" class="h-6 w-6" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium truncate text-gray-900 dark:text-white">
                      {{ employee_doc.data["Permanent Address"] || "Not Available" }}
                    </p>
                    <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                      Address
                    </p>
                  </div>
                </div>
              </li>
            </ul>
          </div>
          <!-- </div> -->
        </div>
        <!-- Personal info card ends -->
        <!-- Organisational info card starts -->
        <div
          class="border-2 border-solid rounded-lg border-gray-300 dark:border-gray-600 h-32 md:h-64"
        >
          <div class="flex items-center justify-center mb-2">
            <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white pt-4">
              Organisational Info
            </h5>
          </div>
          <div class="flow-root">
            <ul role="list" class="divide-y divide-gray-200 dark:divide-gray-700">
              <li class="py-3 sm:py-4 pl-5">
                <div class="flex items-center space-x-4">
                  <div class="flex-shrink-0">
                    <FeatherIcon name="at-sign" class="h-6 w-6" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium truncate text-gray-900 dark:text-white">
                      {{ employee_doc.data["Company Email"] || "Not Available" }}
                    </p>
                    <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                      Org Email
                    </p>
                  </div>
                </div>
              </li>
              <li class="py-3 sm:py-4 pl-5">
                <div class="flex items-center space-x-4">
                  <div class="flex-shrink-0">
                    <FeatherIcon name="phone" class="h-6 w-6" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium truncate text-gray-900 dark:text-white">
                      {{ employee_doc.data["Cell Number"] || "Not Available" }}
                    </p>
                    <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                      Org Phone
                    </p>
                  </div>
                </div>
              </li>
              <li class="py-3 sm:py-4 pl-5">
                <div class="flex items-center space-x-4">
                  <div class="flex-shrink-0">
                    <FeatherIcon name="navigation" class="h-6 w-6" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium truncate text-gray-900 dark:text-white">
                      {{ employee_doc.data["Branch"] || "Not Available" }}
                    </p>
                    <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                      Branch
                    </p>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
        <!-- Organisational info card ends -->
        <!-- Reporting info card starts -->
        <div
          class="border-2 border-solid rounded-lg border-gray-300 dark:border-gray-600 h-32 md:h-64"
        >
          <div class="flex items-center justify-center mb-2">
            <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white pt-4">
              Reporting Info
            </h5>
          </div>
          <div class="flow-root">
            <ul role="list" class="divide-y divide-gray-200 dark:divide-gray-700">
              <li class="py-3 sm:py-4 pl-5">
                <div class="flex items-center space-x-4">
                  <div class="flex-shrink-0">
                    <FeatherIcon name="calendar" class="h-6 w-6" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium truncate text-gray-900 dark:text-white">
                      {{ employee_doc.data["Shift Request Approver"] || "Not Available" }}
                    </p>
                    <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                      Shift Request Approver
                    </p>
                  </div>
                </div>
              </li>
              <li class="py-3 sm:py-4 pl-5">
                <div class="flex items-center space-x-4">
                  <div class="flex-shrink-0">
                    <FeatherIcon name="phone" class="h-6 w-6" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium truncate text-gray-900 dark:text-white">
                      {{ employee_doc.data["credit-card"] || "Not Available" }}
                    </p>
                    <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                      Expense Approver
                    </p>
                  </div>
                </div>
              </li>
              <li class="py-3 sm:py-4 pl-5">
                <div class="flex items-center space-x-4">
                  <div class="flex-shrink-0">
                    <FeatherIcon name="check" class="h-6 w-6" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium truncate text-gray-900 dark:text-white">
                      {{ employee_doc.data["Leave Approver"] || "Not Available" }}
                    </p>
                    <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                      Leave Approver
                    </p>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
        <!-- Reporting info card ends -->
      </div>
      <!-- Checkin Starts -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <div
          class="border-2 border-solid rounded-lg border-gray-300 dark:border-gray-600 h-48 md:h-72"
        >
          <div class="grid grid-cols-3 gap-4 mb-4 p-3">
            <Button
              appearance="warning"
              @click="checkin('Work From Home')"
              :loading="employee_checkins.loading"
              >WFH</Button
            >
            <Button
              appearance="primary"
              @click="getLocation"
              :loading="employee_checkins.loading"
              >In Field</Button
            >
            <Button
              appearance="success"
              @click="checkin('Office')"
              :loading="employee_checkins.loading"
              >Office</Button
            >
            <Button
              appearance="danger"
              @click="checkOut('Work From Home')"
              :loading="employee_checkins.loading"
              >WFH OUT</Button
            >
            <Button
              appearance="danger"
              @click="checkOut('On Field')"
              :loading="employee_checkins.loading"
              >Field OUT</Button
            >
            <Button
              appearance="danger"
              @click="checkOut('Office')"
              :loading="employee_checkins.loading"
              >Office OUT</Button
            >
          </div>
          <div class="relative overflow-x-auto h-32 overflow-y-visible">
            <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
              <thead
                class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
              >
                <tr>
                  <th scope="col" class="px-6 py-3">Checkin From</th>
                  <th scope="col" class="px-6 py-3">Type</th>
                  <th scope="col" class="px-6 py-3">Time</th>
                </tr>
              </thead>
              <tbody class="h-10 overflow-y-visible">
                <tr
                  class="bg-white border-b dark:bg-gray-900 dark:border-gray-700"
                  v-for="employee_checkin in employee_checkins.data"
                  :key="employee_checkin.name"
                >
                  <th
                    scope="row"
                    class="px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                  >
                    {{ employee_checkin.work_from }}
                  </th>
                  <td class="px-6">
                    {{ employee_checkin.log_type }}
                  </td>
                  <td class="px-6">
                    {{ employee_checkin.time }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div
          class="border-2 border-solid rounded-lg border-gray-300 dark:border-gray-600 h-48 md:h-72"
        >
          <div class="flex items-center justify-center mb-2">
            <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white pt-4">
              Current Location
            </h5>
          </div>
          <div class="border-2 border-solid">
            <div v-if="location.loaded" v-html="location.html"></div>
            <div v-else>
              <iframe
                src="https://www.google.com/maps/embed?pb=!1m17!1m12!1m3!1d3769.669609454357!2d73.00872521490183!3d19.12214478706144!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m2!1m1!2zMTnCsDA3JzE5LjciTiA3M8KwMDAnMzkuMyJF!5e0!3m2!1sen!2sin!4v1688387438794!5m2!1sen!2sin"
                width="100%"
                height="100%"
                style="border: 1"
                allowfullscreen=""
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
              ></iframe>
            </div>
          </div>
        </div>
        <!-- Members in office start -->
        <div
          class="border-2 border-solid rounded-lg border-gray-300 dark:border-gray-600 h-48 md:h-72"
        >
          <div class="flex items-center justify-center mb-2">
            <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white pt-4">
              Members In Office
            </h5>
          </div>
          <div class="relative overflow-x-auto h-60 overflow-y-visible">
            <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
              <thead
                class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
              >
                <tr>
                  <th scope="col" class="px-6 py-3">Employee</th>
                </tr>
              </thead>
              <tbody class="h-10 overflow-y-visible">
                <tr
                  class="bg-white border-b dark:bg-gray-900 dark:border-gray-700"
                  v-for="emp_in_office in employee_in_office.data.emp_in_office"
                  :key="emp_in_office"
                >
                  <td class="px-6">
                    {{ emp_in_office.employee_name }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <!-- Members in office end -->
        <div
          class="border-2 border-solid rounded-lg border-gray-300 dark:border-gray-600 h-48 md:h-72"
        >
          <div class="flex items-center justify-center mb-2">
            <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white pt-4">
              Members Out Of Office
            </h5>
          </div>
          <div class="relative overflow-x-auto h-60 overflow-y-visible">
            <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
              <thead
                class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
              >
                <tr>
                  <th scope="col" class="px-6 py-3">Employee</th>
                </tr>
              </thead>
              <tbody class="h-10 overflow-y-visible">
                <tr
                  class="bg-white border-b dark:bg-gray-900 dark:border-gray-700"
                  v-for="emp_out_of_office in employee_in_office.data.emp_out_of_office"
                  :key="emp_out_of_office"
                >
                  <td class="px-6">
                    {{ emp_out_of_office.employee_name }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div
          class="border-2 border-solid rounded-lg border-gray-300 dark:border-gray-600 h-48 md:h-72"
        >
          <div class="flex items-center justify-center mb-2">
            <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white pt-4">
              Members Absent
            </h5>
          </div>
          <div class="relative overflow-x-auto h-60 overflow-y-visible">
            <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
              <thead
                class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
              >
                <tr>
                  <th scope="col" class="px-6 py-3">Employee</th>
                </tr>
              </thead>
              <tbody class="h-10 overflow-y-visible">
                <tr
                  class="bg-white border-b dark:bg-gray-900 dark:border-gray-700"
                  v-for="emp_absent in employee_in_office.data.emp_absent"
                  :key="emp_absent"
                >
                  <td class="px-6">
                    {{ emp_absent.employee_name }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div
          class="border-2 border-solid rounded-lg border-gray-300 dark:border-gray-600 h-48 md:h-72"
        >
          <div class="flex items-center justify-center mb-2">
            <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white pt-4">
              Birthday's Of The Month
            </h5>
          </div>
          <div class="relative overflow-x-auto h-60 overflow-y-visible">
            <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
              <thead
                class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
              >
                <tr>
                  <th scope="col" class="px-6 py-3">Employee</th>
                  <th scope="col" class="px-6 py-3">Birth Day</th>
                </tr>
              </thead>
              <tbody class="h-10 overflow-y-visible">
                <tr
                  class="bg-white border-b dark:bg-gray-900 dark:border-gray-700"
                  v-for="birthday in birthdays.data"
                  :key="birthday.name"
                >
                  <th
                    scope="row"
                    class="px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                  >
                    {{ birthday.employee_name }}
                  </th>
                  <td class="px-6">
                    {{ birthday.day }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div
          class="border-2 border-solid rounded-lg border-gray-300 dark:border-gray-600 h-48 md:h-72"
        >
          <div class="flex items-center justify-center mb-2">
            <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white pt-4">
              Week Off's Of The Month
            </h5>
          </div>
          <div class="relative overflow-x-auto h-60 overflow-y-visible">
            <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
              <thead
                class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
              >
                <tr>
                  <th scope="col" class="px-6 py-3">Date</th>
                  <th scope="col" class="px-6 py-3">Description</th>
                </tr>
              </thead>
              <tbody class="h-10 overflow-y-visible">
                <tr
                  class="bg-white border-b dark:bg-gray-900 dark:border-gray-700"
                  v-for="week_off in week_off_for_month.data"
                  :key="week_off.day"
                >
                  <th
                    scope="row"
                    class="px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                  >
                    {{ week_off.day }}
                  </th>
                  <td class="px-6">
                    {{ week_off.description }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div
          class="border-2 border-solid rounded-lg border-gray-300 dark:border-gray-600 h-48 md:h-72"
        >
          <div class="flex items-center justify-center mb-2">
            <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white pt-4">
              Holiday's Of The Month
            </h5>
          </div>
          <div class="relative overflow-x-auto h-60 overflow-y-visible">
            <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
              <thead
                class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
              >
                <tr>
                  <th scope="col" class="px-6 py-3">Date</th>
                  <th scope="col" class="px-6 py-3">Holiday</th>
                </tr>
              </thead>
              <tbody class="h-10 overflow-y-visible">
                <div v-if="holiday_for_month.data">
                  <tr
                    class="bg-white border-b dark:bg-gray-900 dark:border-gray-700"
                    v-for="holiday in holiday_for_month.data"
                    :key="holiday.day"
                  >
                    <th
                      scope="row"
                      class="px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                    >
                      {{ holiday.day }}
                    </th>
                    <td class="px-6">
                      {{ holiday.description }}
                    </td>
                  </tr>
                </div>
                <tr v-else>
                  No Holiday's This Month
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <!-- Checkin Ends -->
      <!--Attendance Report -->
      <div
        class="border-2 border-solid rounded-lg border-gray-300 dark:border-gray-600 h-96 mb-4"
      >
        <div class="flex items-center justify-center mb-2">
          <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white pt-4">
            Attendance Report
          </h5>
        </div>
        <div class="relative h-60">
          <div class="relative overflow-x-auto h-72 text-xs">
            <table class="relative w-full border">
              <thead>
                <tr>
                  <th
                    v-for="column in total_working_hours.data.columns"
                    :key="column"
                    class="sticky top-0 px-6 py-3 text-black-900 bg-gray-300"
                  >
                    {{ column.label }}
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y bg-gray-100">
                <tr v-for="res in total_working_hours.data.result" :key="res">
                  <td
                    class="px-6 py-4 text-center"
                    v-for="column in total_working_hours.data.columns"
                    :key="column"
                  >
                    {{ res[column.fieldname] }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <!--Attendance Report -->
      <!-- End of Month Report Starts -->
      <div
        class="border-2 border-solid rounded-lg border-gray-300 dark:border-gray-600 h-96 mb-4"
      >
        <div class="flex items-center justify-center mb-2">
          <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white pt-4">
            End Of Month Report
          </h5>
        </div>
        <div class="relative overflow-x-auto h-72 text-xs">
          <table class="relative w-full border">
            <thead>
              <tr>
                <th
                  v-for="column in eom_report.data.columns"
                  :key="column"
                  class="sticky top-0 px-6 py-3 text-black-900 bg-gray-300"
                >
                  {{ column.label }}
                </th>
              </tr>
            </thead>
            <tbody class="divide-y bg-gray-100">
              <tr v-for="res in eom_report.data.result" :key="res">
                <td
                  class="px-6 py-4 text-center"
                  v-for="column in eom_report.data.columns"
                  :key="column"
                >
                  {{ res[column.fieldname] }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!-- leave section -->
      <div
        class="border-2 border-solid rounded-lg border-gray-300 dark:border-gray-600 h-96 mb-4"
      >
        <div class="flex items-center justify-center mb-2">
          <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white pt-4">
            Leave Details
          </h5>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <div
            v-for="(value, name, index) in leave_details.data.leave_allocation"
            class="rounded-lg border-gray-300 dark:border-gray-600 h-38 md:h-64"
          >
            <div class="flex items-center justify-center mb-2">
              <h5
                class="text-xl font-bold leading-none text-gray-900 dark:text-white pt-4"
              >
                {{ name }}
              </h5>
            </div>
            <div class="flow-root">
              <ul
                v-for="(v, n, i) in leave_details.data.leave_allocation[name]"
                role="list"
                class="divide-y divide-gray-200 dark:divide-gray-700"
              >
                <li class="py-3 sm:py-4 pl-5">
                  <div class="flex items-center space-x-4">
                    <div class="flex-shrink-0">
                      {{ n }}
                    </div>
                    <div class="flex-1 min-w-0">
                      <p
                        class="text-sm font-medium truncate text-gray-900 dark:text-white"
                      >
                        {{ v }}
                      </p>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
            <!-- </div> -->
          </div>
        </div>
      </div>
      <!-- End of Month Report Ends -->
    </main>
  </div>
</template>
