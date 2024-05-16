<script>
    import { onMount } from 'svelte';
    import { DOMAIN } from './config.js';
  
    let video;
    let canvas;
    let error = '';
  
    // Get access to the camera
    onMount(() => {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          video.srcObject = stream;
          video.play();
        })
        .catch(err => {
          console.error("Error accessing the camera: " + err);
          error = 'Error accessing the camera: ' + err.message;
        });
    });
  
    // Capture the image
    async function captureImage() {
      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      const dataURL = canvas.toDataURL('image/png');
  
      try {
        const response = await fetch(`${DOMAIN}/clinic/login/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ image: dataURL })
        });
  
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
        } else {
          error = data.message || 'Login failed';
        }
      } catch (err) {
        error = 'Error: ' + err.message;
      }
    }
  </script>
  
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
    <h1 class="text-2xl font-bold mb-4">Webcam Login</h1>
    {#if error}
      <div class="text-red-500 mb-4">{error}</div>
    {/if}
    <video bind:this={video} width="640" height="480" class="border rounded shadow mb-4"></video>
    <button on:click={captureImage} class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Capture</button>
    <canvas bind:this={canvas} width="640" height="480" class="hidden"></canvas>
  </div>
  
  <style>
    video {
      max-width: 100%;
    }
  </style>
  