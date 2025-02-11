// change and icon (dark mode)
const mode = document.querySelector('.mode');
const icon = document.querySelector('.fa-moon');
const logo = document.querySelector('.logo-silhouette');

mode.addEventListener('click', function(){
    document.body.classList.toggle('dark-mode');

    if(document.body.classList.contains('dark-mode')) {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
        logo.classList.add('logo-dark')
    }
    else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
        logo.classList.remove('logo-dark')
    }
});

// change toggle btn navbar
const bars = document.querySelector('.toggle-btn');
const navbar = document.querySelector('header .navbar');

bars.addEventListener('click', function() {
   if(bars.classList.contains('fa-bars')) {
        bars.classList.remove('fa-bars');
        bars.classList.add('fa-xmark');
        navbar.classList.add('slide')
   }
   else {
        bars.classList.remove('fa-xmark');
        bars.classList.add('fa-bars');
        navbar.classList.remove('slide')
   }
});

const dropdowns = document.querySelectorAll('.dropdown');

// Loop through all dropdown elements
dropdowns.forEach(dropdown => {
    //Get inner elements from each dropdown
    const select = dropdown.querySelector('.select');
    const caret = dropdown.querySelector('.caret');
    const menu = dropdown.querySelector('.menu');
    const options = dropdown.querySelector('.menu li');
    const selected = dropdown.querySelector('.selected');

    // Add a click event to the select element
    select.addEventListener('click', () => {
        // Add the clicked select styles to the select element
        select.classList.toggle('select-clicked');
        // Add the rotate styles to the caret element
        caret.classList.toggle('caret-rotate');
        // Add the open styles to the menu element
        menu.classList.toggle('menu-open');
    });

    // Loop through all option elements
    options.forEach(option => {
        // Add a click event to the option element
        option.addEventListener('click', () => {
            // Change selected inner text to clicked option inner text
            selected.innerText = option.innerText;
            // Add the clicked select styles to the select element
            select.classList.remove('select-clicked');
            // Add the rotate styles to the caret element
            caret.classList.remove('caret-rotate');
            // Add the open styles to the menu element
            menu.classList.remove('menu-open');
            // Remove active class from all option elements
            options.forEach(option => {
                option.classList.remove('active');
            });
            // Add active class to clicked option element
            option.classList.add('active');
        });
    });
});

document.getElementById('selection').addEventListener('change', function() {
    // Cacher tous les champs dynamiques
    document.querySelectorAll('.hidden').forEach(function(element) {
        element.style.display = 'none';
    });

    // Afficher les champs correspondant à l'option sélectionnée
    const selectedValue = this.value;
    if (selectedValue) {
        const fields = document.getElementById(selectedValue + 'Fields');
        if (fields) {
            fields.style.display = 'block';
        }
    }
});