// Función global accesible desde el atributo onclick del botón de eliminar
async function deleteRestaurant(restaurantId) {
  if (!restaurantId) return;

  if (confirm("¿Estás seguro de que deseas eliminar este restaurante?")) {
    try {
      const response = await fetch(`/api/v1/restaurants/${restaurantId}`, {
        method: "DELETE"
      });

      if (response.ok || response.status === 204) {
        // Redirige al inicio forzando actualización sin caché
        window.location.href = "/?refresh=" + Date.now();
      } else {
        alert("Error al eliminar el restaurante de la base de datos.");
      }
    } catch (err) {
      alert("Error de conexión al intentar eliminar.");
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  // Manejo del formulario (Crear y Editar)
  const form = document.getElementById("restaurant-form");
  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const restaurantId = form.dataset.id;
      const formData = Object.fromEntries(new FormData(form));
      formData.price = Number(formData.price);

      const isEdit = Boolean(restaurantId);
      const url = isEdit ? `/api/v1/restaurants/${restaurantId}` : "/api/v1/restaurants";
      const method = isEdit ? "PATCH" : "POST";

      const message = document.getElementById("message");
      if (message) {
        message.style.color = "#3b82f6";
        message.textContent = "Guardando cambios...";
      }

      try {
        const response = await fetch(url, {
          method: method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData)
        });

        if (response.ok) {
          if (message) {
            message.style.color = "#4ade80";
            message.textContent = isEdit ? "¡Restaurante actualizado con éxito!" : "¡Restaurante creado con éxito!";
          }
          
          setTimeout(() => {
            window.location.href = "/?refresh=" + Date.now();
          }, 500);
        } else {
          const error = await response.json();
          if (message) {
            message.style.color = "#f87171";
            message.textContent = error.detail || "Error al guardar el restaurante.";
          }
        }
      } catch (err) {
        if (message) {
          message.style.color = "#f87171";
          message.textContent = "Error de conexión con el servidor.";
        }
      }
    });
  }
});