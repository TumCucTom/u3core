<template>
  <q-page class="q-px-lg q-py-md">
    <div>
      <div class="q-mb-lg">
        <h1 class="text-h4 text-bold">Welcome back, {{name}}</h1>
        <p class="text-subtitle2">Track, manage and forecast your customers and orders.</p>
      </div>

      <!--  top level box -->
      <div class="row q-mb-lg">
        <q-card flat bordered class="col-12 col-md-4 q-pa-md">
          <!-- add button in the title line-->
          <div class="row justify-between items-center q-mb-sm">
            <div class="text-caption text-grey-7">Total Sites</div>
            <q-btn
              flat
              dense
              round
              class="q-ml-auto"
              size="sm"
              @click="handleSettingsClick"
            >
              <q-icon
                name="img:src/assets/infobutton.png"
                size="25px"
                color="grey-7"
              />
            </q-btn>
          </div>
          <div class="row justify-between items-center">
            <div class="text-h5 text-bold">{{ siteCount }}</div>
            <q-icon name="trending_up" color="positive" />
          </div>
        </q-card>

        <q-card flat bordered class="col-12 col-md-4 q-pa-md">
          <div class="row justify-between items-center q-mb-sm">
            <div class="text-caption text-grey-7">Cameras</div>
            <q-btn
              flat
              dense
              round
              class="q-ml-auto"
              size="sm"
              @click="handleSettingsClick"
            >
              <q-icon
                name="img:src/assets/infobutton.png"
                size="25px"
                color="grey-7"
              />
            </q-btn>
          </div>
          <div class="row justify-between items-center">
            <div class="text-h5 text-bold">{{ cameraCount }}</div>
            <q-icon name="trending_up" color="positive" />
          </div>
        </q-card>

        <q-card flat bordered class="col-12 col-md-4 q-pa-md">
          <div class="row justify-between items-center q-mb-sm">
            <div class="text-caption text-grey-7">Alerts</div>
            <q-btn
              flat
              dense
              round
              class="q-ml-auto"
              size="sm"
              @click="handleSettingsClick"
            >
              <q-icon
                name="img:src/assets/infobutton.png"
                size="25px"
                color="grey-7"
              />
            </q-btn>
          </div>
          <div class="row justify-between items-center">
            <div class="text-h5 text-bold">{{ alertCount }}</div>
            <q-icon name="trending_up" color="positive" />
          </div>
        </q-card>
      </div>

      <!-- charts section -->
      <div class="row q-mb-lg">
        <!-- left column -->
        <div class="col-12 col-md-8">
          <!-- number of anomalies -->
          <q-card flat bordered class="q-pa-md q-mb-md">
            <div class="row justify-between items-center q-mb-sm">
              <div class="text-h6">Number of Anomalies Detected</div>
              <q-btn
                flat
                dense
                round
                class="q-ml-auto"
                size="sm"
                @click="handleSettingsClick"
              >
                <q-icon
                  name="img:src/assets/infobutton.png"
                  size="25px"
                  color="grey-7"
                />
              </q-btn>
            </div>
            <!-- Chart.js canvas for Number of Anomalies -->
            <div style="height: 300px">
              <canvas ref="anomaliesChart"></canvas>
            </div>
            <div v-if="isLoadingAnomaliesData" class="text-center q-mt-md">
              <q-spinner color="primary" size="3em" />
              <div class="q-mt-sm">Loading anomaly data...</div>
            </div>
          </q-card>

          <!-- type of anomalies detected -->
          <q-card flat bordered class="q-pa-md">
            <div class="row justify-between items-center q-mb-sm">
              <div class="text-h6">Type of Anomalies Detected</div>
              <q-btn
                flat
                dense
                round
                class="q-ml-auto"
                size="sm"
                @click="handleSettingsClick"
              >
                <q-icon
                  name="img:src/assets/infobutton.png"
                  size="25px"
                  color="grey-7"
                />
              </q-btn>
            </div>
            <!-- Chart.js canvas for Type of Anomalies -->
            <div style="height: 300px">
              <canvas ref="typesChart"></canvas>
            </div>
            <div v-if="isLoadingTypesData" class="text-center q-mt-md">
              <q-spinner color="primary" size="3em" />
              <div class="q-mt-sm">Loading anomaly types data...</div>
            </div>
          </q-card>
        </div>

        <!-- right Column -->
        <div class="col-12 col-md-4">
          <!-- incidence severity overview -->
          <q-card flat bordered class="q-pa-md">
            <div class="row justify-between items-center q-mb-sm">
              <div class="text-h6">Incidence Severity Overview</div>
              <q-btn
                flat
                dense
                round
                class="q-ml-auto"
                size="sm"
                @click="handleSettingsClick"
              >
                <q-icon
                  name="img:src/assets/infobutton.png"
                  size="25px"
                  color="grey-7"
                />
              </q-btn>
            </div>
            <div class="text-grey-7 text-center q-mt-lg">No data available</div>
          </q-card>
        </div>
      </div>

      <!-- heatmap  -->
      <q-card flat bordered class="q-pa-md">
        <div class="row justify-between items-center q-mb-sm">
          <div class="text-h6">Anomaly Heat-map - Location-Based Anomaly Occurrence</div>
          <q-btn
            flat
            dense
            round
            class="q-ml-auto"
            size="sm"
            @click="handleSettingsClick"
          >
            <q-icon
              name="img:src/assets/infobutton.png"
              size="25px"
              color="grey-7"
            />
          </q-btn>
        </div>
        <div class="text-grey-7 text-center q-mt-lg">No data available</div>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Chart from 'chart.js/auto'

