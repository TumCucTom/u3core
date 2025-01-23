<template>
    <q-page class="q-pa-lg flex flex-center full-height bg-light">
      <div class="verification-box column items-center q-px-xl q-py-lg shadow-2 rounded-borders bg-white">
        
        <q-avatar size="80px" class="q-mb-md bg-light-pink text-pink">
          <q-icon name="email" size="40px" />
        </q-avatar>
  
        
        <h2 class="text-bold text-center">Check your email</h2>
        <p class="text-subtitle1 text-center">
          We sent a verification link to <span class="text-bold">olivia@untitledui.com</span>
        </p>
  
       
        <div class="row q-my-lg justify-center">
          <q-input
            v-for="(otp, index) in otpFields"
            :key="index"
            v-model="otpFields[index]"
            maxlength="1"
            type="text"
            class="otp-box text-center q-mx-xs"
            input-class="text-pink text-h5"
          />
        </div>
  
        
        <q-btn label="Verify email" color="pink" class="full-width q-my-md text-white" />
        <p class="text-caption text-center q-mt-sm">
          Didn’t receive the email? 
          <span class="text-pink cursor-pointer">Click to resend</span>
        </p>
        <q-btn flat class="q-mt-md" label="Back to log in" icon="west" color="dark" />
      </div>
    </q-page>
  </template>
  
  <script>
  export default {
    data() {
      return {
        otpFields: ['', '', '', ''], // array for the code 
      };
    },
  };
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
  