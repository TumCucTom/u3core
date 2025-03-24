<template>
    <q-page class="q-pa-lg flex flex-center full-height bg-light">
      <div class="verification-box column items-center q-px-xl q-py-lg shadow-2 rounded-borders bg-white">

        <q-avatar size="80px" class="q-mb-md bg-light-pink text-pink">
          <q-icon name="email" size="40px" />
        </q-avatar>


        <h2 class="text-bold text-center">Check your email</h2>
        <p class="text-subtitle1 text-center">
          We sent a verification link to <span class="text-bold" id="retrievedEmail"> </span>
        </p>


        <p class="text-caption text-center q-mt-sm" @click="resendEmail">
          Didn’t receive the email?
          <span class="text-pink cursor-pointer"><b>Click to resend</b></span>
        </p>
        <q-btn flat class="q-mt-md" label="Back to log in" icon="west" color="dark" />
      </div>
    </q-page>
  </template>

  <script>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useQuasar } from 'quasar';
  import axios from 'axios';

  export default {
    name: "CodeVerification",

    mounted() {
      this.sendEmail();
    },

    methods: {
      async sendEmail() {
        try {
          let retrievedEmail = sessionStorage.getItem("emailTransfer")
          document.getElementById("retrievedEmail").innerHTML = retrievedEmail
          const response = await axios.post('http://16.171.224.57:0080/api/sendVerifyEmail', { email: retrievedEmail });

        }
        catch (error) {
        console.error("Error fetching alerts:", error);
      }
      }
    },

    setup() {
      const router = useRouter();
      const $q = useQuasar();
      let givenCode = ref(null);

      const verifyCode = async () => {
        try {
          const response = await axios.post('http://16.171.224.57:0080/api/checkCode', { code: givenCode.value });
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
          let retrievedEmail = sessionStorage.getItem("emailTransfer")
          const response = await axios.post('http://16.171.224.57:0080/api/sendVerifyEmail', { email: retrievedEmail });
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

  <style>
  .bg-light {
    background-color: #f9fafb;
  }
  .full-height {
    height: 100vh;
  }
  .verification-box {
    max-width: 400px;
  }
  .otp-box {
    width: 50px;
    height: 50px;
    border: 2px solid #f48fb1;
    border-radius: 8px;
  }
  .otp-box input {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
  }
  .text-pink {
    color: #f48fb1;
  }
  .bg-light-pink {
    background-color: #fdecef;
  }
  .rounded-borders {
    border-radius: 16px;
  }
  </style>
