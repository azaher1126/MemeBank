let tagify = null;

document.addEventListener("DOMContentLoaded", () => {
    const tags_input = document.getElementById("tags");
    tagify = new Tagify(tags_input)

    const file_upload = document.getElementById("file-upload");
    file_upload.addEventListener("change", readURL);
});

function readURL() {
    if (this.files && this.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            document.getElementById("imageResult").setAttribute("src", e.target.result);
        };
        reader.readAsDataURL(this.files[0]);
    }
  }