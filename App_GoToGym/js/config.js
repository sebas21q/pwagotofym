// js/config.js

const isProd = window.location.hostname.includes("netlify.app");

export const API_URL = isProd
  ? "https://693b248a7fd925195cb9d0e8--moonlit-axolotl-97627d.netlify.app/" // backend en la nube
  : "http://127.0.0.1:8000/api";                    // backend local para desarrollo
