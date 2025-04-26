import { beforeEach } from 'vitest';
import { Quasar, Dialog, Notify } from 'quasar';
import { config } from '@vue/test-utils';

beforeEach(() => {
  config.global.plugins = [Quasar, Dialog, Notify];
});
