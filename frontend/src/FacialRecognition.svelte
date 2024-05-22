<script>
  import { onMount } from "svelte";
  import { DOMAIN } from "./config.js";
  import Navbar from "./Navbar.svelte";

  let video;
  let canvas;
  let error = "";
  let isVideoReady = false;

  // Get access to the camera
  onMount(() => {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        video.srcObject = stream;
        video.play();
        video.onloadedmetadata = () => {
          isVideoReady = true;
          startCapture();
        };
      })
      .catch((err) => {
        console.error("Error accessing the camera: " + err);
        error = "Error accessing the camera: " + err.message;
      });
  });

  // Function to continuously capture images
  function startCapture() {
    canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    const captureInterval = setInterval(async () => {
      if (!isVideoReady || !video.videoWidth || !video.videoHeight) return;

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      const dataURL = canvas.toDataURL("image/png");

      const base64Image = dataURL.split(",")[1];
      try {
        const response = await fetch(`${DOMAIN}/clinic/login/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ image: base64Image }),
        });

        const data = await response.json();
        if (response.ok) {
          clearInterval(captureInterval); // Stop capturing once logged in
          alert(data.message);
        } else {
          error = data.message;
          console.log("Login attempt failed: ", data.message);
        }
      } catch (err) {
        console.error("Error: " + err.message);
      }
    }, 1000); // Capture every second
  }
</script>

<div class="flex flex-col min-h-screen bg-base-100">
  <Navbar />
  <div class="flex flex-col items-center justify-center flex-1 mt-[-3rem]">
    <div class="p-8 rounded-lg shadow-lg bg-base-200 w-full max-w-4xl">
      <h1 class="text-2xl font-bold mb-4">Webcam Login</h1>
      {#if error}
        <div class="text-red-500 mb-4">{error}</div>
      {/if}
      <div class="w-full flex justify-center bg-base-100">
        <video bind:this={video} width="800" height="600">
          <track kind="captions" src="" srclang="en" label="English" default />
        </video>
      </div>
    </div>
  </div>
</div>

<style>
  video {
    max-width: 100%;
  }
</style>
