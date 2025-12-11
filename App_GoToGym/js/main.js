async function registrarUsuario(username, email, password, plan = "Gratis") {
  try {
    const res = await fetch(API_URL + "register/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password, plan }),
    });

    const data = await res.json();

    if (res.ok) {
      showToast("✅ Usuario registrado: " + data.username);
      console.log("✅ Respuesta del backend:", data);
      setTimeout(() => {
        window.location.href = "indexInicioDeSesion.html";
      }, 1500);
    } else {
      console.error("❌ Error del backend:", data);
      showToast("❌ " + (data.error || "No se pudo registrar el usuario"), false);
    }
  } catch (err) {
    console.error("⚠ Error de conexión:", err);
    showToast("⚠ No se pudo conectar con el servidor", false);
  }
}
