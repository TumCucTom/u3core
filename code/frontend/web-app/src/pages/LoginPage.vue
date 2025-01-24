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
                : "Untitled has saved us thousands of hours of work. We’re able to spin up projects and features much faster."
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
          <!-- Title -->
          <h2 class="text-bold">{{ isLogin ? 'Welcome back' : 'Sign up' }}</h2>
          <p>{{ isLogin ? 'Welcome back! Please enter your details.' : 'Start your 30-day free trial.' }}</p>

          <!-- form -->
          <q-form>

            <q-input
              filled
              type="email"
              label="Email*"
              placeholder="Enter your email"
              class="q-my-md"
            />


            <q-input
              filled
              type="password"
              label="Password*"
              placeholder="Enter your password"
              class="q-my-md"
            >
              <template v-if="!isLogin" v-slot:hint>
                Must be at least 8 characters.
              </template>
            </q-input>


            <q-input
              v-if="!isLogin"
              filled
              type="password"
              label="Confirm Password*"
              placeholder="Confirm your password"
              class="q-my-md"
            />


            <q-btn
              :label="isLogin ? 'Sign in' : 'Continue'"
              color="primary"
              class="full-width q-my-md"
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

  export default {
    data() {
      return {
        isLogin: false, // sees if page is in login or register mode
      };
    },
    methods: {
      toggleMode() {
        this.isLogin = !this.isLogin; // switches between login and register
      },
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

<style>
.bg-light {
  background-color: #f9fafb;
}
.full-height {
  height: 100vh;
}
</style>
