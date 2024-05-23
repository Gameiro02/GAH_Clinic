<script>
  import { cardio } from "ldrs";
  import { onMount } from "svelte";
  import { doctorsAppointments } from "../store";

  cardio.register();

  const users = [
    { id: 1, name: "Alice" },
    { id: 2, name: "Bob" },
  ];

  function getUserName(userId) {
    const user = users.find((user) => user.id === userId);
    return user ? user.name : "Desconhecido";
  }

  let doctorId;
  let filteredAppointments = [];

  onMount(() => {
    // Get the id from the last part of the URL
    const url = window.location.href;
    doctorId = url.substring(url.lastIndexOf("/") + 1);
  });

  $: data = $doctorsAppointments;
  $: filteredAppointments = data.pastAppointments;
</script>

<div class="card w-full bg-base-200 shadow-base-100 shadow-2xl flex-1">
  <div class="card-body items-center text-center p-1">
    <h2 class="card-title text-secondary text-3xl mb-2 mt-4">Histórico de Consultas</h2>
    <div class="appointments flex flex-col h-full w-full">
      {#if data.isLoading}
        <div class="spinner-container flex items-center justify-center mt-20">
          <l-cardio size="150" stroke="10" speed="0.7" color="oklch(var(--s))"></l-cardio>
        </div>
      {:else if data.errorMessage}
        <p class="error text-error text-center font-bold text-xl mt-16">{data.errorMessage}</p>
      {:else if filteredAppointments.length === 0}
        <p class="info text-info text-center font-bold text-xl mt-16">Ainda não tiveste nenhuma consulta.</p>
      {:else}
        <div class="overflow-y-auto max-h-96">
          <table class="table w-full min-w-full bg-base-200 border-separate border-spacing-y-2">
            <thead class="border-b-2 border-bg-base-200 text-accent">
              <tr>
                <th class="text-xl text-center rounded-tl-full py-3">Especialidade</th>
                <th class="text-xl text-center py-3">Paciente</th>
                <th class="text-xl text-center py-3">Data</th>
                <th class="text-xl text-center rounded-tr-full py-3">Hora</th>
              </tr>
            </thead>
            <tbody>
              {#each filteredAppointments as appointment, index}
                <tr class="hover:bg-primary bg-base-300">
                  <td class="text-base-content text-center font-medium rounded-l-full py-4">{appointment.specialty}</td>
                  <td class="text-base-content text-center font-medium py-4">{getUserName(appointment.userId)}</td>
                  <td class="text-base-content text-center font-medium py-4">{appointment.date}</td>
                  <td class="text-base-content text-center font-medium rounded-r-full py-4">{appointment.time}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {/if}
    </div>
  </div>
</div>
