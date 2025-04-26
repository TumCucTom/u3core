// src/tests/setup.ts

import { beforeEach } from 'vitest'
import { config } from '@vue/test-utils'

beforeEach(() => {
  config.global.stubs = {
    'q-btn': true,
    'q-btn-group': true,
    'q-card': true,
    'q-card-section': true,
    'q-card-actions': true,
    'q-table': true,
    'q-toolbar': true,
    'q-toolbar-title': true,
    'q-icon': true,
    'q-input': true,
    'q-select': true,
    'q-dialog': true,
    'q-page': true,
    'router-link': true, // if needed
    'router-view': true, // if needed
  }
})
