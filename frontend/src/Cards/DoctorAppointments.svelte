<script>
  import { theme } from "../store.js"; // Importando apenas o tema do store original
  import { cardio } from "ldrs";
  import { doctorsAppointments } from "../store.js";
  import { DOMAIN } from "../config.js";

  cardio.register();

  // DADOS DE EXEMPLO ESTATICOS
  const users = [
    { id: 1, name: "Alice" },
    { id: 2, name: "Bob" },
  ];

  function getUserName(userId) {
    const user = users.find((user) => user.id === userId);
    return user ? user.name : "Desconhecido";
  }

  let selectedAppointment = null;
  let showModal = false;

  function openModal(appointment) {
    selectedAppointment = appointment;
    showModal = true;
  }

  function closeModal() {
    showModal = false;
  }

  async function markAsCompleted() {
    try {
      const tokenString = localStorage.getItem("jwt");
      if (tokenString) {
        const token = JSON.parse(tokenString);

        const requestData = JSON.stringify({
          appointmentId: selectedAppointment.appointmentId,
          userId: selectedAppointment.userId,
        });

        const response = await fetch(
          `${DOMAIN}/appointments/finish/`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`, // Assuming your API requires JWT in Authorization header
            },
            body: requestData,
          }
        );

        if (!response.ok) {
          throw new Error("Failed to finish appointment");
        }

        console.log("Appointment was marked as finished");
      }
    } catch (error) {
      console.error(error);
    }

    closeModal();
  }

  $: data = $doctorsAppointments;
  $: themeColor = $theme;
</script>

<div
  class="card w-full bg-base-200 shadow-2xl shadow-base-100 flex-1 ${themeColor ===
  'dark'
    ? 'shadow-white'
    : 'shadow-black'}"
>
  <div class="card-body items-center text-center p-1">
    <h2 class="card-title text-secondary text-3xl mb-2 mt-4">
      Próximas Consultas
    </h2>
    <div class="appointments flex flex-col h-full w-full">
      {#if data.isLoading}
        <div class="spinner-container flex items-center justify-center mt-20">
          <l-cardio size="150" stroke="10" speed="0.7" color="oklch(var(--s))"
          ></l-cardio>
        </div>
      {:else if data.errorMessage}
        <p class="error text-error text-center font-bold text-xl mt-16">
          {data.errorMessage}
        </p>
      {:else if data.upcomingAppointments.length === 0}
        <p class="info text-accent text-center font-bold text-xl mt-16">
          Não tens nenhuma consulta agendada.
        </p>
      {:else}
        <div class="overflow-y-auto max-h-96">
          <table
            class="table w-full min-w-full bg-base-200 border-separate border-spacing-y-2"
          >
            <thead class="border-b-2 border-bg-base-200 text-accent">
              <tr>
                <th class="text-xl text-center rounded-tl-full py-3"
                  >Especialidade</th
                >
                <th class="text-xl text-center py-3">Paciente</th>
                <th class="text-xl text-center py-3">Data</th>
                <th class="text-xl text-center rounded-tr-full py-3">Hora</th>
              </tr>
            </thead>
            <tbody>
              {#each data.upcomingAppointments as appointment, index}
                <tr
                  class="bg-base-300 hover:bg-primary"
                  on:click={() => openModal(appointment)}
                  style="cursor: pointer;"
                >
                  <td
                    class="text-base-content text-center font-medium rounded-l-full py-4"
                    >{appointment.specialty}</td
                  >
                  <td class="text-base-content text-center font-medium py-4"
                    >{getUserName(appointment.userId)}</td
                  >
                  <td class="text-base-content text-center font-medium py-4"
                    >{appointment.date}</td
                  >
                  <td
                    class="text-base-content text-center font-medium rounded-r-full py-4"
                    >{appointment.time}</td
                  >
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {/if}
    </div>
  </div>
</div>

{#if showModal && selectedAppointment}
  <dialog class="modal" open>
    <div class="modal-box flex flex-col">
      <button
        class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
        on:click={closeModal}>X</button
      >
      <h3 class="flex-grow font-bold text-primary text-center text-3xl">
        Marcar Consulta como Terminada
      </h3>
      <div class="text text-base-content flex-grow">
        <p class="pt-4 text-center font-bold text-xl">
          Consulta de <span class="text-secondary font-bold"
            >{selectedAppointment.specialty}</span
          >
        </p>
        <p class="pt-2 text-center text-gray text-s pb-5">
          Agendada para o dia <span class="text-secondary font-bold"
            >{selectedAppointment.date}</span
          >
          às
          <span class="text-secondary font-bold"
            >{selectedAppointment.time}</span
          > horas
        </p>
      </div>
      <button
        class="btn btn-primary h-12 flex items-center justify-center mt-auto"
        on:click={markAsCompleted}>Marcar como Terminada</button
      >
    </div>
  </dialog>
{/if}
