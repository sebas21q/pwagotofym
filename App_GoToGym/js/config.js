// js/config.js

const isProd = window.location.hostname.includes("netlify.app");

export const API_URL = isProd
  ? "https://pwagotofym.onrender.com/api"  // 👈 tu backend Django en Render
  : "http://127.0.0.1:8000/api";           // backend local en tu PC
