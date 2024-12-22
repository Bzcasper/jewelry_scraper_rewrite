import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
    en: {
        translation: {
            'Welcome': 'Welcome to Jewelry Scraper',
            'Login': 'Login',
            'Register': 'Register',
            // Add more translations
        }
    },
    es: {
        translation: {
            'Welcome': 'Bienvenido a Jewelry Scraper',
            'Login': 'Iniciar Sesión',
            'Register': 'Registrarse',
            // Add more translations
        }
    },
    // Add more languages
};

i18n
  .use(initReactI18next)
  .init({
      resources,
      lng: 'en',
      interpolation: {
          escapeValue: false
      }
  });

export default i18n;
