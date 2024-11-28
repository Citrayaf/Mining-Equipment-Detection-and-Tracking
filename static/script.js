const endpointUrl = 'https://10.56.206.128:5014/equipment_detector';

async function startCamera() {
    const webcam = document.getElementById('webcam');
    const canvas = document.getElementById('mycanvas');
    const ctx = canvas.getContext('2d');

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        webcam.srcObject = stream;
    } catch (error) {
        console.error('Error accessing webcam:', error);
    }

    webcam.onloadedmetadata = () => {
        canvas.width = webcam.videoWidth;
        canvas.height = webcam.videoHeight;
        requestAnimationFrame(captureAndSendFrame);
    };

    const captureAndSendFrame = async () => {
        const video = document.createElement('video');
        video.width = canvas.width;
        video.height = canvas.height;
        video.srcObject = webcam.srcObject;

        const imageCapture = new ImageCapture(webcam.srcObject.getVideoTracks()[0]);

        const frame = await imageCapture.grabFrame();

        const imgBlob = await frameToBlob(frame);

        const formData = new FormData();
        formData.append('image', imgBlob);

        try {
            const response = await fetch(endpointUrl, {
                method: 'POST',
                body: formData,
            });

            const responseJson = await response.json();

            processApiResponse(responseJson, canvas, webcam);

        } catch (error) {
            console.error('Error sending frame to the API:', error);
        }

        requestAnimationFrame(captureAndSendFrame);
    };

    const frameToBlob = async (frame) => {
        const canvasTemp = document.createElement('canvas');
        canvasTemp.width = frame.width;
        canvasTemp.height = frame.height;
        const ctxTemp = canvasTemp.getContext('2d');
        ctxTemp.drawImage(frame, 0, 0, frame.width, frame.height);
        return new Promise((resolve) => {
            canvasTemp.toBlob(resolve, 'image/jpeg');
        });
    };

    captureAndSendFrame();
}

function processApiResponse(responseJson, canvas, webcam) {
    const videoWidth = webcam.videoWidth;
    const videoHeight = webcam.videoHeight;
    const ctx = canvas.getContext('2d');

    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.drawImage(webcam, 0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = '#00FF00';
    ctx.lineWidth = 3;
    ctx.font = '18px serif';

    ctx.beginPath();

    for (let i = 0; i < responseJson.roi.length; i++) {
        const roi = responseJson.roi[i];
        let x1 = parseInt(roi[0]);
        let y1 = parseInt(roi[1]);
        let x2 = parseInt(roi[2]);
        let y2 = parseInt(roi[3]);
        x1 = (x1 * videoWidth) / responseJson.image_width;
        y1 = (y1 * videoHeight) / responseJson.image_height;
        x2 = (x2 * videoWidth) / responseJson.image_width;
        y2 = (y2 * videoHeight) / responseJson.image_height;
        const label = responseJson.label[i];
        const score = responseJson.identification_score[i];
        const color = label === 'NO-Hardhat' || label === 'NO-Mask' || label === 'NO-Safety Vest' ? 'red' : 'green';

        if (score >= 50) {
            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            ctx.rect(x1, y1, x2 - x1, y2 - y1);
            ctx.fillStyle = color;
            ctx.stroke();

            const text = `${label}: ${score.toFixed(2)}`;
            const width = ctx.measureText(text).width;
            ctx.font = '16px Arial';
            ctx.fillStyle = color;
            ctx.fillText(text, x1, y1 + 18);
        }
    }
}

startCamera();
