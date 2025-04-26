// test-setup.ts
import { beforeAll } from 'vitest'
import { installQuasarPlugin } from '@quasar/quasar-app-extension-testing-unit-vitest'

// Mocks are auto-loaded now, you just need to import the file
import './setupMocks'

// Install Quasar plugin
beforeAll(() => {
  installQuasarPlugin()
})
