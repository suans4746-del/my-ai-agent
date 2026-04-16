/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        apple: {
          bg: '#1D1D1F',
          card: '#2C2C2E',
          blue: '#007AFF',
          green: '#34C759',
          red: '#FF3B30',
          gray: '#8E8E93',
        }
      },
      borderRadius: {
        'xl': '12px',
        '2xl': '16px',
      },
      boxShadow: {
        'soft': '0 4px 24px rgba(0,0,0,0.25)',
      }
    },
  },
  plugins: [],
}
