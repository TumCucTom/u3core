<template>
  <q-page style="height: 100vh;">
    <div class="q-pa-lg row items-stretch full-height">
      <!-- left column -->
      <div class="col-12 col-md-6 bg-light q-px-lg q-py-xl">
        <div class="text-left">
          <q-img src="../assets/u3logo1.png" alt="Digital U3" style="width: 150px;" />
          <div class="q-mt-xl text-center">
            <q-rating value="5" readonly size="lg" color="amber" />
            <p class="q-my-md text-h5">
              {{ isLogin
                ? "We've been using Untitled to kick start every new project and can't imagine working without it."
                : "U3Core's safety compliance features helped us monitor workplace conditions more efficiently. We've not only reduced risks but also met the regulatory requirements with ease.'"
              }}
            </p>
            <q-avatar size="80px">
              <q-img
                :src="isLogin ? obamaImage : anotherUserImage"
                alt="User Image"
              />
            </q-avatar>
            <p class="q-mt-sm text-bold">{{ isLogin ? 'Pippa Wilkinson' : 'Lori Bryson' }}</p>
            <p class="text-caption">
              {{ isLogin ? 'Head of Design, Layers' : 'Product Designer, Sisyphus' }}
            </p>
          </div>
        </div>
      </div>

      <!-- right column-->
      <div class="col-12 col-md-6">
        <div class="q-px-lg q-py-xl">
          <!-- title -->
          <h2 class="text-bold">{{ isLogin ? 'Welcome back' : 'Sign up' }}</h2>
          <p>{{ isLogin ? 'Welcome back! Please enter your details.' : 'Start your 30-day free trial.' }}</p>

          <!-- form -->
          <q-form>
            <q-input
              v-if="!isLogin"
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
              v-if="!isLogin"
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
              v-if="!isLogin"
              filled
              v-model="confirmPassword"
              label="Confirm Password *"
              type="password"
              lazy-rules
              :rules="[val => val && val.length > 0 || 'Please type something', val => val == password || 'Passwords do not match']"
            />


            <q-btn
              :label="isLogin ? 'Sign in' : 'Continue'"
              color="primary"
              class="full-width q-my-md"
              @click="proceedToOtp"
            />


            <div class="text-center q-mt-md">
              <q-checkbox v-if="isLogin" label="Remember for 30 days" />
              <q-btn v-if="isLogin" flat label="Forgot password" color="primary" class="q-my-md" />

              <span v-if="isLogin">Don't have an account?</span>
              <span v-else>Already have an account?</span>
              <q-btn
                flat
                :label="isLogin ? 'Sign up' : 'Log in'"
                color="primary"
                @click="toggleMode"
              />
            </div>
          </q-form>
        </div>
      </div>
    </div>
  </q-page>
</template>


<script>
  import { ref } from 'vue';
  import { useQuasar } from 'quasar';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import bcrypt from 'bcryptjs';
  import {colors} from 'quasar';
  import obamaImage from '@/assets/obama.jpg';
  import anotherUserImage from '@/assets/Lori.png';
  
  
  export default {
    data() {
      return {
        isLogin: false, // sees if page is in login or register mode
        obamaImage,
        anotherUserImage,
      };
    },
    methods: {
      toggleMode() {
        this.isLogin = !this.isLogin; // switches between login and register
      },
      proceedToOtp() {
      this.$router.push("/otp");
    }
    },
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

  axios.get('http://16.171.224.57:3002/api/emails')
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


  axios.post('http://16.171.224.57:3002/api/addToCustomer', requestData)
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
  const response = await axios.get('http://16.171.224.57:3002/api/login', { params: { emailVar: emailSend } });
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

.move-left {
  position-try: relative;
  left: -2000px;
}

.bg-light {
  background-color: #f9fafb;
}
.full-height {
  height: 100vh;
}

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
