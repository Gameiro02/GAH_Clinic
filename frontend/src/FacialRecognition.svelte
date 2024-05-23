<script>
  import { DOMAIN } from "./config.js";
  import Navbar from "./Navbar.svelte";
  import { pulsar } from 'ldrs'

  pulsar.register();

  let video;
  let canvas;
  let error = "";
  let isVideoReady = false;
  let showVideo = false;
  let loggedIn = false;

  function startCamera() {
    showVideo = true;

    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        video = document.createElement("video");
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
  }

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
          video.srcObject.getTracks().forEach((track) => track.stop());
          error = "";
          showVideo = false;
          loggedIn = true;

        } else {
          error = data.message;
          console.log("Login attempt failed: ", data.message);
        }
      } catch (err) {
        console.error("Error: " + err.message);
      }
    }, 2500); // Capture every second
  }
</script>

<div class="flex flex-col h-screen bg-base-100">
  <Navbar />
  <div class="flex justify-center h-screen items-center">
    <div class="card w-96 h-80 max-w-sm shadow-2xl bg-base-200">
      <div class="card-body flex flex-col justify-between items-stretch w-full h-full flex-1">
        <h2 class="card-title justify-center text-secondary text-3xl">Facial Recognition</h2>
        <div class="flex flex-col flex-grow justify-center items-center">
          {#if !showVideo}
            {#if !loggedIn}
              <button on:click={startCamera} class="btn w-40 btn-primary text justify-center">Start Webcam</button>
            {:else}
              <div class="text-center font-bold text-2xl  text-primary">Logged in</div>
              <div class="text-center">Redirecting you to the clinic...</div>
            {/if}
          {:else}
            {#if !loggedIn}
              <div class="text-center font-semibold text-lg mb-4">Looking for your face...</div>
              <div class="spinner-container">
                <l-pulsar
                  size="40"
                  speed="1.75" 
                  color="oklch(var(--s))" 
                ></l-pulsar>
              </div>
            {/if}
          {/if}
        </div>
        {#if error}
          <div class="text-red-500 text-center">{error}</div>
        {:else}
          <div class="text-center invisible">Temp</div>
        {/if}
      </div>
    </div>
  </div>
</div>
