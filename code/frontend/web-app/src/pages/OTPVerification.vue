<template>
  <div class="q-pa-md q-gutter-y-sm">
    <!-- OTP Verification section heading -->
    <q-toolbar class="text-primary-5" style="color: #0e004d">
      <q-icon name="mail" style="color: #0e004d; font-size: 2em;"/>
      <q-toolbar-title><strong>OTP VERIFICATION</strong></q-toolbar-title>
    </q-toolbar>

    <!-- Instructions for OTP verification-->
    <q-card class="q-mt-md">
      <q-card-section>
        <div class="text-h6" style="text-align: center">How to verify</div>
        <div class="text-body1" style="text-align: left; margin-top: 20px;">
          <ul>
            <li>An email will have been sent to you including a 4 digit numerical code</li>
            <li>Use the code in the following section to verify yourself</li>
          </ul>
        </div>
      </q-card-section>
    </q-card>

    <!-- Email input form card -->
    <q-card class="q-mt-md">
      <q-card-section>
        <div class="text-h6" style="text-align: center">Verify Yourself</div>
        <q-input
          filled
          v-model.number="givenCode"
          label="Verification code"
          type="CodeVerification"
          class="q-mt-md"
          :rules="[val => val.length > 0 || 'Please Enter a code',
          val => val.length === 4 || 'This is not a valid format for the code'
          ]"
        />
        <div class="text-center q-mt-md">
          <q-btn class="gradient-button" @click="verifyCode" label="Enter verification code" type="button" rounded push />
        </div>
      </q-card-section>
    </q-card>

    <!-- Resend Email section -->
    <q-card class="q-mt-md">
      <q-card-section>
        <div class="text-body1" style="text-align: center; margin-bottom: 10px;">
          If you haven't received an email, please press the button below to resend the email.
        </div>
        <div class="text-center">
          <q-btn class="gradient-button" @click="resendEmail" label="Resend Email" type="button" rounded push />
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
  name: "CodeVerification",
  setup() {
    const router = useRouter();
    const $q = useQuasar();
    let givenCode = ref(null);

    const verifyCode = async () => {
      try {
        const response = await axios.post('http://localhost:3002/api/checkCode', { code: givenCode.value });
        if (response === true) {
          $q.notify({
            color: 'green-4',
            textColor: 'white',
            icon: 'email',
            message: 'Verification successful. Please wait to be redirected.'
          });
        }
        else{
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'error',
            message: 'Incorrect code. Please try again'
          });
        }
      } catch (error) {
        console.error('Error with verification of email:', error);
        $q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'error',
          message: 'Error with verification of email'
        });
      }
    };

    const resendEmail = async () => {
      try {
        const response = await axios.post('http://localhost:3002/api/sendVerifyEmail', { email: 'info@shopveloworks.com' });
        $q.notify({
          color: 'green-4',
          textColor: 'white',
          icon: 'email',
          message: 'Verification email resent successfully. Please check your inbox.'
        });
      } catch (error) {
        console.error('Error resending verification email:', error);
        $q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'error',
          message: 'Error resending verification email'
        });
      }
    };

    return {
      givenCode,
      verifyCode,
      resendEmail
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
