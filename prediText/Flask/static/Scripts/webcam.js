(function() {

    const video = document.querySelector('#basic video');
    const audio = document.querySelector('#basic audio');

    const captureVideoButton = document.querySelector('#basic .capture-button');
    const stopVideoButton = document.querySelector('#basic #stop-button');

    //Capture Video
    captureVideoButton.onclick = function() {
        navigator.mediaDevices.getUserMedia({
            audio: true,
            video: true
        })
            .then(stream => {
                window.localStream = stream;
                video.srcObject = stream;
                audio.srcObject = stream;
            })
            .catch((err) => {
                console.log(err);
            });
    };

    stopVideoButton.onclick = function() {
        localStream.getVideoTracks()[0].stop();
        video.src = '#';
    };
})();