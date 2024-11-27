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
                  val => val && val.length > 0 || 'Name must include characters',
                  val => /^[A-Z]/.test(val) || 'First name must start with a capital'
                ]"
              />
              <q-input
                  filled
                  v-model="lastName"
                  label="Last Name *"
                  lazy-rules
                  :rules="[
                  val => val && val.length > 0 || 'Name must include characters',
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
                    val => /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/.test(val) || 'Invalid email format'
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
                <router-link to="/EmailVerification" class="forgot-password-link">Forgot your password?</router-link>
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
