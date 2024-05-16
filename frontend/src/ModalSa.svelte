<script>
  import { DOMAIN } from "./config.js";
  import { onMount } from "svelte";

  let selectedSpecialty = "";
  let selectedDoctor = "";
  let selectedDate = "";
  let selectedTime = "";
  let modalOpen = false;
  let isLoading = false;
  let errorMessage = "";

  const specialties = ["Massagem", "Fisioterapia", "Psicologia", "Ortopedia"];
  const doctors = [
    { id: 1, name: "Pedro Pais" },
    { id: 2, name: "Afonso Mora" },
    { id: 3, name: "Mariana Filho" },
    { id: 4, name: "Carlos Sousa" },
  ];

  function handleTimeChange(event) {
    const value = event.target.value;
    const [hours] = value.split(":");
    selectedTime = `${hours}:00`;
  }

  function handleFocus(event) {
    const value = event.target.value;
    if (value === "") {
      const [hours] = value.split(":");
      selectedTime = `${hours}:00`;
    }
  }

  async function scheduleAppointment(event) {
    event.preventDefault();
    isLoading = true;
    errorMessage = "";
    try {
      const tokenString = localStorage.getItem("jwt");
      if (tokenString) {
        const token = JSON.parse(tokenString);

        const specialty = selectedSpecialty;
        const doctorId = parseInt(selectedDoctor);
        const date = new Date(selectedDate).toISOString().slice(0, 10);
        const time = selectedTime;

        const requestData = JSON.stringify({
          specialty,
          doctorId,
          date,
          time,
        });

        const response = await fetch(`${DOMAIN}/book-appointment/`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: requestData,
        });

        if (!response.ok) {
          if (response.status === 409) {
            throw new Error("Já existe uma marcação para este horário");
          }
          throw new Error("Falha ao agendar consulta");
        }

        console.log("Appointment scheduled successfully");
        closeModal();
      }
    } catch (error) {
      errorMessage = error.message;
      console.error("Error scheduling appointment:", error.message);
    } finally {
      isLoading = false;
    }
  }

  function showModal() {
    modalOpen = true;
  }

  function closeModal() {
    modalOpen = false;
    isLoading = false;
    errorMessage = "";
    resetForm();
  }

  function resetForm() {
    selectedSpecialty = "";
    selectedDoctor = "";
    selectedDate = "";
    selectedTime = "";
  }

  function handleClickOutside(event) {
    if (event.target.id === "modal-overlay") {
      closeModal();
    }
  }

  function handleKeyDownOutside(event) {
    if (event.key === "Escape" || event.key === "Enter") {
      closeModal();
    }
  }

  onMount(() => {
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
  <div
    id="modal-overlay"
    class="fixed inset-0 bg-black bg-opacity-50 z-40 flex justify-center items-center"
    on:click={handleClickOutside}
    on:keydown={handleKeyDownOutside}
    tabindex="0"
    role="button"
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
          aria-label="Close Modal"
          disabled={isLoading}
        >
          {#if isLoading}
            <svg
              class="animate-spin h-5 w-5 text-primary"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v8h8a8 8 0 11-8 8V4z"
              ></path>
            </svg>
          {:else}
            X
          {/if}
        </button>
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
                on:input={handleTimeChange}
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
                on:input={handleTimeChange}
                on:focus={handleFocus}
                required
              />
            </div>
          </div>

          {#if errorMessage}
            <p class="text-center text-error font-bold mt-3">{errorMessage}</p>
          {/if}

          <div class="modal-action mt-4 flex justify-center">
            {#if isLoading}
              <div
                class="spinner-container flex items-center justify-center h-12 mt-auto"
              >
                <l-cardio
                  size="60"
                  stroke="4"
                  speed="0.7"
                  color="oklch(var(--s))"
                ></l-cardio>
              </div>
            {:else}
              <button type="submit" class="btn btn-primary flex-1">
                Marcar Consulta
              </button>
            {/if}
          </div>
        </form>
      </div>
    </div>
  </div>
{/if}
