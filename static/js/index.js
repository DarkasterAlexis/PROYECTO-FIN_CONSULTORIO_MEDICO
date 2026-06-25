// Sonidos
const hoverSound = new Audio("/static/sounds/hover.mp3");
const clickSound = new Audio("/static/sounds/click.mp3");

hoverSound.volume = 0.3;
clickSound.volume = 0.4;

/*==============================
  SONIDO HOVER
==============================*/

document.querySelectorAll(".efecto-sonido").forEach(elemento => {

    elemento.addEventListener("mouseenter", () => {

        hoverSound.currentTime = 0;

        hoverSound.play().catch(() => {});

    });

});


/*==============================
  ENLACES (<a>)
==============================*/

document.querySelectorAll("a.boton-sonido").forEach(link => {

    link.addEventListener("click", function (e) {

        // Ignorar enlaces sin href válido
        const destino = this.getAttribute("href");

        if (!destino || destino === "#") {
            return;
        }

        e.preventDefault();

        clickSound.pause();
        clickSound.currentTime = 0;

        clickSound.play().catch(() => {});

        setTimeout(() => {

            window.location.href = destino;

        }, 550);

    });

});


/*==============================
  FORMULARIOS (LOGIN)
==============================*/

document.querySelectorAll("form").forEach(formulario => {

    formulario.addEventListener("submit", function(e){

        e.preventDefault();

        clickSound.currentTime = 0;

        clickSound.play().catch(() => {});

        setTimeout(() => {

            formulario.submit();

        }, 550);

    });

});