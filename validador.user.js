// ==UserScript==
// @name        Validador de NIF
// @namespace   Violentmonkey Scripts
// @match       https://sata-ssp-ngen.npf.com.pt/sataNGen2/dashboard-flight-reservation*
// @grant       none
// @version     1.0
// @author      Shino
// @description 29/03/2025, 16:09:43
// ==/UserScript==

function ValidateNIF(arg1) {
  let rev = arg1.split("").reverse();
  let check_digit = parseInt(rev.splice(0, 1));
  let _sum = 0;

  for (i = 0; i < rev.length; i++) {
    _sum += parseInt(rev[i]) * (i + 2);
  }

  var remainder = _sum % 11;

  if (remainder <= 1) remainder = 0;
  else remainder = 11 - remainder;

  return remainder === check_digit;
}

var checker = setInterval(function () {
  let nifs = document.querySelectorAll(`input[ng-model="passenger.NIF"]`);
  if (nifs.length != 0) {
    clearInterval(checker);
  }

  for (let i = 0; i < nifs.length; i++) {
    let old_style = nifs[0].style.border;
    let nif = nifs[i].addEventListener("input", (arg) => {
      var value_nif = arg.target;

      if (value_nif.value.length === 9) {
        switch (ValidateNIF(value_nif.value)) {
          case true:
            value_nif.style.border = "3px solid green";
            break;
          default:
            value_nif.style.border = "3px solid red";
            break;
        }
      } else {
        value_nif.style.border = old_style;
      }
    });
  }
}, 1000);