export default {
  name: 'DashboardPage',
  setup () {
    const email = ref('')
    const name = ref('User')
    const siteCount = ref(0)
    const cameraCount = ref(0)
    const alertCount = ref(0)

    // Loading states
    const isLoadingAnomaliesData = ref(true)
    const isLoadingTypesData = ref(true)

    // Chart references
    const anomaliesChart = ref(null)
    const typesChart = ref(null)

    // Chart instances
    let anomaliesChartInstance = null
    let typesChartInstance = null

    // Data for charts
    const monthlyAnomaliesData = ref([])
    const anomalyTypes = ref([])
    const anomalyCounts = ref([])

    const route = useRoute()

    const handleSettingsClick = () => {
      console.log('Settings button clicked')
      // add logic here for the button
    }

    // API base URL
    const apiBaseUrl = 'http://16.171.224.57:0080'

    const fetchCounts = async () => {
      try {
        const [sitesResult, camerasResult, alertsResult] = await Promise.all([
          axios.get(`${apiBaseUrl}/api/get-site-count`),
          axios.get(`${apiBaseUrl}/api/get-camera-count`),
          axios.get(`${apiBaseUrl}/api/get-hazard-count`)
        ])
        siteCount.value = sitesResult.data || 0
        cameraCount.value = camerasResult.data || 0
        alertCount.value = alertsResult.data || 0
      } catch (error) {
        console.error('Error fetching dashboard counts:', error.response?.data || error.message)
        // Set default values in case of error
        siteCount.value = 0
        cameraCount.value = 0
        alertCount.value = 0
      }
    }

    const fetchAnomalyData = async () => {
      isLoadingAnomaliesData.value = true
      try {
        const response = await axios.get(`${apiBaseUrl}/api/anomalies-by-month`)
        monthlyAnomaliesData.value = response.data
        updateAnomaliesChart()
      } catch (error) {
        console.error('Error fetching anomalies by month:', error.response?.data || error.message)
      } finally {
        isLoadingAnomaliesData.value = false
      }
    }

    const fetchAnomalyTypes = async () => {
      isLoadingTypesData.value = true
      try {
        const response = await axios.get(`${apiBaseUrl}/api/anomalies-by-type`)
        anomalyTypes.value = response.data.types
        anomalyCounts.value = response.data.counts
        updateTypesChart()
      } catch (error) {
        console.error('Error fetching anomaly types:', error.response?.data || error.message)
      } finally {
        isLoadingTypesData.value = false
      }
    }

    const updateAnomaliesChart = () => {
      if (anomaliesChartInstance) {
        anomaliesChartInstance.destroy()
      }

      if (anomaliesChart.value) {
        anomaliesChartInstance = new Chart(anomaliesChart.value, {
          type: 'bar',
          data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
              label: 'Count of anomalies',
              backgroundColor: '#f4a261',
              data: monthlyAnomaliesData.value
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              }
            },
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'Count of anomalies'
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Month'
                }
              }
            }
          }
        })
      }
    }

    const updateTypesChart = () => {
      if (typesChartInstance) {
        typesChartInstance.destroy()
      }

      if (typesChart.value) {
        typesChartInstance = new Chart(typesChart.value, {
          type: 'bar',
          data: {
            labels: anomalyTypes.value,
            datasets: [{
              label: 'Number of occurrences',
              backgroundColor: '#2a9d8f',
              data: anomalyCounts.value
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              }
            },
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'Number of occurrences'
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Types of anomalies'
                }
              }
            }
          }
        })
      }
    }

    const fetchUserName = async () => {
      if (email.value) {
        try {
          const response = await axios.get(`${apiBaseUrl}/api/getName`, {
            params: { email: email.value }
          })
          name.value = String(response.data)
        } catch (error) {
          console.error('Error fetching name:', error)
        }
      } else {
        console.error('No email found in the URL')
      }
    }

    onMounted(() => {
      email.value = decodeURIComponent(route.query.email || '')

      fetchUserName()
      fetchCounts()
      fetchAnomalyData()
      fetchAnomalyTypes()
    })

    return {
      handleSettingsClick,
      email,
      name,
      siteCount,
      cameraCount,
      alertCount,
      anomaliesChart,
      typesChart,
      isLoadingAnomaliesData,
      isLoadingTypesData
    }
  }
}
</script>

<style>
.q-page {
  background: #f9f9f9; /* Match light background */
}

.text-grey-7 {
  color: #a0a0b0;
}
</style>