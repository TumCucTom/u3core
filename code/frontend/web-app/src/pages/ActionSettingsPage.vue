<template>
    <q-page class="q-px-lg q-py-md">
      <div>
        <!-- title Section -->
        <div class="row justify-between items-center q-mb-lg">
          <div>
            <h1 class="text-h4 text-bold">Actions Setting</h1>
            <p class="text-subtitle2">
              Track, manage and forecast your customers and orders.
            </p>
          </div>
          <q-btn label="+ Add Recipient" color="primary" text-color="white" />
        </div>
  
        <!-- filters Section -->
        <div class="row justify-between items-center q-mb-md">
          <div class="row">
            <q-btn label="SMS" outline class="q-mx-sm" />
            <q-btn label="Email" outline class="q-mx-sm" />
            <q-btn label="Whatsapp" outline class="q-mx-sm" />
            <q-btn label="Twitter" outline class="q-mx-sm" />
          </div>
          <div class="row">
            <q-input outlined dense placeholder="Search" prefix="search" class="q-mr-md" />
            <q-btn label="All" flat icon="close" class="q-mx-sm" />
            <q-btn label="More filters" outline class="q-mx-sm" />
          </div>
        </div>
  
        <!-- mock table will fill with data from backend later -->
        <q-table
          flat
          rows-per-page-options="[5, 10, 15]"
          :rows="[]"
          :columns="columns"
          row-key="id"
        >
          <template v-slot:body>
            <tr>
              <td colspan="6" class="text-center text-grey">
                <q-icon name="info" size="md" /> No data available
              </td>
            </tr>
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
        columns: [
          { name: "recipientId", label: "Recipient Id", align: "left", field: "recipientId" },
          { name: "name", label: "Recipient name", align: "left", field: "name" },
          { name: "email", label: "Email", align: "left", field: "email" },
          { name: "phone", label: "Phone number", align: "left", field: "phone" },
          { name: "fault", label: "Fault Type", align: "left", field: "fault" },
          { name: "timestamp", label: "Timestamp", align: "left", field: "timestamp" },
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
  