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

          <template v-slot:body-cell-cameraName="{ _row }">
            <q-td>{{ _row.cameraName }}</q-td>
          </template>
  
          
          <template v-slot:body-cell-cameraAddress="{ _row }">
            <q-td>{{ _row.cameraAddress }}</q-td>
          </template>


          
          <template v-slot:body-cell-timestamp="{ _row }">
            <q-td>{{ _row.timestamp }}</q-td>
          </template>
  
         
          <template v-slot:body-cell-faultType="{ _row }">
            <q-td>
              
              <q-chip :label="_row.faultType" color="primary" text-color="white" />
            </q-td>
          </template>
  
          
          <template v-slot:body-cell-numberOfHazards="{ _row }">
            <q-td>{{ _row.numberOfHazards }}</q-td>
          </template>

          <template v-slot:body-cell-falsePositives="{ _row }">
            <q-td>{{ _row.falsePositives }}</q-td>
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
          { name: 'cameraName', label: 'Site Name', field: 'cameraName', sortable: true },
          { name: 'cameraAddress', label: 'Site Location', field: 'cameraAddress', sortable: true },
          { name: 'timestamp', label: 'Timestamp', field: 'timestamp', sortable: true },
          { name: 'faultType', label: 'Fault Type', field: 'faultType', sortable: true },
          { name: 'numberOfHazards', label: 'Hazard count', field: 'numberOfHazards' },
          { name: 'falsePositives', label: 'False positive?', field: 'falsePositives' },
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
  