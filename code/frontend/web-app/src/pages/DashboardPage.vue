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
                  name = "img:src/assets/infobutton.png"
                  size = "25px"
                  color = "grey-7"
                />
              </q-btn>
            </div>
            <div class="row justify-between items-center">
              <div class="text-h5 text-bold">{{siteCount}}</div>
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
                  name = "img:src/assets/infobutton.png"
                  size = "25px"
                  color = "grey-7"
                />
              </q-btn>
            </div>
            <div class="row justify-between items-center">
              <div class="text-h5 text-bold">{{cameraCount}}</div>
              <q-icon name="trending_up" color="positive" /></div>
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
                  name = "img:src/assets/infobutton.png"
                  size = "25px"
                  color = "grey-7"
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
                  name = "img:src/assets/infobutton.png"
                  size = "25px"
                  color = "grey-7"
                />
              </q-btn>
              </div>
              <div class="text-grey-7 text-center q-mt-lg">No data available</div>
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
                  name = "img:src/assets/infobutton.png"
                  size = "25px"
                  color = "grey-7"
                />
              </q-btn>
              </div>
              <div class="text-grey-7 text-center q-mt-lg">No data available</div>
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
                  name = "img:src/assets/infobutton.png"
                  size = "25px"
                  color = "grey-7"
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
                  name = "img:src/assets/infobutton.png"
                  size = "25px"
                  color = "grey-7"
                />
              </q-btn>
          </div>
          <div class="text-grey-7 text-center q-mt-lg">No data available</div>
        </q-card>
      </div>
    </q-page>
  </template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

export default {
  name: "DashboardPage",
  setup() {
    const email = ref('');
    const name = ref('User'); // Use a ref for the name variable
    const siteCount = ref(100);
    const cameraCount = ref(100);
    const alertCount = ref(100);


    const route = useRoute();
    const handleSettingsClick = () => {
    console.log('Settings button clicked');
    // add logic here for the button
    };

    const fetchCounts = async () => {
      try {
        const [sitesResult, camerasResult, alertsResult] = await Promise.all([
          axios.get("http://127.0.0.1:3002/api/get-site-count"),
          axios.get("http://127.0.0.1:3002/api/get-camera-count"),
          axios.get("http://127.0.0.1:3002/api/get-hazard-count")
        ]);
      siteCount.value = sitesResult.data || 0;
      cameraCount.value = camerasResult.data || 0;
      alertCount.value = alertsResult.data || 0;
  } catch (error) {
    console.error("Error fetching dashboard counts:", error.response?.data || error.message);
  }
    };
    onMounted(() => {
      email.value = decodeURIComponent(route.query.email || '');
      if (email.value) {
        axios
          .get(`http://16.171.224.57:3002/api/getName`, {
            params: { email: email.value }, // Pass the email as a query parameter
          })
          .then((response) => {
            name.value = String(response.data); // Update the name with the backend response
          })
          .catch((error) => {
            console.error('Error fetching name:', error);
          });
      } else {
        console.error('No email found in the URL');
      }

      fetchCounts(); 
    });

    return {
      handleSettingsClick,
      email,
      name,
      siteCount,
      cameraCount,
      alertCount,
    };
  },
};
</script>

<style>
.q-page {
  background: #f9f9f9; /* Match light background */
}

.text-grey-7 {
  color: #a0a0b0;
}
</style>
