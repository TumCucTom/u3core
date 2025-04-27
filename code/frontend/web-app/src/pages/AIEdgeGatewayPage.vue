<template>
    <q-page class="q-px-lg q-py-md">
      <div>
        <div class="row justify-between items-center q-mb-lg">
          <div>
            <h1 class="text-h4 text-weight-bold">AI Edge</h1>
            <p class="text-subtitle2">Track and manage your devices.</p>
          </div>
          <q-btn
            label="+ Add New Device"
            color="dark"
            text-color="white"
            unelevated
            class="q-px-md q-py-sm"
            @click="showAddDevice = true"
          />
        </div>

        <div class="row items-center justify-between q-mb-md">
          <div class="row items-center">
            <q-chip removable class="bg-grey-2 text-black q-mr-sm">All</q-chip>
            <q-chip removable icon="filter_list" class="bg-grey-2 text-black">
              Smoke Detection
            </q-chip>
          </div>
          <q-input
            outlined
            rounded
            dense
            v-model="search"
            placeholder="Search"
            style="width: 300px;"
          >
            <template v-slot:prepend>
              <q-icon name="search" />
            </template>
          </q-input>
        </div>

        <q-table
          flat
          bordered
          :rows="filteredRows"
          :columns="columns"
          row-key="id"
          selection="multiple"
          hide-pagination
        >
          <template v-slot:body-cell-status="props">
            <q-td :props="props">
              <q-badge :label="props.value" :color="statusColor(props.value)" align="top" transparent />
            </q-td>
          </template>
          <template v-slot:body-cell-action="props">
            <q-td :props="props">
              <q-btn flat dense label="Manage" color="negative" @click="manageDevice(props.row)" />
            </q-td>
          </template>
        </q-table>

        <div class="row justify-between items-center q-mt-md">
          <q-btn flat label="Previous" />
          <q-btn flat label="Next" />
          <div class="text-caption text-grey-7">Page 1 of 10</div>
        </div>
      </div>

      <q-dialog v-model="showAddDevice" persistent>
        <q-card style="width: 600px; max-width: 95vw;">
          <q-card-section class="row justify-between items-start">
            <div class="row items-center">
              <q-avatar size="42px" class="bg-grey-2 text-dark q-mr-md">
                <q-icon name="desktop_windows" />
              </q-avatar>
              <div>
                <div class="text-h6 text-weight-bold">Add New Device</div>
                <div class="text-caption">
                  Create a new device for edge ai device management.
                </div>
              </div>
            </div>
            <q-btn dense flat round icon="close" v-close-popup />
          </q-card-section>

          <q-separator />

          <q-card-section class="q-gutter-md">
            <q-input
              outlined
              dense
              rounded
              v-model="newDevice.name"
              label="Device name"
              placeholder="Edge-03"
            />
            <q-select
              outlined
              dense
              rounded
              v-model="newDevice.type"
              :options="deviceTypes"
              label="Device name"
              placeholder="Jetson Nano"
              emit-value
              map-options
              dropdown-icon=" "
            >
              <template v-slot:append>
                <q-icon name="expand_more" />
              </template>
            </q-select>
            <q-input
              outlined
              dense
              rounded
              v-model="newDevice.spec"
              label="Device Specifications"
              placeholder="4GB RAM, 64GB Storage"
            />
            <q-select
              outlined
              dense
              rounded
              v-model="newDevice.status"
              :options="statusOptions"
              label="Deployment Status"
              placeholder="Online"
              emit-value
              map-options
              dropdown-icon=" "
            >
              <template v-slot:append>
                <q-icon name="expand_more" />
              </template>
            </q-select>
          </q-card-section>

          <q-card-actions class="row justify-between q-px-md q-pb-md">
            <q-btn flat label="Cancel" v-close-popup class="q-px-lg" />
            <q-btn
              label="Save"
              color="dark"
              text-color="white"
              class="q-px-xl"
              @click="saveDevice"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </q-page>
  </template>

  <script>
  export default {
    data() {
      return {
        search: "",
        showAddDevice: false,
        columns: [
          { name: "deviceName", label: "Device Name", field: "deviceName", align: "left", sortable: true },
          { name: "deviceType", label: "Device Type", field: "deviceType", align: "left" },
          { name: "spec", label: "Specification", field: "spec", align: "left" },
          { name: "status", label: "Status", field: "status", align: "left" },
          { name: "action", label: "Action", field: "action", align: "left" }
        ],
        rows: [
          { id: 1, deviceName: "Edge-01", deviceType: "Jetson Nano", spec: "4GB RAM, 64GB Storage", status: "Online" },
          { id: 2, deviceName: "Edge-01", deviceType: "Jetson Nano", spec: "4GB RAM, 64GB Storage", status: "Offline" },
          { id: 3, deviceName: "Model version 102", deviceType: "SI10112", spec: "SI10112", status: "Online" }
        ],
        deviceTypes: ["Jetson Nano", "Raspberry Pi 4", "SI10112"],
        statusOptions: ["Online", "Offline", "Maintenance"],
        newDevice: {
          name: "",
          type: "",
          spec: "",
          status: ""
        }
      };
    },
    computed: {
      filteredRows() {
        if (!this.search) return this.rows;
        const term = this.search.toLowerCase();
        return this.rows.filter(r =>
          Object.values(r).some(val => String(val).toLowerCase().includes(term))
        );
      }
    },
    methods: {
      statusColor(s) {
        return s === "Online" ? "green-4" : s === "Offline" ? "red-4" : "orange-4";
      },
      manageDevice(row) {},
      saveDevice() {
        this.showAddDevice = false;
      }
    }
  };
  </script>

  <style>
  .q-page {
    background: #ffffff;
  }
  </style>
