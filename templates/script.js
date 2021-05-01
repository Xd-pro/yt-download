function download(fileUrl) {
    var a = document.createElement("a");
    a.href = fileUrl;
    a.setAttribute("download", fileUrl);
    a.click();
}

function startDownload() {
    var url = "http://127.0.0.1:5000/api/download";

    var xhr = new XMLHttpRequest();
    xhr.open("POST", url);

    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (!xhr.responseText === "Not a YouTube URL!") {
                console.log(xhr.responseText);
                response_data = JSON.parse(xhr.responseText)
                download(response_data.download_url)
            } else {
                alert(xhr.responseText)
            }

        }
    };

    var data = {
        download_audio: document.getElementById("audio").checked,
        video_url: document.getElementById("url").value
    };

    json = JSON.stringify(data)

    xhr.send(json);
}