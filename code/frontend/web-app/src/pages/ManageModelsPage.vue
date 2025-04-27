<template>
  <q-page class="q-px-lg q-py-md">
    <div>
      <!-- title section -->
      <div class="row justify-between items-center q-mb-lg">
        <div>
          <h1 class="text-h4 text-weight-bold">Manage Models</h1>
          <p class="text-subtitle2">
            Track, Manage and Configure models
          </p>
        </div>
        <q-btn
          label="+ Upload New Model"
          color="dark"
          text-color="white"
          unelevated
          class="q-px-md q-py-sm"
          @click="showUploadDialog = true"
        />
      </div>

      <!-- filters -->
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

      <!-- table empty data needs to be filled from backend -->
      <q-table
        flat
        bordered
        :rows="rows"
        :columns="columns"
        row-key="id"
        selection="multiple"
        hide-pagination
      >
        <template v-slot:body-cell-useCase="props">
          <q-td :props="props">
            <q-badge
              :label="props.value"
              :color="useCaseColor(props.value)"
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

    <q-dialog v-model="showUploadDialog" persistent>
      <q-card style="width: 600px; max-width: 90vw;">
        <q-card-section class="row justify-between items-start">
          <div>
            <div class="text-h5 text-weight-bold">Upload Model</div>
            <div class="text-caption">Upload relevant images to train data.</div>
          </div>
          <q-btn dense flat round icon="close" v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section>
          <div class="q-gutter-md">
            <div>
              <div class="text-subtitle2 q-mb-xs">Assign Use Cases</div>
              <q-select
                outlined
                dense
                rounded
                use-chips
                multiple
                hide-dropdown-icon
                v-model="selectedUseCases"
                :options="useCaseOptions"
                placeholder="Select"
              />
            </div>

            <div>
              <div class="text-subtitle2 q-mb-xs">Model name</div>
              <q-input
                outlined
                dense
                rounded
                v-model="modelName"
                placeholder="Model 001"
              />
            </div>

            <div>
              <div class="text-subtitle2 q-mb-xs">Description</div>
              <q-input
                type="textarea"
                outlined
                dense
                v-model="modelDescription"
                placeholder="Added 3 labels to the model 001, Model 002, Model 003."
                style="min-height: 120px;"
              />
            </div>

            <quploader
              v-model="uploadedFiles"
              accept=".svg,.png,.jpg,.jpeg,.gif,.py"
              label="Click to upload or drag and drop"
              square
              flat
              outlined
              :no-thumbnails="true"
              max-file-size="20971520"
            >
              <template v-slot:header>
                <div class="full-width column items-center justify-center q-pa-md">
                  <q-icon name="cloud_upload" size="32px" />
                  <div class="text-negative text-subtitle2">Click to upload</div>
                  <div class="text-caption">SVG, PNG, JPG or GIF (max. 800x400px)</div>
                </div>
              </template>
            </quploader>

            <div
              v-for="file in uploadedFiles"
              :key="file.__key"
              class="row items-center q-pa-sm q-mb-sm bg-grey-1 rounded-borders"
            >
              <q-icon name="insert_drive_file" size="28px" class="text-pink-5 q-mr-sm" />
              <div class="col">
                <div class="text-body2">{{ file.name }}</div>
                <div class="text-caption text-grey-7">
                  {{ prettySize(file.size) }} – {{ file.__uploadPercentage }}% uploaded
                </div>
              </div>
              <q-checkbox dense v-model="file.selected" />
            </div>
          </div>
        </q-card-section>

        <q-card-actions class="row justify-between">
          <q-btn flat label="Skip" v-close-popup />
          <q-btn color="dark" text-color="white" label="Save Progress" @click="saveProgress" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
export default {
  data() {
    return {
      showUploadDialog: false,
      search: "",
      columns: [
        { name: "id", label: "Model Id", field: "id", align: "left", sortable: true },
        { name: "name", label: "Model name", field: "name", align: "left" },
        { name: "uploadedBy", label: "Uploaded by", field: "uploadedBy", align: "left" },
        { name: "lastRevision", label: "Last Revision date", field: "lastRevision", align: "left" },
        { name: "useCase", label: "Use Case", field: "useCase", align: "left" },
        { name: "description", label: "Description", field: "description", align: "left" }
      ],
      rows: [
        {
          id: "REC-90213AB",
          name: "Model X01",
          uploadedBy: "Oliver Stone",
          lastRevision: "2025-04-10 08:00 AM",
          useCase: "Oil leak",
          description: "Model uploaded. Pipelines live."
        },
        {
          id: "REC-84275BC",
          name: "Model GT9",
          uploadedBy: "Sophia Green",
          lastRevision: "2025-04-10 09:45 AM",
          useCase: "Water leak",
          description: "Upload complete. Syncing now."
        },
        {
          id: "REC-73481CD",
          name: "Model T03",
          uploadedBy: "Liam Taylor",
          lastRevision: "2025-04-10 11:10 AM",
          useCase: "Fire",
          description: "Model deployed. Let's go!"
        },
        {
          id: "REC-62847DE",
          name: "Model X04",
          uploadedBy: "Ava Hughes",
          lastRevision: "2025-04-09 02:35 PM",
          useCase: "Smoke",
          description: "Model live. Integration now."
        },
        {
          id: "REC-51936EF",
          name: "Model E22",
          uploadedBy: "Ethan Wood",
          lastRevision: "2025-04-09 04:20 PM",
          useCase: "Water leak",
          description: "Upload successful. Data active."
        },
        {
          id: "REC-47382FG",
          name: "Model X0X",
          uploadedBy: "Mia Brown",
          lastRevision: "2025-04-08 06:50 PM",
          useCase: "Fire",
          description: "Model in place. Next steps."
        },
        {
          id: "REC-36519GH",
          name: "Model RE2",
          uploadedBy: "Noah Smith",
          lastRevision: "2025-04-08 08:10 AM",
          useCase: "Oil leak",
          description: "Leakage confirmed via camera feed on Unit 7"
        }
      ],
      useCaseOptions: ["Oil leak", "Water leak", "Fire detection", "Smoke detection"],
      selectedUseCases: ["Fire detection", "Smoke detection"],
      modelName: "Model 001",
      modelDescription: "Added 3 labels to the model 001, Model 002, Model 003.",
      uploadedFiles: [
        {
          __key: 1,
          name: "Oil Leak Industrial.py",
          size: 204800,
          __uploadPercentage: 100,
          selected: true
        },
        {
          __key: 2,
          name: "Solar panel crack.py",
          size: 204800,
          __uploadPercentage: 70,
          selected: false
        },
        {
          __key: 3,
          name: "Boarder breach.py",
          size: 204800,
          __uploadPercentage: 70,
          selected: false
        }
      ]
    };
  },
  methods: {
    useCaseColor(useCase) {
      switch (useCase) {
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
    prettySize(size) {
      return (size / 1024).toFixed(0) + " KB";
    },
    saveProgress() {
      this.showUploadDialog = false;
    }
  }
};
</script>

<style>
.q-page {
  background: #ffffff;
}
</style>
