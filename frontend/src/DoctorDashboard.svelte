<script>
  import { onMount } from "svelte";
  import WelcomePanel from "./WelcomePanel.svelte";
  import Navbar from "./Navbar.svelte";

  let selectedDoctor = null;
  const doctors = [
    { id: 1, name: "Pedro Pais" },
    { id: 2, name: "Afonso Mora" },
    { id: 3, name: "Mariana Filho" },
    { id: 4, name: "Carlos Sousa" },
  ];

  onMount(() => {
    // Get the id from the last digit of the URL
    const url = window.location.href;
    const id = url.substring(url.lastIndexOf("/") + 1);

    // Get the doctor object from the id
    selectedDoctor = doctors.find((doctor) => doctor.id == id);
    console.log(selectedDoctor);

    // Handle case where doctor is not found
    if (!selectedDoctor) {
      selectedDoctor = { name: "Unknown Doctor" };
    }
  });
</script>

<main class="flex flex-col mx-auto w-screen h-screen px-6 pt2 pb-6">
  <Navbar />
  <div class="flex flex-col flex-grow space-y-5">
    <div class="welcome">
      <WelcomePanel userName={selectedDoctor ? selectedDoctor.name : "Loading..."} />
    </div>
    <!-- <div class="flex flex-col flex-grow md:flex-row space-y-5 md:space-y-0 md:space-x-5">
        <HistoryPanel />
        <AppointmentsPanel />
      </div> -->
  </div>
</main>
