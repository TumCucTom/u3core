<template>
  <q-page class="q-pa-md">
    <div>
      <h1 class="text-h4">Alerts</h1>
      <p class="text-subtitle2 q-mb-md">Track and manage your alerts</p>

      <!-- Button to Add a Test Log -->
      <q-btn
        label="Add Test Log"
        color="primary"
        class="q-mb-md"
        @click="addTestLog"
      />

      <!-- Table to Display Alerts -->
      <q-table
        title="Alerts Table"
        :columns="columns"
        :rows="alertsData"
        row-key="id"
        selection="multiple"
      >
        <!-- cameraName -->
        <template v-slot:body-cell-cameraName="{ row }">
          <q-td>{{ row.cameraName }}</q-td>
        </template>

        <!-- cameraAddress -->
        <template v-slot:body-cell-cameraAddress="{ row }">
          <q-td>{{ row.cameraAddress }}</q-td>
        </template>

        <!-- timestamp -->
        <template v-slot:body-cell-timestamp="{ row }">
          <q-td>{{ row.timestamp }}</q-td>
        </template>

        <!-- faultType -->
        <template v-slot:body-cell-faultType="{ row }">
          <q-td>
            <q-chip :label="row.faultType" color="primary" text-color="white" />
          </q-td>
        </template>

        <!-- numberOfHazards -->
        <template v-slot:body-cell-numberOfHazards="{ row }">
          <q-td>{{ row.numberOfHazards }}</q-td>
        </template>

        <!-- falsePositives -->
        <template v-slot:body-cell-falsePositives="{ row }">
          <q-td>{{ row.falsePositives }}</q-td>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'AlertsPage',
  data() {
    return {
      columns: [
        { name: 'cameraName', label: 'Camera Name', field: 'cameraName', sortable: true },
        { name: 'cameraAddress', label: 'Camera Address', field: 'cameraAddress', sortable: true },
        { name: 'timestamp', label: 'Timestamp', field: 'timestamp', sortable: true },
        { name: 'faultType', label: 'Fault Type', field: 'faultType', sortable: true },
        { name: 'numberOfHazards', label: 'Hazard count', field: 'numberOfHazards' },
        { name: 'falsePositives', label: 'False positive?', field: 'falsePositives' }
      ],
      alertsData: [],
      pollInterval: null
    };
  },
  mounted() {
    // Fetch logs once when component mounts
    this.fetchAlerts();

    // Set up polling every 5 seconds
    this.pollInterval = setInterval(() => {
      this.fetchAlerts();
    }, 5000);
  },
  beforeDestroy() {
    // Clear the interval to prevent memory leaks
    clearInterval(this.pollInterval);
  },
  methods: {
    // Fetch existing logs from the server
    async fetchAlerts() {
      try {
        const response = await fetch("http://127.0.0.1:3002/api/get-logs");
        const data = await response.json();
        this.alertsData = data;
      } catch (error) {
        console.error("Error fetching alerts:", error);
      }
    },

    // Add a test log with random hazard type and current timestamp
    async addTestLog() {
      try {
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');

        // Format: "YYYY-MM-DD HH:MM:SS"
        const timestamp = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;

        // Choose a random hazard type
        const hazardTypes = ["fire", "smoke", "intruder"];
        const randomHazard = hazardTypes[Math.floor(Math.random() * hazardTypes.length)];

        // Build the JSON payload
        const payload = {
          timestamp: timestamp,
          type: randomHazard,
          cameraAddress: "rtsp://dummy.camera/stream_test"
        };

        // POST to your server
        const response = await fetch("http://127.0.0.1:3002/api/add-hazard", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(payload)
        });

        if (!response.ok) {
          console.error("Failed to add test log");
          return;
        }

        const result = await response.json();
        console.log("Test log added:", result);

        // Refresh the table to see the new log
        this.fetchAlerts();
      } catch (error) {
        console.error("Error adding test log:", error);
      }
    }
  }
};
</script>

<style scoped>
</style>
