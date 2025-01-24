<template>
  <div class="q-pa-md q-gutter-y-sm">
    <q-toolbar class="text-primary-5" style="color: #0e004d">
      <q-icon name="lock" style="color: #0e004d; font-size: 2em;"/>
      <q-toolbar-title><strong>Password Verified</strong></q-toolbar-title>
    </q-toolbar>
  </div>
</template>


<script>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

export default {
  name: "VerifiedPassword",
  setup() {
    const router = useRouter();
    const email = ref('');
    const token = ref('');

    onMounted(() => {
      const route = useRoute();
      token.value = route.query.token;
      email.value = decodeURIComponent(route.query.email);

      console.log('Token from URL:', token.value, 'Email from URL:', email.value);

      if (!token.value || !email.value) {
        console.warn("No token or email provided, redirecting to home.");
        router.push('/');
      } else {
        console.log('Successful verification')
        router.push('/Dashboard')
      }
    });
  }
}
</script>

<style scoped>
.q-card {
  border: 1px solid #f04c26;
  background: linear-gradient(to bottom, rgba(245, 245, 245, 1) 0%, rgba(255, 255, 255, 0.95) 50%, rgba(245, 245, 245, 1) 100%) !important;
  box-shadow: 0 8px 10px rgba(0, 0, 0, 0.15);
}

:deep(.gradient-button) {
  background: linear-gradient(to right, #0e004d, #064e81) !important;
  color: white !important;
}

:deep(.gradient-button:hover) {
  background: linear-gradient(to right, #064e81, #0e004d) !important;
}

.cursor-pointer {
  cursor: pointer;
}
</style>

