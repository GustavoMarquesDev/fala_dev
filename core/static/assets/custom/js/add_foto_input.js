function addInput(input) {
  if (input.files.length > 0) {
    let container = document.getElementById("fotos-container");
    let inputs = container.querySelectorAll('input[type="file"]');
    let lastInput = inputs[inputs.length - 1];
    if (lastInput === input) {
      let newInput = document.createElement("input");
      newInput.type = "file";
      newInput.name = "fotos";
      newInput.className = "form-control mt-2";
      newInput.onchange = function () {
        addInput(this);
      };
      container.appendChild(newInput);
    }
    // Preview das imagens
    let previewContainer = document.getElementById("fotos-preview");
    if (!previewContainer) {
      previewContainer = document.createElement("div");
      previewContainer.id = "fotos-preview";
      previewContainer.style.display = "flex";
      previewContainer.style.flexWrap = "wrap";
      previewContainer.style.gap = "10px";
      container.parentNode.insertBefore(
        previewContainer,
        container.nextSibling
      );
    }
    // Limpa previews anteriores do input
    let previews = input._previews || [];
    previews.forEach((img) => previewContainer.removeChild(img));
    input._previews = [];
    for (let i = 0; i < input.files.length; i++) {
      let file = input.files[i];
      let reader = new FileReader();
      reader.onload = function (e) {
        let img = document.createElement("img");
        img.src = e.target.result;
        img.style.width = "80px";
        img.style.height = "80px";
        img.style.objectFit = "cover";
        img.style.borderRadius = "8px";
        previewContainer.appendChild(img);
        input._previews.push(img);
      };
      reader.readAsDataURL(file);
    }
  }
}
