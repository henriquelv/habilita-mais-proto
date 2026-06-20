document.addEventListener("DOMContentLoaded", () => {
  const paymentModal = document.getElementById("paymentModal");
  if (!paymentModal) return;

  paymentModal.addEventListener("show.bs.modal", (event) => {
    const button = event.relatedTarget;
    if (!button) return;

    const paymentId = button.getAttribute("data-payment-id");
    const title = button.getAttribute("data-payment-title");
    const amount = button.getAttribute("data-payment-amount");

    const idInput = paymentModal.querySelector("#paymentId");
    const description = paymentModal.querySelector("#paymentDescription");

    if (idInput) idInput.value = paymentId || "";
    if (description) description.textContent = `${title || "Pagamento"} - R$ ${amount || "0,00"}`;
  });
});
