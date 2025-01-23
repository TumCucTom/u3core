//Change to LoginRegister.vue
<template>
  <div class="registration-login-container">
    <div class="row q-pa-lg" style="width: 90%;">
      <div class="col q-pa-sm">
        <!-- Register -->
        <q-card>
          <q-card-section :class="{ 'bg-dark': $q.dark.isActive }">
            <q-form @submit="onSubmit" @login="onLogin" class="q-gutter-md">
              <q-toolbar class="text-center">
                <q-toolbar-title style="font-size: 28px;"><strong>REGISTER</strong></q-toolbar-title>
              </q-toolbar>
              <!-- Registration Form Inputs -->
              <!-- Add validation to all of these fields -->
              <q-input
                filled
                v-model="firstName"
                label="First Name *"
                lazy-rules
                :rules="[
                  val => val && val.length > 0 || 'Please type something',
                  val => /^[A-Z]/.test(val) || 'First name must start with a capital letter'
                ]"
              />
              <q-input
                filled
                v-model="lastName"
                label="Last Name *"
                lazy-rules
                :rules="[
                  val => val && val.length > 0 || 'Please type something',
                  val => /^[A-Z]/.test(val) || 'Last name must start with a capital letter'
                ]"
              />
              <q-input
                filled
                v-model="email"
                label="Email Address *"
                suffix=""
                :rules="[
                    val => val && val.length > 0 || 'Please enter an email address',
                    val => /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/g.test(val) || 'Invalid email format'
                  ]"
              >
              </q-input>

              <q-input
                filled
                v-model="password"
                label="Password *"
                type="password"
                lazy-rules
                :rules="[
                    val => val && val.length >= 8 || 'Password must be at least 8 characters long',
                    val => /[A-Z]/.test(val) || 'Password must contain at least one capital letter',
                    val => /[0-9]/.test(val) || 'Password must contain at least one number',
                    val => /[\W_]/.test(val) || 'Password must contain at least one special character'
                  ]"
              />

              <div class="password-requirements">
                Password must be at least 8 characters long and include at least one capital letter, one number, and one special character.
              </div>

              <q-input
                filled
                v-model="confirmPassword"
                label="Confirm Password *"
                type="password"
                lazy-rules
                :rules="[val => val && val.length > 0 || 'Please type something', val => val == password || 'Passwords do not match']"
              />

              <div class="q-mt-md text-center">
                <q-btn class="gradient-button" label="CREATE AN ACCOUNT" size="18px" type="submit" rounded push />
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </div>

      <q-separator dark inset/>
      <q-separator dark inset/>

      <div class="col q-pa-sm" style="margin-top: 30vh; transform: translateY(-25%);">
        <!-- Login -->
        <q-card>
          <q-card-section :class="{ 'bg-dark': $q.dark.isActive }">
            <q-form @submit="onLogin">
              <q-toolbar class="text-center">
                <q-toolbar-title style="font-size: 28px;"><strong>LOGIN</strong></q-toolbar-title>
              </q-toolbar>

              <!-- Login Form Inputs -->
              <q-input
                filled
                v-model="emailLogin"
                label="Email Address *"
                suffix=""
                :rules="[
                      val => val && val.length > 0 || 'Please enter an email address',
                      val => /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/g.test(val) || 'Invalid email format'
                    ]"
              >
              </q-input>
              <q-input
                filled
                v-model="passwordLogin"
                label="Password *"
                type="password"
                lazy-rules
                :rules="[val => val && val.length > 0 || 'Please type something']"
              />

              <div class="text-center">
                <router-link to="/SetupResetPassword" class="forgot-password-link">Forgot your password?</router-link>
              </div>
              <div class="q-mt-md text-center">
                <q-btn class="gradient-button" label="SIGN IN" size="18px" type="login" rounded push />
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useQuasar } from 'quasar';
import axios from 'axios';
import { useRouter } from 'vue-router';
import bcrypt from 'bcryptjs';
import {colors} from 'quasar';

export default {
  name: 'RegisterPage',
  setup() {
    const firstName = ref('');
    const lastName = ref('');
    const email = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const emailLogin = ref('');
    const passwordLogin = ref('');
    const allEmails = ref([]);
    const $q = useQuasar();
    const router = useRouter(); // Get the router instance
    const {getPaletteColor} = colors
    console.log(getPaletteColor('text-brand'))

    /*
    const passwordsMatch = () => {
      return password.value === confirmPassword.value;
    };
    */


    const onSubmit = () => {

      axios.get('http://127.0.0.1:3002/api/emails')
        .then(response => {
          allEmails.value = response.data;
          if (allEmails.value.includes(email.value)) {
            console.error('Email is already registered');
            $q.notify({
              color: 'red-5',
              textColor: 'white',
              icon: 'warning',
              message: 'Email is already registered',
            });
          } else {
            addToCustomer();
            $q.notify({
              color: 'green-4',
              textColor: 'white',
              icon: 'cloud_done',
              message: 'Email registered',
            });
          }
        })
        .catch(error => {
          console.error('Error fetching emails:', error);
        });
    };

    const addToCustomer = () => {
      const requestData = {
        items: [firstName.value, lastName.value, email.value, password.value],
      };

      axios.post('http://127.0.0.1:3002/api/addToCustomer', requestData)
        .then(response => {
          console.log(response.data);
        })
        .catch(error => {
          console.error('Error adding item:', error);
        });
    };

    const onLogin = async () => {
      const emailSend = String(emailLogin.value);

      try {
        const response = await axios.get('http://127.0.0.1:3002/api/login', { params: { emailVar: emailSend } });
        const fetchedHashedPassword = response.data;

        const result = await bcrypt.compare(passwordLogin.value, fetchedHashedPassword);

        if (result) {
          // Passwords match, allow the user to log in
          $q.notify({
            color: 'green-4',
            textColor: 'white',
            icon: 'cloud_done',
            message: 'Successfully logged in',
          });

          // Redirect user
          router.push('/OTPVerification');
        } else {
          // Passwords don't match, notify the user
          $q.notify({
            color: 'red-5',
            textColor: 'white',
            icon: 'warning',
            message: 'Invalid username/password',
          });
        }
      } catch (error) {
        console.error('Error during login:', error);
        // Handle any other errors here
        $q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'warning',
          message: 'Email does not exist. Please register an account.',
        });
      }
    };

    return {
      firstName,
      lastName,
      email,
      password,
      confirmPassword,
      emailLogin,
      passwordLogin,
      //passwordsMatch,
      onSubmit,
      onLogin,
    };
  },
};
</script>

<style scoped>

.q-card {
  border: 1px solid #f04c26; /* Keeps the existing border */
  background: linear-gradient(to bottom,
  rgba(245, 245, 245, 1) 0%,
  rgba(255, 255, 255, 0.95) 50%,
  rgba(245, 245, 245, 1) 100%) !important;
  box-shadow: 0 8px 10px rgba(0, 0, 0, 0.15); /* More pronounced shadow for depth */
}

:deep(.gradient-button) {
  background: linear-gradient(to right, #0e004d, #064e81) !important; /* Adjusted for blue gradient */
  color: white !important;
}

:deep(.gradient-button:hover) {
  background: linear-gradient(to right, #064e81, #0e004d) !important; /* Hover effect reverses gradient */
}

.registration-login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 70vh; /* height of container */
  margin-bottom: 20px;
  padding-left: 35px; /* Adjust the size as needed */
  padding-right: 35px; /* Adjust the size as needed */

}

.password-requirements {
  font-size: 14px;
  color: #666;
  margin-top: 1px;
  margin-bottom: 10px; /* Adjust spacing as needed */
}

</style>
