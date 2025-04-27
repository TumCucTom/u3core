<template>
  <q-page class="q-px-lg q-py-md">
    <div>
      <div class="row justify-between items-center q-mb-lg">
        <div>
          <h1 class="text-h4 text-weight-bold">Actions Setting</h1>
          <p class="text-subtitle2">
            Track, manage and forecast your customers and orders.
          </p>
        </div>
        <q-btn
          label="+ Add Recipient"
          color="dark"
          text-color="white"
          unelevated
          class="q-px-md q-py-sm"
          @click="showAddRecipient = true"
        />
      </div>

      <q-tabs
        v-model="activeChannel"
        dense
        inline-label
        class="q-mb-md"
        active-color="dark"
      >
        <q-tab v-for="c in channels" :key="c" :name="c" :label="c" />
      </q-tabs>

      <div class="row items-center q-mb-md">
        <q-input
          outlined
          rounded
          dense
          placeholder="Search"
          v-model="search"
          style="width: 320px;"
        >
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
        </q-input>

        <q-chip
          removable
          class="q-ml-md bg-grey-2 text-black"
        >
          All
        </q-chip>

        <q-btn
          flat
          dense
          icon="filter_list"
          label="More filters"
          class="q-ml-sm text-weight-medium"
        />
      </div>

      <q-table
        flat
        bordered
        :rows="rows"
        :columns="columns"
        row-key="id"
        selection="multiple"
        hide-pagination
      >
        <template v-slot:body-cell-faultType="props">
          <q-td :props="props">
            <q-badge
              :label="props.value"
              :color="faultColor(props.value)"
              align="top"
              transparent
            />
          </q-td>
        </template>
      </q-table>

      <div class="row justify-between items-center q-mt-md">
        <q-btn flat label="Previous" />
        <q-btn flat label="Next" />
        <div class="text-caption text-grey-7">Page 1 of 10</div>
      </div>
    </div>

    <q-dialog v-model="showAddRecipient" persistent>
      <q-card style="width: 500px; max-width: 90vw;">
        <q-card-section class="row justify-between items-start">
          <div class="row items-center">
            <q-avatar icon="person" color="grey-2" text-color="dark" class="q-mr-sm" />
            <div>
              <div class="text-h6 text-weight-bold">Add Recipient</div>
              <div class="text-caption">Create a new recipient for the alert service.</div>
            </div>
          </div>
          <q-btn dense flat round icon="close" v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section class="q-gutter-md">
          <q-input
            outlined
            dense
            rounded
            v-model="recipientName"
            label="Recipient name*"
            placeholder="Sharjat P"
          />
          <q-input
            outlined
            dense
            rounded
            v-model="recipientEmail"
            label="Email"
            placeholder="email123@gmail.com"
          />
          <q-input
            outlined
            dense
            rounded
            v-model="recipientPhone"
            label="Phone number"
            placeholder="+91 example"
          />
          <div class="row items-center">
            <q-toggle v-model="receiveAllChannels" size="md" dense />
            <div class="text-caption q-ml-sm">
              Sms, Email, WhatsApp, Tweets related to alerts are to be sent on this number & email.
            </div>
          </div>
          <q-select
            outlined
            dense
            rounded
            v-model="selectedAlert"
            :options="alertOptions"
            label="Select Alert"
            placeholder="Select"
            emit-value
            map-options
            transition-show="none"
            transition-hide="none"
            dropdown-icon=" "
          >
            <template v-slot:append>
              <q-icon name="expand_more" />
            </template>
          </q-select>
          <q-select
            outlined
            dense
            rounded
            use-chips
            multiple
            hide-dropdown-icon
            v-model="selectedSites"
            :options="siteOptions"
            label="Assign Site"
            placeholder="Select"
          >
            <template v-slot:append>
              <q-icon name="expand_more" />
            </template>
          </q-select>
        </q-card-section>

        <q-card-actions class="row justify-between q-px-md q-pb-md">
          <q-btn
            flat
            label="Cancel"
            v-close-popup
            class="q-px-lg"
          />
          <q-btn
            label="Save"
            color="dark"
            text-color="white"
            class="q-px-xl"
            @click="saveRecipient"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
export default {
  data() {
    return {
      showAddRecipient: false,
      activeChannel: "Sms",
      channels: ["Sms", "Email", "WhatsApp", "Tweets"],
      search: "",
      columns: [
        { name: "id", label: "Recipient Id", field: "id", align: "left", sortable: true },
        { name: "name", label: "Recipient name", field: "name", align: "left" },
        { name: "phone", label: "Phone number", field: "phone", align: "left" },
        { name: "faultType", label: "Fault Type", field: "faultType", align: "left" },
        { name: "timestamp", label: "Timestamp", field: "timestamp", align: "left" }
      ],
      rows: [
        {
          id: "REC-28374XX",
          name: "Alice Johnson",
          phone: "555-1234",
          faultType: "Oil leak",
          timestamp: "2024-11-05 08:30 AM"
        },
        {
          id: "REC-76192AE",
          name: "Bob Smith",
          phone: "555-9876",
          faultType: "Water leak",
          timestamp: "2024-11-05 12:45 PM"
        },
        {
          id: "REC-49587ZT",
          name: "Cathy Brown",
          phone: "555-4567",
          faultType: "Fire",
          timestamp: "2024-11-05 03:15 PM"
        },
        {
          id: "REC-39018PL",
          name: "Daniel Lee",
          phone: "555-7890",
          faultType: "Smoke",
          timestamp: "2024-11-06 09:00 AM"
        },
        {
          id: "REC-45107CR",
          name: "Eve Smith",
          phone: "555-2468",
          faultType: "Water leak",
          timestamp: "2024-11-06 01:30 PM"
        },
        {
          id: "REC-98016VH",
          name: "Frank Wright",
          phone: "555-1357",
          faultType: "Fire",
          timestamp: "2024-11-06 05:00 PM"
        },
        {
          id: "REC-39018PL",
          name: "Grace Lee",
          phone: "555-7410",
          faultType: "Oil leak",
          timestamp: "2024-11-07 10:15 AM"
        }
      ],
      alertOptions: [
        { label: "Fire Alert", value: "Fire Alert" },
        { label: "Water Alert", value: "Water Alert" },
        { label: "Oil Alert", value: "Oil Alert" }
      ],
      siteOptions: ["Site 0001", "Site 0002", "Site 0003"],
      selectedAlert: "Fire Alert",
      selectedSites: ["Site 0001", "Site 0002"],
      recipientName: "Sharjat P",
      recipientEmail: "email123@gmail.com",
      recipientPhone: "",
      receiveAllChannels: false
    };
  },
  methods: {
    faultColor(type) {
      switch (type) {
        case "Oil leak":
          return "amber-4";
        case "Water leak":
          return "light-blue-4";
        case "Fire":
          return "red-4";
        case "Smoke":
          return "purple-4";
        default:
          return "grey-4";
      }
    },
    saveRecipient() {
      this.showAddRecipient = false;
    }
  }
};
</script>

<style>
.q-page {
  background: #ffffff;
}
</style>
