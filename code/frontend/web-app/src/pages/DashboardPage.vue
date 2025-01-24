<template>
    <q-page class="q-px-lg q-py-md">
      <div>
        <div class="q-mb-lg">
          <h1 class="text-h4 text-bold">Welcome back, </h1>
          <p class="text-subtitle2">Track, manage and forecast your customers and orders.</p>
        </div>
  
        <!--  top level box -->
        <div class="row q-mb-lg">
          <q-card flat bordered class="col-12 col-md-4 q-pa-md">
            <div class="text-caption text-grey-7">Total Sites</div>
            <div class="row justify-between items-center">
              <div class="text-h5 text-bold">0</div>
              <q-icon name="trending_up" color="positive" />
            </div>
          </q-card>
          <q-card flat bordered class="col-12 col-md-4 q-pa-md">
            <div class="text-caption text-grey-7">Cameras</div>
            <div class="row justify-between items-center">
              <div class="text-h5 text-bold">0</div>
              <q-icon name="trending_up" color="positive" />
            </div>
          </q-card>
          <q-card flat bordered class="col-12 col-md-4 q-pa-md">
            <div class="text-caption text-grey-7">Alerts</div>
            <div class="row justify-between items-center">
              <div class="text-h5 text-bold">0</div>
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
              <div class="row justify-between items-center">
                <div class="text-h6">Number of Anomalies Detected</div>
                <q-icon name="more_vert" />
              </div>
              <div class="text-grey-7 text-center q-mt-lg">No data available</div>
            </q-card>
  
            <!-- type of anomalies detected -->
            <q-card flat bordered class="q-pa-md">
              <div class="row justify-between items-center">
                <div class="text-h6">Type of Anomalies Detected</div>
                <q-icon name="more_vert" />
              </div>
              <div class="text-grey-7 text-center q-mt-lg">No data available</div>
            </q-card>
          </div>
  
          <!-- right Column -->
          <div class="col-12 col-md-4">
            <!-- incidence severity overview -->
            <q-card flat bordered class="q-pa-md">
              <div class="row justify-between items-center">
                <div class="text-h6">Incidence Severity Overview</div>
                <q-icon name="more_vert" />
              </div>
              <div class="text-grey-7 text-center q-mt-lg">No data available</div>
            </q-card>
          </div>
        </div>
  
        <!-- heatmap  -->
        <q-card flat bordered class="q-pa-md">
          <div class="row justify-between items-center">
            <div class="text-h6">Anomaly Heat-map - Location-Based Anomaly Occurrence</div>
            <q-icon name="more_vert" />
          </div>
          <div class="text-grey-7 text-center q-mt-lg">No data available</div>
        </q-card>
      </div>
    </q-page>
  </template>
  
  <script>
  export default {
    name: "DashboardPage",
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
  