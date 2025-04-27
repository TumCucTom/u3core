<template>
  <div class="q-pa-md q-gutter-y-sm">
    <q-toolbar class="text-primary-5" style="color: #0e004d">
      <q-icon name="lock" style="color: #0e004d; font-size: 2em;"/>
      <q-toolbar-title><strong>RESET PASSWORD</strong></q-toolbar-title>
    </q-toolbar>

    <!-- Instructions card -->
    <q-card class="q-mt-md">
      <q-card-section>
        <div class="text-h6" style="text-align: center">Password Requirements</div>
        <div class="text-body1" style="text-align: left; margin-top: 20px;">
          <ul>
            <li>At least 8 characters long</li>
            <li>At least one capital letter</li>
            <li>At least one number</li>
            <li>At least one special character</li>
          </ul>
        </div>
      </q-card-section>
    </q-card>

    <!-- Password input and reset card -->
    <q-card class="q-mt-md">
      <q-card-section>
        <div class="text-h6" style="text-align: center">Enter Your New Password</div>
        <q-input
          filled
          v-model="newPassword"
          :type="showPassword ? 'text' : 'password'"
          label="New Password"
          class="q-mt-md"
          :rules="passwordRules">
          <template v-slot:append>
            <q-icon
              :name="showPassword ? 'visibility' : 'visibility_off'"
              class="cursor-pointer"
              @click="togglePassword"/>
          </template>
        </q-input>

        <q-input
          filled
          v-model="confirmPassword"
          :type="showConfirmPassword ? 'text' : 'password'"
          label="Confirm New Password"
          class="q-mt-md"
          :rules="confirmPasswordRules">
          <template v-slot:append>
            <q-icon
              :name="showConfirmPassword ? 'visibility' : 'visibility_off'"
              class="cursor-pointer"
              @click="toggleConfirmPassword"/>
          </template>
        </q-input>

        <div class="text-center q-mt-md">
          <q-btn class="gradient-button" @click="resetPassword" label="Reset Password" type="button" rounded push />
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>


<script>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useQuasar } from 'quasar';
import axios from 'axios';

export default {
  name: "ResetPassword",
  setup() {
    const router = useRouter();
    const $q = useQuasar();
    const email = ref('');
    const newPassword = ref('');
    const confirmPassword = ref('');
    const showPassword = ref(false);
    const showConfirmPassword = ref(false);
    const token = ref('');

    const passwordRules = [
      val => val && val.length >= 8 || 'Password must be at least 8 characters long',
      val => /[A-Z]/.test(val) || 'Password must contain at least one capital letter',
      val => /[0-9]/.test(val) || 'Password must contain at least one number',
      val => /[\W_]/.test(val) || 'Password must contain at least one special character',
    ];

    const confirmPasswordRules = [
      val => val === newPassword.value || 'Passwords do not match'
    ];

    onMounted(() => {
      const route = useRoute();
      token.value = route.query.token;
      email.value = decodeURIComponent(route.query.email);

      console.log('Token from URL:', token.value, 'Email from URL:', email.value);

      if (!token.value || !email.value) {
        console.warn("No token or email provided, redirecting to home.");
        router.push('/');
      } else {
      }
    });

    const resetPassword = async () => {
      try {
        const emailCheckResponse = await axios.get('http://16.171.224.57:80/api/emails');

        if (emailCheckResponse.data.includes(email.value)) {
          const isPasswordValid = passwordRules.every(rule => rule(newPassword.value) === true);
          const isConfirmPasswordMatching = newPassword.value === confirmPassword.value;

          if (isPasswordValid && isConfirmPasswordMatching) {
            const payload = {
              email: email.value,
              password: newPassword.value,
              token: token.value,
            };

            const updateResponse = await axios.post('http://16.171.224.57:80/api/updatePassword', payload);

            if (updateResponse.data.message === 'Password updated successfully') {
              $q.notify({
                color: 'green-4',
                textColor: 'white',
                icon: 'cloud_done',
                message: 'Password changed successfully'
              });
              router.push('/');
            } else {
              $q.notify({
                color: 'red-5',
                textColor: 'white',
                icon: 'warning',
                message: 'Failed to update password'
              });
            }
          } else {
            $q.notify({
              color: 'red-5',
              textColor: 'white',
              icon: 'warning',
              message: 'Passwords do not match or do not meet the requirements'
            });
          }
        } else {
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'warning',
            message: 'Email is not registered'
          });
        }
      } catch (error) {
        console.error('Error resetting password:', error);
        $q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'warning',
          message: 'Error resetting password'
        });
      }
    };


    const togglePassword = () => {
      showPassword.value = !showPassword.value;
    };

    const toggleConfirmPassword = () => {
      showConfirmPassword.value = !showConfirmPassword.value;
    };

    return {
      email,
      token,
      newPassword,
      confirmPassword,
      showPassword,
      showConfirmPassword,
      passwordRules,
      confirmPasswordRules,
      resetPassword,
      togglePassword,
      toggleConfirmPassword
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

