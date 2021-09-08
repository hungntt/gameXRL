
function readTextFile(file, jqText) {
    var fileTypes = ['txt'];
    var fileReader = new FileReader();

    var extension = file.name.split('.').pop().toLowerCase(),  //file extension from input file
    isSuccess = fileTypes.indexOf(extension) > -1;  //is extension in acceptable types

    if (isSuccess) { //yes
        fileReader.onload = function () {
            var data = fileReader.result;
    
            jqText.val(data);
        };
        fileReader.readAsText(file);
        return true;
    }
    else { //no
        jqText.val("");
        return false;
    }
    return false;
}

// modal
function showModal(title, message, closeText) {
    $("#modal-title").text(title);
    $("#modal-message").text(message);
    $("#modal-close-text").text(closeText);

    $("#demo-modal").modal('show');
}

// loading
function showLoading(showing) {
    $(".loading").css("display", (showing ? "block" : "none"));
}