<template>
    <q-page class="q-px-lg q-py-md">
      <div>
        <div class="row justify-between items-center q-mb-lg">
          <div>
            <h1 class="text-h4 text-weight-bold">Manage Sites</h1>
            <p class="text-subtitle2">
              Track, manage and forecast your customers and orders.
            </p>
          </div>
          <q-btn
            label="+ Add Site"
            color="dark"
            text-color="white"
            unelevated
            class="q-px-md q-py-sm"
            @click="showAddSite = true"
          />
        </div>

        <div class="row q-col-gutter-md q-mb-xl">
          <div class="col-12 col-sm-4">
            <q-card flat bordered class="q-pa-lg">
              <div class="text-caption text-grey-7">Total Sites</div>
              <div class="text-h4 text-weight-bold">{{ metrics.totalSites.toLocaleString() }}</div>
            </q-card>
          </div>
          <div class="col-12 col-sm-4">
            <q-card flat bordered class="q-pa-lg">
              <div class="text-caption text-grey-7">Operational Cameras</div>
              <div class="text-h4 text-weight-bold">{{ metrics.operationalCams.toLocaleString() }}</div>
            </q-card>
          </div>
          <div class="col-12 col-sm-4">
            <q-card flat bordered class="q-pa-lg">
              <div class="text-caption text-grey-7">All Alerts</div>
              <div class="text-h4 text-weight-bold">{{ metrics.allAlerts.toLocaleString() }}</div>
            </q-card>
          </div>
        </div>

        <div class="q-mb-md">
          <div class="row justify-between items-center q-mb-sm">
            <div class="text-subtitle1 text-weight-medium">Recent alerts</div>
            <div class="row items-center">
              <q-btn outline dense icon="event" label="Select dates" class="q-mr-sm" />
              <q-btn outline dense icon="filter_list" label="Apply filter" />
            </div>
          </div>

          <q-table
            flat
            bordered
            :rows="rows"
            :columns="columns"
            row-key="id"
            selection="multiple"
            hide-pagination
          />
        </div>

        <div class="row justify-between items-center q-mt-md">
          <q-btn flat label="Previous" />
          <q-btn flat label="Next" />
          <div class="text-caption text-grey-7">Page 1 of 10</div>
        </div>
      </div>

      <q-dialog v-model="showAddSite" persistent>
        <q-card style="width: 500px; max-width: 90vw;">
          <q-card-section class="row justify-between items-start">
            <div class="row items-center">
              <q-avatar icon="apartment" color="grey-2" text-color="dark" class="q-mr-md" />
              <div>
                <div class="text-h6 text-weight-bold">Add site</div>
                <div class="text-caption">
                  Create a new site with all the required information.
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
              v-model="siteName"
              label="Site name*"
              placeholder="What is your title?"
            />

            <div class="row q-col-gutter-md">
              <div class="col">
                <q-input
                  outlined
                  dense
                  rounded
                  v-model="longitude"
                  label="Longitude"
                  placeholder="What is your Longitude?"
                />
              </div>
              <div class="col">
                <q-input
                  outlined
                  dense
                  rounded
                  v-model="latitude"
                  label="Latitude"
                  placeholder="What is your Latitude?"
                />
              </div>
            </div>

            <q-input
              outlined
              dense
              rounded
              v-model="locationZone"
              label="Location Zone"
              placeholder="Zone A"
            />

            <q-input
              type="textarea"
              outlined
              dense
              v-model="description"
              label="Description*"
              placeholder="e.g. I joined Stripe’s Customer Success team to help them scale their checkout product..."
              style="min-height: 120px;"
            />
          </q-card-section>

          <q-card-actions class="row justify-between q-px-md q-pb-md">
            <q-btn flat label="Cancel" v-close-popup class="q-px-lg" />
            <q-btn
              label="Save"
              color="dark"
              text-color="white"
              class="q-px-xl"
              @click="saveSite"
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
        showAddSite: false,
        metrics: {
          totalSites: 2420,
          operationalCams: 1210,
          allAlerts: 316
        },
        columns: [
          { name: "name", label: "Site name", field: "name", align: "left", sortable: true },
          { name: "location", label: "Site Location", field: "location", align: "left" },
          { name: "camera", label: "Associated Camera", field: "camera", align: "left" },
          { name: "gateway", label: "Gateway", field: "gateway", align: "left" }
        ],
        rows: [
          {
            id: 1,
            name: "Road and Highway Construction",
            location: "Building Perimeter and Fence Lines",
            camera: "CAM-001A",
            gateway: "CAM-001A"
          },
          {
            id: 2,
            name: "Los Angeles Distribution Center",
            location: "Common Rooms and Lounges",
            camera: "CAM-002B",
            gateway: "CAM-001A"
          },
          {
            id: 3,
            name: "Road and Highway Construction",
            location: "Loading Docks and Delivery Areas",
            camera: "CAM-003C",
            gateway: "CAM-001A"
          },
          {
            id: 4,
            name: "Los Angeles Distribution Center",
            location: "Elevator Entrances",
            camera: "CAM-004D",
            gateway: "CAM-001A"
          },
          {
            id: 5,
            name: "Road and Highway Construction",
            location: "Building Entrances and Exits",
            camera: "CAM-005E",
            gateway: "CAM-001A"
          },
          {
            id: 6,
            name: "Los Angeles Distribution Center",
            location: "Reception Area",
            camera: "CAM-006F",
            gateway: "CAM-001A"
          },
          {
            id: 7,
            name: "Site 01",
            location: "Parking Lots and Garages",
            camera: "CAM-007G",
            gateway: "CAM-001A"
          }
        ],
        siteName: "",
        longitude: "",
        latitude: "",
        locationZone: "",
        description: ""
      };
    },
    methods: {
      saveSite() {
        this.showAddSite = false;
      }
    }
  };
  </script>

  <style>
  .q-page {
    background: #ffffff;
  }
  </style>
