let searchForm = document.querySelector(".search-form");

document.querySelector("#search-btn").onclick = () => {
  searchForm.classList.toggle("active");
  shoppingCart.classList.remove("active");
  // loginForm.classList.remove('active');
  navbar.classList.remove("active");
};

let shoppingCart = document.querySelector(".shopping-cart");

document.querySelector("#cart-btn").onclick = () => {
  shoppingCart.classList.toggle("active");
  searchForm.classList.remove("active");
  // loginForm.classList.remove('active');
  navbar.classList.remove("active");
};

// let loginForm = document.querySelector('.login-form');

// document.querySelector('#login-btn').onclick = () =>{
//     loginForm.classList.toggle('active');
//     searchForm.classList.remove('active');
//     shoppingCart.classList.remove('active');
//     navbar.classList.remove('active');

// }

// let createAccountLink = document.querySelector('#create-account-link');
// let loginLink = document.querySelector('#login-link');
// let createAccountForm = document.querySelector('#create-account-form');

// Clic sur le lien pour créer un compte
// createAccountLink.onclick = () => {
//   createAccountForm.classList.toggle('active');
//   loginForm.classList.remove('active');
//   searchForm.classList.remove('active');
//   shoppingCart.classList.remove('active');
//   navbar.classList.remove('active');
// }

// Clic sur le lien pour se connecter
// loginLink.onclick = () => {
//   loginForm.classList.toggle('active');
//   createAccountForm.classList.remove('active');
//   searchForm.classList.remove('active');
//   shoppingCart.classList.remove('active');
//   navbar.classList.remove('active');
// }

let navbar = document.querySelector(".navbar");

document.querySelector("#menu-btn").onclick = () => {
  navbar.classList.toggle("active");
  searchForm.classList.remove("active");
  shoppingCart.classList.remove("active");
  // loginForm.classList.remove('active');
  // createAccountForm.classList.remove('active');
};

window.onscroll = () => {
  searchForm.classList.remove("active");
  shoppingCart.classList.remove("active");
  // loginForm.classList.remove('active');
  navbar.classList.remove("active");
  // createAccountForm.classList.remove('active');
};
// --------------------paiement monetbil-----------------------
// const paiementForm = document.querySelector("#paiementForm");

//     paiementForm.addEventListener("submit", async (event) => {
//         event.preventDefault();

//         // Get email and password values from the form
//         const service = '{{service}}'
//         const amt = document.querySelector("#amount").value;
//         const phone = document.querySelector("#phone").value;
//         const order = document.querySelector("#order").value;
//         // console.log(service)
//         // console.log(phone)
//         // console.log(order)

//         try {
//             // Make an Axios POST request to your API endpoint
//             //
//             // https://api.monetbil.com/widget/v2.1/NViQCYoKszWPeG4ZUEYnGV02AiLYBa2f
//             const response = await axios.post("https://api.monetbil.com/payment/v1/placePayment", {
//                 amount: amt,
//                 phonenumber : phone,
//                 service : service,
//                 item_ref : order,
//                 notify_url : 'https://www.remethesauce.com/mobile-payment/'
//                 // notify_url : 'https://5691-154-72-167-46.ngrok-free.app/mobile-payment/'
//             });

//             // Handle the response (e.g., show a success message)
//             // console.log("Login successful:", response.data);
//             // console.log(response.data.message)
//             if (response.data.message=='payment pending') {
//                 alert('Veillez confirmer le paiement sur votre telephone')
//                 // letat de la page
//                 window.location.href = "{% url 'core:mobile-payment' %}";
//             }

//         } catch (error) {
//             alert('Format du numeros de telephone est incorect 237XXXXXXXXX')
//             console.log(error)
//             // window.location.href = "{% url 'core:payment-failed' %}"
//         }
//     });
//--------------------fin monet bill-----------------------------------------
//--------------------paiement stripe---------------------------------
// var stripe = Stripe('{{ stripe_publishable_key }}');
// var elements = stripe.elements();
// var cardElement = elements.create('card');
// cardElement.mount('#card-element');

// var form = document.getElementById('payment-form');
// var errorElement = document.getElementById('error-message');

// form.addEventListener('submit', function(event) {
//     event.preventDefault();
//     stripe.confirmCardPayment('{{ client_secret }}', {
//         payment_method: {
//             card: cardElement,
//         }
//     }).then(function(result) {
//         if (result.error) {
//             errorElement.textContent = result.error.message;
//         } else {
//             window.location.href = "{% url 'core:payment-completed' %}";
//         }
//     });
// });

//-----------------------fin stripe----------------------------------

// var swiper = new Swiper(".product-slider", {
//     loop:true,
//     spaceBetween: 20,
//     autoplay: {
//         delay: 7500,
//         disableOnInteraction: false,
//     },
//     centeredSlides: true,
//     breakpoints: {
//       0: {
//         slidesPerView: 1,
//       },
//       768: {
//         slidesPerView: 2,
//       },
//       1020: {
//         slidesPerView: 3,
//       },
//     },
// });

// var swiper = new Swiper(".review-slider", {
//     loop:true,
//     spaceBetween: 20,
//     autoplay: {
//         delay: 7500,
//         disableOnInteraction: false,
//     },
//     centeredSlides: true,
//     breakpoints: {
//       0: {
//         slidesPerView: 1,
//       },
//       768: {
//         slidesPerView: 2,
//       },
//       1020: {
//         slidesPerView: 3,
//       },
//     },
// });

// Sélectionnez tous les éléments d'alerte
var alerts = document.querySelectorAll(".alert");

// Parcourez chaque élément d'alerte
alerts.forEach(function (alert) {
  // Fermez l'élément d'alerte après 3 secondes
  setTimeout(function () {
    alert.style.display = "none"; // Masquer l'élément d'alerte
  }, 3000);
});

// checout page hide elements
function selectPayment(paymentMethod) {
  document.querySelectorAll(".payment-info").forEach(function (el) {
    el.classList.add("hidden");
  });

  document.getElementById(paymentMethod + "-info").classList.remove("hidden");

  document.querySelectorAll(".payment-btn").forEach(function (el) {
    el.classList.remove("red");
  });
  document.getElementById(paymentMethod + "-btn").classList.add("red");
}
