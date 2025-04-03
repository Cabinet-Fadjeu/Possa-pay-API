document.addEventListener("DOMContentLoaded", function () {
  console.log("hello :");
  // ✅ Vérifier que l'élément JSON existe avant d'analyser
  const servicesDataElement = document.getElementById("services-data");
  if (!servicesDataElement) {
    console.error("Erreur : Élément 'services-data' introuvable.");
    return;
  }

  // ✅ Convertir le JSON en objet JavaScript
  let services;
  try {
    services = JSON.parse(servicesDataElement.textContent);
  } catch (error) {
    console.error("Erreur lors de l'analyse JSON :", error);
    return;
  }

  console.log("Services chargés :", services);

  function loadService(serviceId) {
    const service = services.find((s) => s.id === serviceId);
    if (service) {
      document.getElementById("service-name").textContent = service.name;
      document.getElementById(
        "service-balance"
      ).textContent = `$${service.balance.toFixed(2)}`;
      document.getElementById("apiKey").value = service.apiKey;

      // ✅ Charger les transactions
      const transactionsContainer = document.getElementById(
        "service-transactions"
      );
      transactionsContainer.innerHTML = "";

      if (service.transactions.length > 0) {
        service.transactions.forEach((tx) => {
          const li = document.createElement("li");
          li.innerHTML = `${tx.desc} <span class="${
            tx.amount.startsWith("+") ? "credit" : "debit"
          }">${tx.amount}</span>`;
          transactionsContainer.appendChild(li);
        });
      } else {
        transactionsContainer.innerHTML =
          "<li>Aucune transaction disponible</li>";
      }
    } else {
      console.warn("Service non trouvé :", serviceId);
    }
  }

  // ✅ Ajouter un écouteur sur chaque élément de la liste des services
  document.querySelectorAll("#service-list li").forEach((item) => {
    item.addEventListener("click", function () {
      loadService(this.dataset.id);
    });
  });
});

// document.addEventListener("DOMContentLoaded", function () {
//   // Récupérer les données JSON du template
//   const services = JSON.parse(
//     document.getElementById("services-data").textContent
//   );
//   console.log(services);

//   function loadService(serviceId) {
//     const service = services.find((s) => s.id == serviceId);
//     if (service) {
//       document.getElementById("service-name").textContent = service.name;
//       document.getElementById(
//         "service-balance"
//       ).textContent = `$${service.balance}`;
//       document.getElementById("apiKey").value = service.apiKey;

//       // Charger les transactions
//       const transactionsContainer = document.getElementById(
//         "service-transactions"
//       );
//       transactionsContainer.innerHTML = "";
//       service.transactions.forEach((tx) => {
//         const li = document.createElement("li");
//         li.innerHTML = `${tx.desc} <span class="${
//           tx.amount.startsWith("+") ? "credit" : "debit"
//         }">${tx.amount}</span>`;
//         transactionsContainer.appendChild(li);
//       });
//     }
//   }

//   // Ajouter un écouteur sur chaque élément de la liste des services
//   document.querySelectorAll("#service-list li").forEach((item) => {
//     item.addEventListener("click", function () {
//       loadService(this.dataset.id);
//     });
//   });
// });
