<template>
  <q-page class="dashboard q-pa-lg">
    <!-- Welcome Header -->
    <div class="header q-mb-lg">
      <h1 class="title">Welcome back, {{ name }}</h1>
      <p class="subtitle">Track, manage and forecast your asset performance</p>
    </div>

    <!-- Statistics Cards -->
    <div class="row q-mb-lg stats-row">
      <!-- Total Sites -->
      <q-card flat bordered class="stat-card col-12 col-md-4">
        <div class="stat-header row justify-between items-center q-mb-sm">
          <span class="stat-label">Total Sites</span>
          <q-menu>
            <template v-slot:anchor>
              <q-btn flat dense round icon="more_vert" size="sm" />
            </template>
            <q-list>
              <q-item clickable v-close-popup>
                <q-item-section>Details</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </div>
        <div class="stat-body row justify-between items-center">
          <span class="stat-value">{{ siteCount }}</span>
          <div class="trend-pill row items-center">
            <q-icon name="arrow_upward" size="18px" color="green-6" />
            <span>100%</span>
          </div>
        </div>
      </q-card>

      <!-- Cameras -->
      <q-card flat bordered class="stat-card col-12 col-md-4">
        <div class="stat-header row justify-between items-center q-mb-sm">
          <span class="stat-label">Cameras</span>
          <q-menu>
            <template v-slot:anchor>
              <q-btn flat dense round icon="more_vert" size="sm" />
            </template>
            <q-list>
              <q-item clickable v-close-popup>
                <q-item-section>Details</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </div>
        <div class="stat-body row justify-between items-center">
          <span class="stat-value">{{ cameraCount }}</span>
          <div class="trend-pill row items-center">
            <q-icon name="arrow_upward" size="18px" color="green-6" />
            <span>100%</span>
          </div>
        </div>
      </q-card>

      <!-- Alerts -->
      <q-card flat bordered class="stat-card col-12 col-md-4">
        <div class="stat-header row justify-between items-center q-mb-sm">
          <span class="stat-label">Alerts</span>
          <q-menu>
            <template v-slot:anchor>
              <q-btn flat dense round icon="more_vert" size="sm" />
            </template>
            <q-list>
              <q-item clickable v-close-popup>
                <q-item-section>Details</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </div>
        <div class="stat-body row justify-between items-center">
          <span class="stat-value">{{ alertCount }}</span>
          <div class="trend-pill row items-center">
            <q-icon name="arrow_upward" size="18px" color="green-6" />
            <span>100%</span>
          </div>
        </div>
      </q-card>
    </div>

    <!-- Charts & Overview -->
    <div class="row q-mb-lg content-row">
      <!-- Anomalies Chart -->
      <div class="col-12 col-md-8 charts-col">
        <q-card flat bordered class="chart-card q-mb-md">
          <div class="chart-header row justify-between items-center q-mb-sm">
            <span class="chart-title">Number of Anomalies Detected</span>
            <q-menu>
              <template v-slot:anchor>
                <q-btn flat dense round icon="more_vert" size="sm" />
              </template>
              <q-list>
                <q-item clickable v-close-popup>
                  <q-item-section>Details</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </div>
          <div style="height: 260px">
            <canvas ref="anomaliesChart"></canvas>
          </div>
          <div v-if="isLoadingAnomaliesData" class="fallback q-mt-md">
            <q-spinner size="2.5em" />
            <p>Loading anomaly data...</p>
          </div>
        </q-card>

        <!-- Types Chart -->
        <q-card flat bordered class="chart-card">
          <div class="chart-header row justify-between items-center q-mb-sm">
            <span class="chart-title">Type of Anomalies Detected</span>
            <q-menu>
              <template v-slot:anchor>
                <q-btn flat dense round icon="more_vert" size="sm" />
              </template>
              <q-list>
                <q-item clickable v-close-popup>
                  <q-item-section>Details</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </div>
          <div style="height: 260px">
            <canvas ref="typesChart"></canvas>
          </div>
          <div v-if="isLoadingTypesData" class="fallback q-mt-md">
            <q-spinner size="2.5em" />
            <p>Loading anomaly types data...</p>
          </div>
        </q-card>
      </div>

      <!-- Severity Overview -->
      <div class="col-12 col-md-4 overview-col">
        <q-card flat bordered class="overview-card">
          <div class="card-header row justify-between items-center q-mb-sm">
            <span class="card-title">Incidence Severity Overview</span>
            <q-menu>
              <template v-slot:anchor>
                <q-btn flat dense round icon="more_vert" size="sm" />
              </template>
              <q-list>
                <q-item clickable v-close-popup>
                  <q-item-section>Details</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </div>
          <div style="height: 250px">
            <canvas ref="severityChart"></canvas>
          </div>
        </q-card>
      </div>
    </div>

    <!-- Heatmap Card -->
    <q-card flat bordered class="heatmap-card">
      <div class="card-header row justify-between items-center q-mb-sm">
        <span class="card-title"
          >Anomaly Heat-map - Location-Based Anomaly Occurrence</span
        >
        <q-menu>
          <template v-slot:anchor>
            <q-btn flat dense round icon="more_vert" size="sm" />
          </template>
          <q-list>
            <q-item clickable v-close-popup>
              <q-item-section>Details</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </div>

      <!-- heatmap grid -->
      <div class="heatmap-grid">
        <div
          v-for="row in heatmapRows"
          :key="row.type"
          class="heatmap-row row items-center"
        >
          <div class="type-label">{{ row.type }}</div>
          <div class="cells row">
            <div
              v-for="(val, idx) in row.values"
              :key="idx"
              class="cell"
              :style="{ background: colorForValue(val) }"
            />
          </div>
        </div>

        <!-- legend -->
        <div class="legend q-ml-md column items-center">
          <div
            v-for="l in legendTicks"
            :key="l.label"
            class="row items-center q-mb-xs"
          >
            <div class="legend-box q-mr-xs" :style="{ background: l.color }" />
            <span class="legend-label">{{ l.label }}</span>
          </div>
        </div>
      </div>
    </q-card>
  </q-page>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import Chart from "chart.js/auto";

