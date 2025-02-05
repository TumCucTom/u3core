<template>
    <q-page class="q-pa-md">
      <div>
        <h1 class="text-h4">Alerts</h1>
        <p class="text-subtitle2 q-mb-md">Track and manage your alerts</p>
  
       
        <q-table
          title="Alerts Table"
          :columns="columns"
          :rows="alertsData"
          row-key="id"
          selection="multiple"

        >

          <template v-slot:body-cell-siteName="{ _row }">
            <q-td>{{ _row.siteName }}</q-td>
          </template>
  
          
          <template v-slot:body-cell-siteLocation="{ _row }">
            <q-td>{{ _row.siteLocation }}</q-td>
          </template>


          
          <template v-slot:body-cell-cameraID="{ _row }">
            <q-td>{{ _row.cameraID }}</q-td>
          </template>
  
         
          <template v-slot:body-cell-faultType="{ _row }">
            <q-td>
              
              <q-chip :label="_row.faultType" color="primary" text-color="white" />
            </q-td>
          </template>
  
          
          <template v-slot:body-cell-timestamp="{ _row }">
            <q-td>{{ _row.timestamp }}</q-td>
          </template>
  
          
          <template v-slot:body-cell-resourceLink>
            <q-td>
            </q-td>
          </template>
        </q-table>
      </div>
    </q-page>
  </template>
  
  <script>
  export default {
    name: 'alertsData',
    data() {
      return {

        columns: [
          { name: 'siteName', label: 'Site Name', field: 'siteName', sortable: true },
          { name: 'siteLocation', label: 'Site Location', field: 'siteLocation', sortable: true },
          { name: 'cameraID', label: 'Camera ID', field: 'cameraID', sortable: true },
          { name: 'faultType', label: 'Fault Type', field: 'faultType', sortable: true },
          { name: 'timestamp', label: 'Timestamp', field: 'timestamp', sortable: true },
          { name: 'resourceLink', label: 'Resource Link', field: 'resourceLink' }
        ],
        alertsData: [], 
        pagination: {
          page: 1,
          rowsPerPage: 8,
        }
      };
    },
    //this is for when the server detects an alert and pushes 
    methods: {
      addAlert(alertData) {
        this.alertsData.push(alertsData);
      }
    }
  };
  </script>
  
  <style scoped>
  </style>
  