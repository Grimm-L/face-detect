const constraints = {
    video: true,
};

var video = document.querySelector("video");

navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
    video.srcObject = stream;
});

const canvas = document.createElement("canvas");
canvas.width = 640;
canvas.height = 480;
const context = canvas.getContext("2d");

setInterval(
    function () {
        context.drawImage(video, 0, 0);
        canvas.toBlob((blob) => {
            const formData = new FormData();
            formData.append("file", blob, "image.png");
            fetch("/detect/detect_dev_api", {
                method: "POST",
                body: formData,
            }).then((response) => {
                response.text().then((text) => {
                    // console.log(text);
                    if(text == "empty"){
                        $("tbody").html("");
                        $("#user_name").text("");
                        $("#total_cnt").text("0");
                        $("#total_price").text("0");
                        $("#rem").text("0");
                    }else if (text != "no change") {
                        $(window.document.body).html(text);
                        video = document.querySelector("video");
                        navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
                            video.srcObject = stream;
                        });
                    } 
                });

            });
        }
        );
    },
    200000);