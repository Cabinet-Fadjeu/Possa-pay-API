const pwShowHide = document.querySelectorAll(".password_icon");

pwShowHide.forEach((icon) => {
  icon.addEventListener("click", () => {
    let getPwInput = icon.parentElement.querySelector("input");
    if (getPwInput.type === "password") {
      getPwInput.type = "text";
      icon.classList.replace("uil-eye-slash", "uil-eye");
    } else {
      getPwInput.type = "password";
      icon.classList.replace("uil-eye", "uil-eye-slash");
    }
  });
});

const mode = document.querySelector(".mode");
const icon = document.querySelector(".fa-moon");
const logo = document.querySelector(".logo-silhouette");

mode.addEventListener("click", function () {
  document.body.classList.toggle("dark-mode");

  if (document.body.classList.contains("dark-mode")) {
    icon.classList.remove("fa-moon");
    icon.classList.add("fa-sun");
    logo.classList.add("logo-dark");
  } else {
    icon.classList.remove("fa-sun");
    icon.classList.add("fa-moon");
    logo.classList.remove("logo-dark");
  }
});

document.getElementById("selection").addEventListener("change", function () {
  // Cacher tous les champs dynamiques
  document.querySelectorAll(".hidden").forEach(function (element) {
    element.style.display = "none";
  });

  // Afficher les champs correspondant à l'option sélectionnée
  const selectedValue = this.value;
  if (selectedValue) {
    const fields = document.getElementById(selectedValue + "Fields");
    if (fields) {
      fields.style.display = "block";
    }
  }
});

// Assurance 2% script

// const baseAmountInput = document.getElementById("baseAmount");
// const insuranceOption = document.getElementById("receiver_type");
// const totalAmountDisplay = document.getElementById("totalAmount");

// function calculateTotal() {
//   const baseAmount = parseFloat(baseAmountInput.value) || 0;
//   const wantsInsurance = insuranceOption.value === "entreprise";
//   const insuranceFee = wantsInsurance ? baseAmount * 0.02 : 0;
//   const totalAmount = baseAmount + insuranceFee;
//   totalAmountDisplay.textContent = totalAmount.toFixed(2);
// }

baseAmountInput.addEventListener("input", calculateTotal);
insuranceOption.addEventListener("change", calculateTotal);

// dropdown script
const dropdowns = document.querySelectorAll(".dropdown");

// Loop through all dropdown elements
dropdowns.forEach((dropdown) => {
  //Get inner elements from each dropdown
  const select = dropdown.querySelector(".select");
  const caret = dropdown.querySelector(".caret");
  const menu = dropdown.querySelector(".menu");
  const options = dropdown.querySelector(".menu li");
  const selected = dropdown.querySelector(".selected");

  // Add a click event to the select element
  select.addEventListener("click", () => {
    // Add the clicked select styles to the select element
    select.classList.toggle("select-clicked");
    // Add the rotate styles to the caret element
    caret.classList.toggle("caret-rotate");
    // Add the open styles to the menu element
    menu.classList.toggle("menu-open");
  });

  // Loop through all option elements
  options.forEach((option) => {
    // Add a click event to the option element
    option.addEventListener("click", () => {
      // Change selected inner text to clicked option inner text
      selected.innerText = option.innerText;
      // Add the clicked select styles to the select element
      select.classList.remove("select-clicked");
      // Add the rotate styles to the caret element
      caret.classList.remove("caret-rotate");
      // Add the open styles to the menu element
      menu.classList.remove("menu-open");
      // Remove active class from all option elements
      options.forEach((option) => {
        option.classList.remove("active");
      });
      // Add active class to clicked option element
      option.classList.add("active");
    });
  });
});
