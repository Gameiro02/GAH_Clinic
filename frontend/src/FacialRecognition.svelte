<script>
  import { onMount } from 'svelte';
  import { DOMAIN } from './config.js';

  let video;
  let canvas;
  let error = '';
  let isVideoReady = false;

  // Get access to the camera
  onMount(() => {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        video.srcObject = stream;
        video.play();
        video.onloadedmetadata = () => {
          isVideoReady = true;
          startCapture();
        };
      })
      .catch(err => {
        console.error("Error accessing the camera: " + err);
        error = 'Error accessing the camera: ' + err.message;
      });
  });

  // Function to continuously capture images
  function startCapture() {
    canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    const captureInterval = setInterval(async () => {
      if (!isVideoReady || !video.videoWidth || !video.videoHeight) return;

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      const dataURL = canvas.toDataURL('image/png');

      const base64Image = dataURL.split(',')[1];
      try {
        const response = await fetch(`${DOMAIN}/clinic/login/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ image: base64Image })
        });

        const data = await response.json();
        if (response.ok) {
          clearInterval(captureInterval); // Stop capturing once logged in
          alert(data.message);
        } else {
          error = data.message;
          console.log('Login attempt failed: ', data.message);
        }
      } catch (err) {
        console.error('Error: ' + err.message);
      }
    }, 1000); // Capture every second
  }
</script>

<div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
  <h1 class="text-2xl font-bold mb-4">Webcam Login</h1>
  {#if error}
    <div class="text-red-500 mb-4">{error}</div>
  {/if}
  <div class="card w-96 bg-base-100 shadow-xl justify-center items-center">
    <video bind:this={video} width="640" height="480" class="border rounded shadow mb-4"></video>
  </div>
</div>

<style>
  video {
    max-width: 100%;
  }
</style>
