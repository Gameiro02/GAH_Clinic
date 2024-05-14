<script>
  import { DOMAIN } from "./config.js";
  import { onMount } from 'svelte';

  let selectedSpecialty = '';
  let selectedDoctor = '';
  let selectedDate = '';
  let selectedTime = '';
  let modalOpen = false;

  async function scheduleAppointment(event) {
    event.preventDefault();  // Prevenir a ação padrão de envio do formulário
    try {
      const tokenString = localStorage.getItem("jwt");
      if (tokenString) {
        const token = JSON.parse(tokenString);

        // Get date and time from the form
        const specialty = selectedSpecialty;
        const doctorId = parseInt(selectedDoctor);
        const date = new Date(selectedDate).toISOString().slice(0, 10);  // Gets 'YYYY-MM-DD'
        const time = selectedTime;
        
        const requestData = JSON.stringify({
          specialty,
          doctorId,
          date,
          time
        });

        console.log("Request data:", requestData)

        const response = await fetch(`${DOMAIN}/book-appointment/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: requestData
        });

        if (!response.ok) {
          throw new Error('Failed to schedule appointment');
        }

        console.log("Appointment scheduled successfully");
        closeModal();  // Fechar o modal após agendar a consulta com sucesso
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

  // Função para fechar o modal ao clicar fora do conteúdo do modal
  function handleClickOutside(event) {
    if (event.target.id === 'modal-overlay') {
      closeModal();
    }
  }

  onMount(() => {
    // Fechar modal com a tecla ESC
    function handleKeyDown(event) {
      if (event.key === 'Escape') {
        closeModal();
      }
    }
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  });
</script>

<button class="btn btn-primary mt-4" on:click={showModal}>
  Agendar Consulta
</button>

{#if modalOpen}
<div id="modal-overlay" class="fixed inset-0 bg-black bg-opacity-50 z-40 flex justify-center items-center" on:click={handleClickOutside}>
  <div class="card w-full max-w-md bg-base-100 mx-auto flex-1 relative">
    <div class="relative p-4">
      <h3 class="text-2xl font-bold text-primary text-center">Schedule Your Appointment</h3>
      <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" on:click={closeModal}>X</button>
    </div>
    <div class="card-body items-center text-center p-4 pt-0">
      <p class="font-bold text-sm text-base-content">Fill in the details below to set up your appointment.</p>
      <form on:submit={scheduleAppointment} class="w-full">
        <div class="space-y-3 mt-3">
          <div>
            <label for="specialty" class="text-md text-center font-bold text-primary">Specialty:</label>
            <input id="specialty" type="text" bind:value={selectedSpecialty} class="input input-bordered w-full text-base-content" required>
          </div>

          <div>
            <label for="doctor" class="text-md text-center font-bold text-primary">Doctor:</label>
            <input id="doctor" type="text" bind:value={selectedDoctor} class="input input-bordered w-full text-base-content" required>
          </div>

          <div>
            <label for="date" class="text-md text-center font-bold text-primary">Date:</label>
            <input id="date" type="date" bind:value={selectedDate} class="input input-bordered w-full text-base-content" required>
          </div>

          <div>
            <label for="time" class="text-md text-center font-bold text-primary">Time:</label>
            <input id="time" type="time" bind:value={selectedTime} class="input input-bordered w-full text-base-content" required>
          </div>
        </div>

        <div class="modal-action mt-4 flex justify-center">
          <button type="submit" class="btn btn-primary flex-1">Set Appointment</button>
        </div>
      </form>
    </div>
  </div>
</div>
{/if}
