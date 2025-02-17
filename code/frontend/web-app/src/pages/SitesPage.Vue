<template>
  <q-page class="q-px-lg q-py-md">
    <div>
      
      <div class="row justify-between items-center q-mb-lg">
        <div>
          <h1 class="text-h4 text-bold">Manage Sites</h1>
          <p class="text-subtitle2">
            Track, manage and forecast your customers and orders.
          </p>
        </div>
        <q-btn label="+ Add Site" color="primary" text-color="white" />
      </div>

      
      <div class="row q-mb-lg">
        <q-card flat bordered class="col-12 col-md-4 q-pa-md">
          <div class="text-caption text-grey-7">Total Sites</div>
          <div class="text-h5 text-bold">0</div>
        </q-card>
        <q-card flat bordered class="col-12 col-md-4 q-pa-md">
          <div class="text-caption text-grey-7">Operational Cameras</div>
          <div class="text-h5 text-bold">0</div>
        </q-card>
        <q-card flat bordered class="col-12 col-md-4 q-pa-md">
          <div class="text-caption text-grey-7">All Alerts</div>
          <div class="text-h5 text-bold">0</div>
        </q-card>
      </div>

      
      <div class="row q-mb-md justify-between items-center">
        <h2 class="text-h6">Recent alerts</h2>
        <div class="row">
          <q-btn label="Select dates" outline class="q-mx-sm" />
          <q-btn label="Apply filter" color="primary" text-color="white" />
        </div>
      </div>

      
      <q-table
        flat
        rows-per-page-options="[5, 10, 15]"
        :rows="tableEntries"
        :columns="columns"
        row-key="id"
      >
        
        <template v-slot:body-cell-site="props">
          <q-checkbox />
          <span>{{ props.row.site }}</span>
        </template>

        
        <template v-slot:body-cell-resource-link>
          <q-btn flat label="Video" color="primary" />
          <q-btn flat label="Image" color="primary" />
        </template>
      </q-table>

      
      <div class="row justify-between items-center q-mt-md">
        <q-btn flat label="Previous" />
        <q-btn flat label="Next" />
        <div class="text-caption text-grey-7">Page 1 of 10</div>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  data() {
    return {
      // mock table data until we can link to server
      tableEntries: [
        { id: 1, site: "Site 01", location: "Location 01", camera: "CAM-001", fault: "Oil Leak", timestamp: "2024-11-05 08:30 AM" },
        { id: 2, site: "Site 02", location: "Location 02", camera: "CAM-002", fault: "Water Leak", timestamp: "2024-11-05 12:45 PM" },
        { id: 3, site: "Site 03", location: "Location 03", camera: "CAM-003", fault: "Fire", timestamp: "2024-11-05 03:15 PM" },
        { id: 4, site: "Site 04", location: "Location 04", camera: "CAM-004", fault: "Smoke", timestamp: "2024-11-06 09:00 AM" },
      ],
      columns: [
        { name: "site", align: "left", label: "Site name", field: "site" },
        { name: "location", align: "left", label: "Site Location", field: "location" },
        { name: "camera", align: "left", label: "Camera ID", field: "camera" },
        { name: "fault", align: "left", label: "Fault Type", field: "fault" },
        { name: "timestamp", align: "left", label: "Timestamp", field: "timestamp" },
        { name: "resource-link", align: "left", label: "Resource Link", field: "resourceLink" },
      ],
    };
  },
};
</script>

<style>
.q-page {
  background: #f9f9f9; 
}
</style>
