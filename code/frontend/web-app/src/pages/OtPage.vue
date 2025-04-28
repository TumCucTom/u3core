<template>
  <q-page class="q-pa-lg flex flex-center full-height bg-light">
    <div class="verification-box column items-center q-px-xl q-py-lg shadow-2 rounded-borders bg-white">

      <q-avatar size="80px" class="q-mb-md bg-light-pink text-pink">
        <q-icon name="email" size="40px" />
      </q-avatar>

      <h2 class="text-bold text-center">Check your email</h2>
      <p class="text-subtitle1 text-center">
        We sent a verification link to <span class="text-bold" id="retrievedEmail">{{ email }}</span>
      </p>

      <p class="text-caption text-center q-mt-sm" @click="resendEmail">
        Didn’t receive the email?
        <span class="text-pink cursor-pointer"><b>Click to resend</b></span>
      </p>

      <q-btn flat class="q-mt-md" label="Back to log in" icon="west" color="dark" @click="backtologin" />
    </div>
  </q-page>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import axios from 'axios'

export default {
  name: "CodeVerification",
  setup() {
    const router = useRouter()
    const $q = useQuasar()
    const email = ref('')

    const backtologin = () => {
      router.push('/')
    }

    const sendEmail = async () => {
      try {
        const retrievedEmail = sessionStorage.getItem("emailTransfer")
        email.value = retrievedEmail
        await axios.post('http://16.171.224.57:80/api/sendVerifyEmail', { email: email.value })
      } catch (error) {
        console.error("Error fetching alerts:", error)
      }
    }

    const resendEmail = async () => {
      try {
        await axios.post('http://16.171.224.57:80/api/sendVerifyEmail', { email: email.value })
        $q.notify({
          color: 'green-4',
          textColor: 'white',
          icon: 'email',
          message: 'Verification email resent successfully. Please check your inbox.'
        })
      } catch (error) {
        console.error('Error resending verification email:', error)
        $q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'error',
          message: 'Error resending verification email'
        })
      }
    }

    onMounted(sendEmail)

    return {
      email,
      resendEmail,
      backtologin,
    }
  }
}
</script>
