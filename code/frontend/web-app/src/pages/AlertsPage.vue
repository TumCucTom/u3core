<template>
  <q-page class="q-pa-md">
    <div>
      <h1 class="text-h4">Alerts</h1>
      <p class="text-subtitle2 q-mb-md">Track and manage your alerts</p>

      <q-table
        title="Alerts Table"
        :columns="columns"
        :rows="displayRows"
        row-key="id"
        selection="multiple"
      >
        <template v-slot:body-cell-cameraName="{ row }">
          <q-td>{{ row.cameraName }}</q-td>
        </template>

        <template v-slot:body-cell-cameraAddress="{ row }">
          <q-td>{{ row.cameraAddress }}</q-td>
        </template>

        <template v-slot:body-cell-timestamp="{ row }">
          <q-td>{{ row.timestamp }}</q-td>
        </template>

        <!-- colourful fault type chip -->
        <template v-slot:body-cell-faultType="{ row }">
          <q-td>
            <q-chip
              outline
              dense
              :color="chipColor(row.faultType)"
              class="q-pl-none q-pr-sm"
            >
              <template v-slot:prepend>
                <q-icon
                  name="lens"
                  size="8px"
                  :color="chipColor(row.faultType)"
                  class="q-mr-xs"
                />
              </template>
              {{ row.faultType }}
            </q-chip>
          </q-td>
        </template>

        <template v-slot:body-cell-numberOfHazards="{ row }">
          <q-td>{{ row.numberOfHazards }}</q-td>
        </template>

        <template v-slot:body-cell-falsePositives="{ row }">
          <q-td>{{ row.falsePositives }}</q-td>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script>
export default {
  name: "AlertsPage",
  data() {
    return {
      columns: [
        { name: "cameraName", label: "Camera Name", field: "cameraName", sortable: true },
        { name: "cameraAddress", label: "Camera Address", field: "cameraAddress", sortable: true },
        { name: "timestamp", label: "Timestamp", field: "timestamp", sortable: true },
        { name: "faultType", label: "Fault Type", field: "faultType", sortable: true },
        { name: "numberOfHazards", label: "Hazard count", field: "numberOfHazards" },
        { name: "falsePositives", label: "False positive?", field: "falsePositives" }
      ],
      alertsData: [],
      demoAlerts: [
        {
          id: 1,
          cameraName: "CAM-001A",
          cameraAddress: "10.0.0.21",
          timestamp: "2025-04-10 08:15 AM",
          faultType: "Oil leak",
          numberOfHazards: 3,
          falsePositives: 0
        },
        {
          id: 2,
          cameraName: "CAM-002B",
          cameraAddress: "10.0.0.45",
          timestamp: "2025-04-10 09:42 AM",
          faultType: "Water leak",
          numberOfHazards: 1,
          falsePositives: 1
        },
        {
          id: 3,
          cameraName: "CAM-003C",
          cameraAddress: "10.0.0.63",
          timestamp: "2025-04-09 07:55 PM",
          faultType: "Fire",
          numberOfHazards: 2,
          falsePositives: 0
        },
        {
          id: 4,
          cameraName: "CAM-004D",
          cameraAddress: "10.0.0.77",
          timestamp: "2025-04-09 05:30 PM",
          faultType: "Smoke",
          numberOfHazards: 4,
          falsePositives: 0
        }
      ],
      pollInterval: null
    };
  },
  computed: {
    displayRows() {
      return this.alertsData.length ? this.alertsData : this.demoAlerts;
    }
  },
  mounted() {
    this.fetchAlerts();
    this.pollInterval = setInterval(() => {
      this.fetchAlerts();
    }, 5000);
  },
  beforeUnmount() {
    clearInterval(this.pollInterval);
  },
  methods: {
    async fetchAlerts() {
      try {
        const response = await fetch("http://16.171.224.57:80/api/get-logs");
        const data = await response.json();
        this.alertsData = data;
      } catch (error) {
        console.error("Error fetching alerts:", error);
      }
    },
    chipColor(type) {
      switch (type) {
        case "Oil leak":
          return "amber-6";
        case "Water leak":
          return "light-blue-6";
        case "Fire":
          return "red-5";
        case "Smoke":
          return "purple-6";
        default:
          return "grey-6";
      }
    }
  }
};
</script>

<style scoped>
</style>
