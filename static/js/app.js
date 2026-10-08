document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".alert").forEach(el => {
    setTimeout(() => {
      if (el && window.bootstrap) bootstrap.Alert.getOrCreateInstance(el).close();
    }, 4500);
  });
});
