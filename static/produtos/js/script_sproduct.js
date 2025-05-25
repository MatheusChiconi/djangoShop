const mainImg = document.getElementById("mainImg");
const smallImgs = document.getElementsByClassName("small-img");

if (mainImg) {
    for (const oneSmallImg of smallImgs) {
        oneSmallImg.addEventListener("click", function() {
            mainImg.src = oneSmallImg.src;
        });
    }
} else {
    console.warn("A imagem principal com ID 'mainImg' não foi encontrada. A funcionalidade de clique não será ativada.");
}
