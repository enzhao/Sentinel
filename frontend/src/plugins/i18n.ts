import { createI18n } from 'vue-i18n';
import messages from '@/locales/en.json';

const i18n = createI18n({
  legacy: false, // Use Composition API
  locale: 'en', // Set default locale
  fallbackLocale: 'en', // Fallback locale
  messages: {
    en: messages,
  },
});

export default i18n;
