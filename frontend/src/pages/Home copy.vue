<template>
  <div>
    <!-- Navbar Starts -->
    <NavbarComponent />
    <!-- Navbar Ends -->

    <!-- Body Starts -->

    <div class="">
      <!-- employee info starts -->

      <div class="py-4 w-full">
        <!-- <Card title="Employee Info" subtitle=""> -->
        <div class="grid grid-col-3 lg:grid-cols-3 gap-1 mb-6">
          <div
            class="w-full max-w-sm bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
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
                employee_doc.data[""]
              }}</span>
              <div class="flex mt-4 space-x-3 md:mt-6">
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
              </div>
            </div>
          </div>
          <!-- <div class="col-span-1 w-3/12">
                            <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="A" />
                        </div> -->
          <div
            class="grid grid-cols-3 lg:grid-cols-2 col-span-2 gap-1 mb-6 justify-start"
          >
            <div v-for="(value, key) in employee_doc.data" :key="key">
              <div class="flow-root" v-if="value !== ''">
                <p class="text-sm float-left text-green-600 m-2">
                  {{ key }}
                </p>
                <p class="text-sm float-left text-green-800 m-2">
                  {{ value || "Not Available" }}
                </p>
              </div>
            </div>
          </div>
        </div>
        <!-- </Card> -->
      </div>
      <!-- employee info ends -->
      <!-- section 2 starts -->

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- attendance Card starts -->
        <div class="flex flex-col justify-between">
          <Card title="Attendance" subtitle="Mark Your Checkin">
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
              <Button
                appearance="warning"
                @click="employee_checkins.insert.submit(checkinWFH)"
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
                @click="employee_checkins.insert.submit(checkinOffice)"
                :loading="employee_checkins.loading"
                >Office</Button
              >
              <Button
                appearance="danger"
                @click="employee_checkins.insert.submit(checkOutWFH)"
                :loading="employee_checkins.loading"
                >WFH OUT</Button
              >
              <Button
                appearance="danger"
                @click="employee_checkins.insert.submit(checkOutField)"
                :loading="employee_checkins.loading"
                >Field OUT</Button
              >
              <Button
                appearance="danger"
                @click="employee_checkins.insert.submit(checkOutOffice)"
                :loading="employee_checkins.loading"
                >Office OUT</Button
              >
            </div>

            <div
              class="relative overflow-x-auto h-60 overflow-y-visible shadow-md sm:rounded-lg"
            >
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
          </Card>
        </div>
        <!-- attendance Card ends -->
        <!-- In Office Members Card starts -->
        <div class="flex flex-col justify-between">
          <Card title="In Office Members" subtitle="Today">
            <div
              class="relative overflow-x-auto h-60 overflow-y-visible shadow-md sm:rounded-lg"
            >
              <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                <thead
                  class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
                >
                  <tr>
                    <th scope="col" class="px-6 py-3">Employee Name</th>
                    <th scope="col" class="px-6 py-3">Work From</th>
                  </tr>
                </thead>
                <tbody class="h-10 overflow-y-visible">
                  <tr
                    class="bg-white border-b dark:bg-gray-900 dark:border-gray-700"
                    v-for="present_employee in present_employees.data"
                    :key="present_employee.name"
                  >
                    <th
                      scope="row"
                      class="px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                    >
                      {{ present_employee.employee_name }}
                    </th>
                    <td class="px-6">
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
            <div
              class="relative overflow-x-auto h-80 overflow-y-visible shadow-md sm:rounded-lg"
            >
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
          </Card>
        </div>
        <!-- attendance Card ends -->
        <!-- In Office Members Card starts -->
        <div class="flex flex-col justify-between">
          <Card title="Holiday's" subtitle="This Month">
            <div
              class="relative overflow-x-auto h-80 overflow-y-visible shadow-md sm:rounded-lg"
            >
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
          </Card>
        </div>
        <!-- In Office Members Card ends -->
        <!-- In Office Members Card starts -->
        <div class="flex flex-col justify-between">
          <Card title="Week Off's" subtitle="This Month">
            <div
              class="relative overflow-x-auto h-80 overflow-y-visible shadow-md sm:rounded-lg"
            >
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
          </Card>
        </div>
        <!-- In Office Members Card ends -->
      </div>
      <!-- section 3 ends -->
    </div>
  </div>
</template>

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
import {
  initAccordions,
  initCarousels,
  initCollapses,
  initDials,
  initDismisses,
  initDrawers,
  initDropdowns,
  initModals,
  initPopovers,
  initTabs,
  initTooltips,
} from "flowbite";
import { TheCard } from "flowbite-vue";

// options with default values

// initialize components based on data attribute selectors
onMounted(() => {
  initFlowbite();
});

const checkinOffice = reactive({
  log_type: "IN",
  work_from: "Office",
  longitude: null,
  latitude: null,
});
const checkinWFH = reactive({
  log_type: "IN",
  work_from: "Work From Home",
  longitude: null,
  latitude: null,
});
const checkinField = reactive({
  log_type: "IN",
  work_from: "On Field",
  longitude: null,
  latitude: null,
});
const checkOutOffice = reactive({
  log_type: "OUT",
  work_from: "Office",
  longitude: null,
  latitude: null,
});
const checkOutWFH = reactive({
  log_type: "OUT",
  work_from: "Work From Home",
  longitude: null,
  latitude: null,
});
const checkOutField = reactive({
  log_type: "OUT",
  work_from: "On Field",
  longitude: null,
  latitude: null,
});
const checkOutData = reactive({
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
  employee_checkins.insert.submit(checkinField);
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
