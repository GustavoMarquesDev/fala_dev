let message = document.querySelector(".alert");

if (message) {
  setTimeout(() => {
    message.remove();
  }, 3000);
}
