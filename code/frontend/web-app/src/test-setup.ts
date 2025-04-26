import { beforeAll } from 'vitest'
import { installQuasarPlugin } from '@quasar/quasar-app-extension-testing-unit-vitest'
import { setupMocks } from './setupMocks'

// Important: call the function inside a beforeAll or immediately
await setupMocks()

// Install Quasar plugin
beforeAll(() => {
  installQuasarPlugin()
})
