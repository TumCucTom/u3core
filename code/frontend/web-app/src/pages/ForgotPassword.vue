<template>
  <div class="q-pa-md q-gutter-y-sm">
    <!-- Email Verification section heading -->
    <q-toolbar class="text-primary-5" style="color: #0e004d">
      <q-icon name="mail" style="color: #0e004d; font-size: 2em;"/>
      <q-toolbar-title><strong>EMAIL VERIFICATION</strong></q-toolbar-title>
    </q-toolbar>

    <!-- Instructions to Change Password section -->
    <q-card class="q-mt-md">
      <q-card-section>
        <div class="text-h6" style="text-align: center">Instructions to Change Password</div>
        <div class="text-body1" style="text-align: left; margin-top: 20px;">
          <ul>
            <li>Input your email below.</li>
            <li>An email will be sent to you asking for verification</li>
            <li>Follow the email instructions and you will be redirected to the password changing page</li>
          </ul>
        </div>
      </q-card-section>
    </q-card>

    <!-- Email input form card -->
    <q-card class="q-mt-md">
      <q-card-section>
        <div class="text-h6" style="text-align: center">Verify Your Email</div>
        <q-input
          filled
          v-model="email"
          label="Email Address"
          type="email"
          class="q-mt-md"
          :rules="[val => val && val.length > 0 || 'Please enter an email address']"
        />
        <div class="text-center q-mt-md">
          <q-btn class="gradient-button" @click="sendVerificationEmail" label="Send Verification Email" type="button" rounded push />
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import axios from 'axios';

export default {
  name: "EmailVerification",
  setup() {
    const router = useRouter();
    const $q = useQuasar();
    const email = ref('');

    const sendVerificationEmail = async () => {
      try {
        const response = await axios.post('http://localhost:3000/api/sendEmail', { email: email.value });
        console.log('Verification email sent successfully:', response);
        $q.notify({
          color: 'green-4',
          textColor: 'white',
          icon: 'email',
          message: 'Verification email sent successfully. Please check your inbox.'
        });
      } catch (error) {
        console.error('Error sending verification email:', error);
        $q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'error',
          message: 'Error sending verification email'
        });
      }
    };

    return {
      email,
      sendVerificationEmail
    };
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



