<script>
  import { DOMAIN } from "./config.js";
  import { onMount } from "svelte";

  let selectedSpecialty = "";
  let selectedDoctor = "";
  let selectedDate = "";
  let selectedTime = "";
  let modalOpen = false;

  const specialties = ["Massagem", "Fisioterapia", "Psicologia", "Ortopedia"];
  const doctors = [
    { id: 1, name: "Pedro Pais" },
    { id: 2, name: "Afonso Mora" },
    { id: 3, name: "Mariana Filho" },
    { id: 4, name: "Carlos Sousa" },
  ];

  async function scheduleAppointment(event) {
    event.preventDefault(); // Prevent default form submission
    try {
      const tokenString = localStorage.getItem("jwt");
      if (tokenString) {
        const token = JSON.parse(tokenString);

        // Get date and time from the form
        const specialty = selectedSpecialty;
        const doctorId = parseInt(selectedDoctor);
        const date = new Date(selectedDate).toISOString().slice(0, 10); // Gets 'YYYY-MM-DD'
        const time = selectedTime;

        const requestData = JSON.stringify({
          specialty,
          doctorId,
          date,
          time,
        });

        console.log("Request data:", requestData);

        const response = await fetch(`${DOMAIN}/book-appointment/`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: requestData,
        });

        if (!response.ok) {
          throw new Error("Failed to schedule appointment");
        }

        console.log("Appointment scheduled successfully");
        closeModal(); // Close the modal after successfully scheduling the appointment
      }
    } catch (error) {
      console.error("Error scheduling appointment:", error.message);
    }
  }

  function showModal() {
    modalOpen = true;
  }

  function closeModal() {
    modalOpen = false;
  }

  // Function to close the modal when clicking outside the modal content
  function handleClickOutside(event) {
    if (event.target.id === "modal-overlay") {
      closeModal();
    }
  }

  onMount(() => {
    // Close modal with ESC key
    function handleKeyDown(event) {
      if (event.key === "Escape") {
        closeModal();
      }
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  });
</script>

<button class="btn btn-primary mt-4" on:click={showModal}>
  Agendar Consulta
</button>

{#if modalOpen}
  <button
    id="modal-overlay"
    class="fixed inset-0 bg-black bg-opacity-50 z-40 flex justify-center items-center"
    on:click={handleClickOutside}
    aria-label="Close Modal Overlay"
  >
    <div class="card w-full max-w-md bg-base-100 mx-auto flex-1 relative">
      <div class="relative p-4">
        <h3 class="text-2xl font-bold text-primary text-center">
          Agendar Consulta
        </h3>
        <button
          class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
          on:click={closeModal}
          aria-label="Close Modal">X</button
        >
      </div>
      <div class="card-body items-center text-center p-4 pt-0">
        <p class="font-bold text-sm text-base-content">
          Preencha os detalhes abaixo para agendar sua consulta.
        </p>
        <form on:submit={scheduleAppointment} class="w-full">
          <div class="space-y-3 mt-3">
            <div>
              <label
                for="specialty"
                class="text-md text-center font-bold text-primary"
                >Especialidade:</label
              >
              <select
                id="specialty"
                bind:value={selectedSpecialty}
                class="select select-bordered w-full text-base-content"
                required
              >
                <option value="" disabled selected></option>
                {#each specialties as specialty}
                  <option value={specialty}>{specialty}</option>
                {/each}
              </select>
            </div>

            <div>
              <label
                for="doctor"
                class="text-md text-center font-bold text-primary"
                >Médico:</label
              >
              <select
                id="doctor"
                bind:value={selectedDoctor}
                class="select select-bordered w-full text-base-content"
                required
              >
                <option value="" disabled selected></option>
                {#each doctors as doctor}
                  <option value={doctor.id}>{doctor.name}</option>
                {/each}
              </select>
            </div>

            <div>
              <label
                for="date"
                class="text-md text-center font-bold text-primary">Data:</label
              >
              <input
                id="date"
                type="date"
                bind:value={selectedDate}
                class="input input-bordered w-full text-base-content"
                required
              />
            </div>

            <div>
              <label
                for="time"
                class="text-md text-center font-bold text-primary">Hora:</label
              >
              <input
                id="time"
                type="time"
                bind:value={selectedTime}
                class="input input-bordered w-full text-base-content"
                required
              />
            </div>
          </div>

          <div class="modal-action mt-4 flex justify-center">
            <button type="submit" class="btn btn-primary flex-1"
              >Marcar Consulta</button
            >
          </div>
        </form>
      </div>
    </div>
  </button>
{/if}
