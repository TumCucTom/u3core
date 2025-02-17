<template>
    <q-page class="q-px-lg q-py-md">
      <div>
        <!-- title section -->
        <div class="row justify-between items-center q-mb-lg">
          <div>
            <h1 class="text-h4 text-bold">Manage Models</h1>
            <p class="text-subtitle2">
              Track, manage and forecast your models and performance.
            </p>
          </div>
          <q-btn label="+ Add Model" color="primary" text-color="white" />
        </div>
  
        <!-- filters -->
        <div class="row q-my-md">
          <q-btn-group unelevated>
            <q-btn label="All" />
            <q-btn label="Active" />
            <q-btn label="Paused" />
            <q-btn label="Completed" />
          </q-btn-group>
          <q-input
            outlined
            dense
            placeholder="Search"
            prefix="search"
            class="q-ml-lg"
            style="max-width: 300px;"
          />
        </div>
  
        <!-- table empty data needs to be filled from backend -->
        <q-table
          flat
          rows-per-page-options="[5, 10, 15]"
          :rows="[]"
          :columns="columns"
          row-key="id"
          no-data-label="No models available yet"
        >
          
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
        // columns for format
        columns: [
          { name: "name", align: "left", label: "Model Name", field: "name" },
          { name: "createdBy", align: "left", label: "Created By", field: "createdBy" },
          { name: "status", align: "left", label: "Status", field: "status" },
          { name: "createdAt", align: "left", label: "Created At", field: "createdAt" },
          { name: "actions", align: "left", label: "Actions", field: "actions" },
        ],
      };
    },
  };
  </script>
  
  <style>
  .q-page {
    background: #f9f9f9; /* Match light background */
  }
  </style>
  