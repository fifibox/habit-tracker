// JS for index.html page
// open the login form when user clicks on the login button
function openLoginForm() {
  const modal = document.getElementById("loginForm");
  modal.style.display = "flex";

  const form = modal.querySelector('.form-content');
  if (form) {
    form.style.animation = "none";           // reset animation
    void form.offsetHeight;                  // force reflow
    form.style.animation = "popupScale 0.3s ease-out forwards";  // reapply
  }
}

// close the login form
function closeLoginForm() { 
  const modal = document.getElementById("loginForm");
  modal.style.display = "none";
}

// open the signup form when user clicks on the signup button
function openSignupForm() {
  const modal = document.getElementById("signupForm");
  modal.style.display = "flex";
  const form = modal.querySelector('.form-content');
  form.style.animation = "none";           // remove animation
  form.offsetHeight;                       // trigger reflow
  form.style.animation = "popupScale 0.3s ease-out forwards";  // reapply animation
}
// close the signup form
function closeSignupForm() { 
  const modal = document.getElementById("signupForm");
  modal.style.display = "none";
}

document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  if (params.has("show_login")) {
    openLoginForm();
    // Clean up the URL
    window.history.replaceState({}, document.title, window.location.pathname);
  }
});

// TYPEWRITER EFFECT
var aText = [
  'We are what we repeatedly do. Excellence, then, is not an act, but a habit. — Aristotle'
];
var iSpeed = 100; // time delay of print out
var iIndex = 0; // start printing array at this position
var iArrLength = aText[0].length; // the length of the text array
var iScrollAt = 20; // start scrolling up at this many lines

var iTextPos = 0; // initialise text position
var sContents = ''; // initialise contents variable
var iRow; // initialise current row

function typewriter() {
  sContents = '';
  iRow = Math.max(0, iIndex - iScrollAt);
  var destination = document.getElementById("typedtext");

  while (iRow < iIndex) {
    sContents += aText[iRow++] + '<br />';
  }
  // Add a blinking cursor span
  if (iTextPos < iArrLength) {
    destination.innerHTML = sContents + aText[iIndex].substring(0, iTextPos) + '<span class="type-cursor">|</span>';
    iTextPos++;
    setTimeout(typewriter, iSpeed);
  } else {
    // After typing is done, show the full text and a blinking cursor
    destination.innerHTML = sContents + aText[iIndex] + '<span class="type-cursor">|</span>';
  }
}
typewriter();

// open the reset form when user clicks on forgot password button
function openResetForm() {
  document.getElementById("resetForm").style.display = "flex";
  document.getElementById("loginForm").style.display = "none";
  const form = document.getElementById("resetForm").querySelector('.form-content');
  if (form) {
    form.style.animation = "none";
    void form.offsetHeight;
    form.style.animation = "popupScale 0.3s ease-out forwards";
  }
}

// close the reset form
function closeResetForm() {
  document.getElementById("resetForm").style.display = "none";
}

function closeResetTokenModal() {
  document.getElementById('resetTokenModal').style.display = 'none';
}