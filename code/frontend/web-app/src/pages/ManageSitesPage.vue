<script>
import axios from 'axios'

export default {
  data() {
    return {
      showAddSite: false,
      metrics: {
        totalSites: 2420,
        operationalCams: 1210,
        allAlerts: 316
      },
      columns: [
        { name: "name", label: "Site name", field: "name", align: "left", sortable: true },
        { name: "location", label: "Site Location", field: "location", align: "left" },
        { name: "camera", label: "Associated Camera", field: "camera", align: "left" },
        { name: "gateway", label: "Gateway", field: "gateway", align: "left" }
      ],
      rows: [ /* your rows data */ ],
      siteName: "",
      longitude: "",
      latitude: "",
      locationZone: "",
      description: "",
      videoSrc: "",   // for saveNewRTSP
      newCamera: {
        name: '',
        RTSPURL: ''
      }
    };
  },
  methods: {
    closeAddRTSP() {
      this.addRTSP = false;
    },
    async saveNewRTSP() {
      try {
        const response = await axios.post('http://16.171.224.57:80/api/add-camera', {
          name: this.newCamera.name,
          rtsp_url: this.newCamera.RTSPURL,
        });
        console.log('Server Response:', response.data);
        this.closeAddRTSP();
        this.videoSrc = this.newCamera.RTSPURL;
        console.log('Video Source:', this.videoSrc)
        await this.startLiveStream();
      } catch (error) {
        console.error('Error saving new RTSP:', error);
      }
    },
    async saveSite() {  // <--- rename to match your button @click="saveSite"
      try {
        const response = await axios.post('http://16.171.224.57:80/add-site', {
          name: this.siteName,
          latitude: this.latitude,
          longitude: this.longitude,
        });
        console.log('Server Response:', response.data);
        this.closeAddSiteDialog(); // make sure you have this method or replace with showAddSite = false
      } catch (error) {
        console.error('Error saving new site:', error);
      }
    },
    async fetchSites() {
      try {
        const response = await axios.get('http://16.171.224.57:80/sites');
        this.sites = response.data.sites;
      } catch (error) {
        console.error('Error fetching sites:', error);
      }
    },
    resetForm() {
      this.siteName = '';
      this.longitude = '';
      this.latitude = '';
      this.locationZone = '';
      this.description = '';
      this.newCamera = { name: '', RTSPURL: '' };
    }
  }
}
</script>


<style>
.q-page {
  background: #f9f9f9;
}
</style>
