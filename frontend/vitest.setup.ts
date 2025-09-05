// frontend/vitest.setup.ts
import { config } from '@vue/test-utils';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import { vi } from 'vitest';

// --- Create and Export Vuetify Instance ---
export const vuetify = createVuetify({
  components,
  directives,
});

config.global.plugins = [vuetify];

// --- Mock Missing Browser APIs for JSDOM ---
const IntersectionObserverMock = vi.fn((callback) => {
  const instance = {
    disconnect: vi.fn(),
    observe: vi.fn(() => callback([{ isIntersecting: true }], instance)),
    takeRecords: vi.fn(),
    unobserve: vi.fn(),
  };
  return instance;
});
vi.stubGlobal('IntersectionObserver', IntersectionObserverMock);

const ResizeObserverMock = vi.fn(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));
vi.stubGlobal('ResizeObserver', ResizeObserverMock);

// Enhanced matchMedia mock with logging to verify it's applied
const matchMediaMock = vi.fn().mockImplementation((query) => {
  console.log('matchMedia called with query:', query); // Debug log
  return {
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  };
});
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: matchMediaMock,
});

// Verify matchMedia is defined
if (!window.matchMedia) {
  console.error('matchMedia mock failed to apply');
}

// Mock visualViewport
Object.defineProperty(window, 'visualViewport', {
  writable: true,
  configurable: true,
  value: {
    width: 1920,
    height: 1080,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  },
});

