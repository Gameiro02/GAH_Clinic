<script>
  import Navbar from "./Navbar.svelte";
  import { onMount } from "svelte";

  let selectedDoctor = null;
  const doctors = [
    { id: 1, name: "Pedro Pais" },
    { id: 2, name: "Afonso Mora" },
    { id: 3, name: "Mariana Filho" },
    { id: 4, name: "Carlos Sousa" },
  ];

  function handleLogin() {
    if (selectedDoctor) {
      alert(`Doctor ${selectedDoctor.name} logged in!`);
    } else {
      alert("Please select a doctor.");
    }
  }

  // Function to change the image of the doctor based on selection
  function getDoctorImage() {
    if (selectedDoctor) {
      return `/photo-${selectedDoctor.name.toLowerCase().replace(" ", "-")}.jpeg`;
    } else {
      return "https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.jpg";
    }
  }

  // Initialize the image when component mounts
  onMount(() => {
    document.querySelector(".avatar img").src = getDoctorImage();
  });

  // Update the image whenever the selected doctor changes
  $: if (selectedDoctor) {
    document.querySelector(".avatar img").src = getDoctorImage();
  }
</script>

<main class="flex flex-col mx-auto w-screen h-screen px-6 pt-2 pb-6 overflow-hidden">
  <Navbar />
  <div class="flex items-center justify-center min-h-screen">
    <div class="card w-full max-w-lg bg-base-200 shadow-base-100 shadow-2xl p-8">
      <div class="flex flex-col items-center">
        <div class="avatar mb-8">
          <div class="w-52 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
            <img alt="doctor face" src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.jpg" />
          </div>
        </div>
        <div class="mb-8 text-center">
          <h2 class="text-2xl text-base-content font-bold">Login</h2>
        </div>
        <div class="mb-8 w-full">
          <select class="select select-bordered w-full" bind:value={selectedDoctor}>
            <option value="" disabled selected>Select a doctor</option>
            {#each doctors as doctor}
              <option value={doctor}>{doctor.name}</option>
            {/each}
          </select>
        </div>
        <div class="text-center w-full">
          <button class="btn btn-primary w-full" on:click={handleLogin}>Login</button>
        </div>
      </div>
    </div>
  </div>
</main>