export default {
  name: "DashboardPage",
  setup() {
    const route = useRoute();
    const email = ref("");
    const name = ref("User");
    const siteCount = ref(2420);
    const cameraCount = ref(0);
    const alertCount = ref(4);

    // Loading states
    const isLoadingAnomaliesData = ref(true);
    const isLoadingTypesData = ref(true);

    // Chart refs
    const anomaliesChart = ref(null);
    const typesChart = ref(null);
    const severityChart = ref(null);

    // Chart instances
    let anomaliesChartInstance = null;
    let typesChartInstance = null;
    let severityChartInstance = null;

    // Data for charts
    const monthlyAnomaliesData = ref([]);
    const anomalyTypes = ref([]);
    const anomalyCounts = ref([]);
    const severityData = ref([]);

    // *** fake severity data (donut) ***
    severityData.value = [
      { label: "Critical", value: 60, color: "#a93d32" },
      { label: "High", value: 45, color: "#e79d26" },
      { label: "Medium", value: 25, color: "#f0c93b" },
      { label: "Low", value: 30, color: "#63a95d" }
    ];

    // *** fake heat-map data ***
    const zones = [
      "Zone A",
      "Zone B",
      "Zone C",
      "Zone D",
      "Zone E",
      "Zone F",
      "Zone G",
      "Zone H",
      "Zone I",
      "Zone J",
      "Zone K",
      "Zone L",
      "Zone M",
      "Zone N",
      "Zone O",
      "Zone P",
      "Zone Q",
      "Zone R",
      "Zone S"
    ];

    const heatmapRows = ref([
      "Unauthorized Access",
      "Cybersecurity Threats",
      "Fire and Smoke Detection",
      "Environmental Hazards",
      "Intrusion Detection",
      "Gas Leak",
      "Unusual loopholes"
    ].map((t) => ({
      type: t,
      values: zones.map(() => Math.floor(Math.random() * 31) + 1) // 1-31
    })));

    // legend ticks for heatmap
    const legendTicks = [
      { label: "-5", color: "#d32f2f" },
      { label: "-10", color: "#ef6c00" },
      { label: "-20", color: "#fbc02d" },
      { label: "-25", color: "#8bc34a" },
      { label: "-30", color: "#009688" }
    ];

    // fallbacks
    const fallbackMonths = [
      700, 920, 480, 770, 480, 840, 720, 780, 710, 800, 930, 650
    ];
    const fallbackTypes = ["Type A", "Type B", "Type C", "Type D"];
    const fallbackCounts = [480, 920, 650, 780];

    const apiBaseUrl = "http://16.171.224.57:0080";

    const fetchUserName = async () => {
      if (email.value) {
        try {
          const response = await axios.get(`${apiBaseUrl}/api/getName`, {
            params: { email: email.value }
          });
          name.value = String(response.data);
        } catch (error) {
          console.error("Error fetching name:", error);
        }
      }
    };

    const fetchCounts = async () => {
      try {
        const [sitesResult, camerasResult, alertsResult] = await Promise.all([
          axios.get(`${apiBaseUrl}/api/get-site-count`),
          axios.get(`${apiBaseUrl}/api/get-camera-count`),
          axios.get(`${apiBaseUrl}/api/get-hazard-count`)
        ]);
        siteCount.value = sitesResult.data || 0;
        cameraCount.value = camerasResult.data || 0;
        alertCount.value = alertsResult.data || 0;
      } catch (error) {
        console.error("Error fetching dashboard counts:", error);
        siteCount.value = cameraCount.value = alertCount.value = 0;
      }
    };

    const fetchAnomalyData = async () => {
      isLoadingAnomaliesData.value = true;
      try {
        const response = await axios.get(`${apiBaseUrl}/api/anomalies-by-month`);
        monthlyAnomaliesData.value = response.data || [];
      } catch (error) {
        console.error("Error fetching anomalies by month:", error);
        monthlyAnomaliesData.value = [];
      } finally {
        isLoadingAnomaliesData.value = false;
      }
    };

    const fetchAnomalyTypes = async () => {
      isLoadingTypesData.value = true;
      try {
        const response = await axios.get(`${apiBaseUrl}/api/anomalies-by-type`);
        anomalyTypes.value = response.data.types || [];
        anomalyCounts.value = response.data.counts || [];
      } catch (error) {
        console.error("Error fetching anomaly types:", error);
        anomalyTypes.value = [];
        anomalyCounts.value = [];
      } finally {
        isLoadingTypesData.value = false;
      }
    };

    const updateAnomaliesChart = () => {
      if (!anomaliesChart.value) return; // ADDED GUARD
      if (anomaliesChartInstance) anomaliesChartInstance.destroy();

      const data = monthlyAnomaliesData.value.length
        ? monthlyAnomaliesData.value
        : fallbackMonths;

      anomaliesChartInstance = new Chart(anomaliesChart.value, {
        type: "bar",
        data: {
          labels: [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
          ],
          datasets: [{ data, backgroundColor: "#f6a525" }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: {
              beginAtZero: true,
              title: { display: true, text: "Count of anomalies" }
            },
            x: { title: { display: true, text: "Month" } }
          }
        }
      });
    };

    const updateTypesChart = () => {
      if (!typesChart.value) return; // ADDED GUARD
      if (typesChartInstance) typesChartInstance.destroy();

      const labels = anomalyTypes.value.length
        ? anomalyTypes.value
        : fallbackTypes;
      const data = anomalyCounts.value.length
        ? anomalyCounts.value
        : fallbackCounts;

      typesChartInstance = new Chart(typesChart.value, {
        type: "bar",
        data: {
          labels,
          datasets: [{ data, backgroundColor: "#29cc97" }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: {
              beginAtZero: true,
              title: { display: true, text: "Occurrences" }
            },
            x: { title: { display: true, text: "Anomaly Type" } }
          }
        }
      });
    };

    // severity donut chart
    const updateSeverityChart = () => {
      if (!severityChart.value) return; // ADDED GUARD
      if (severityChartInstance) severityChartInstance.destroy();

      const labels = severityData.value.map((d) => d.label);
      const data = severityData.value.map((d) => d.value);
      const colors = severityData.value.map((d) => d.color);

      severityChartInstance = new Chart(severityChart.value, {
        type: "doughnut",
        data: {
          labels,
          datasets: [{
            data,
            backgroundColor: colors,
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: "55%",
          plugins: {
            legend: {
              position: "bottom",
              labels: {
                usePointStyle: true,
                boxWidth: 8
              }
            }
          }
        }
      });
    };

    // heatmap color scale
    const colorForValue = (v) => {
      if (v > 25) return "#009688";
      if (v > 20) return "#4caf50";
      if (v > 15) return "#fbc02d";
      if (v > 10) return "#ef6c00";
      return "#d32f2f";
    };

    onMounted(async () => {
      email.value = decodeURIComponent(route.query.email || "");

      await fetchUserName();
      await fetchCounts();

      await fetchAnomalyData();  // fetch anomalies monthly data
      await fetchAnomalyTypes(); // fetch anomaly types data

      // Now that data is ready AND canvases are mounted:
      updateAnomaliesChart();
      updateTypesChart();
      updateSeverityChart();
    });


    return {
      name,
      siteCount,
      cameraCount,
      alertCount,
      anomaliesChart,
      typesChart,
      severityChart,
      isLoadingAnomaliesData,
      isLoadingTypesData,
      heatmapRows,
      colorForValue,
      legendTicks
    };
  }
};
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap");

.dashboard {
  background: #fafafa;
  font-family: "Inter", sans-serif;
}

.header {
  .title {
    font-size: 2rem;
    font-weight: 700;
    color: #1e1e1e;
  }
  .subtitle {
    font-size: 1rem;
    color: #636e72;
    margin-bottom: 0.75rem;
  }
}

.stat-card {
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  .stat-label {
    font-size: 0.875rem;
    font-weight: 500;
    color: #636e72;
  }
  .stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #2d3436;
  }
}

.heatmap-card {
  padding: 1rem;
  .heatmap-grid {
    display: flex;
    overflow-x: auto;
  }
  .heatmap-row {
    margin-bottom: 6px;
    .type-label {
      width: 160px;
      font-size: 0.8rem;
      color: #455a64;
      text-align: right;
      padding-right: 8px;
    }
    .cells {
      .cell {
        width: 18px;
        height: 18px;
        margin: 2px;
        border-radius: 3px;
      }
    }
  }
  .legend {
    .legend-box {
      width: 14px;
      height: 14px;
      border-radius: 2px;
    }
    .legend-label {
      font-size: 0.7rem;
      color: #455a64;
    }
  }
}

.rounded {
  border-radius: 4px;
}
</style>
