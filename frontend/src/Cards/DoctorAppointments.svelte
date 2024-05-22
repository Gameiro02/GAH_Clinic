<script>
  import { writable } from "svelte/store";
  import { theme } from "../store.js"; // Importando apenas o tema do store original
  import { cardio } from "ldrs";

  cardio.register();

  const users = [
    { id: 1, name: "Alice" },
    { id: 2, name: "Bob" },
    // Adicione outros usuários aqui
  ];

  function getUserName(userId) {
    const user = users.find((user) => user.id === userId);
    return user ? user.name : "Desconhecido";
  }

  let selectedAppointment = null;
  let showModal = false;

  function openModal(appointment) {
    selectedAppointment = appointment;
    console.log("Appointment clicked:", appointment);
    showModal = true;
  }

  function closeModal() {
    showModal = false;
  }

  function markAsCompleted() {
    // Atualizar o status da consulta para "completed" e removê-la da lista de consultas futuras
    appointmentsData.update((currentData) => {
      return {
        ...currentData,
        upcomingAppointments: currentData.upcomingAppointments.filter(
          (app) => app.appointmentId !== selectedAppointment.appointmentId
        ),
        pastAppointments: [...currentData.pastAppointments, { ...selectedAppointment, status: "completed" }],
      };
    });
    closeModal();
  }

  const appointmentsData = writable({
    upcomingAppointments: [
      {
        date: "2024-06-01",
        appointmentId: "32ba3b0b-90bb-49cd-b2f8-204a314e78fa",
        userId: 1,
        status: "scheduled",
        specialty: "Massagem",
        time: "10:00",
        doctorId: 2,
        doctorName: "Mariana Filho",
      },
      {
        date: "2024-06-05",
        appointmentId: "39797f7a-b10f-4ffd-b2c7-c17974db49dd",
        userId: 2,
        status: "scheduled",
        specialty: "Fisioterapia",
        time: "11:00",
        doctorId: 3,
        doctorName: "Mariana Filho",
      },
    ],
    pastAppointments: [],
    missingPaymentAppointments: [],
    isLoading: false,
    errorMessage: "",
  });

  $: data = $appointmentsData;
  $: themeColor = $theme;

  $: {
    console.log("Appointments Data:", data);
  }

  function handleUpdate(event) {
    const updatedAppointment = event.detail.appointment;
    // Atualizar a lista de consultas com o estado atualizado da consulta
    appointmentsData.update((currentData) => {
      return {
        ...currentData,
        upcomingAppointments: currentData.upcomingAppointments.map((app) =>
          app.appointmentId === updatedAppointment.appointmentId ? updatedAppointment : app
        ),
      };
    });
  }
</script>

<div
  class="card w-full bg-base-200 shadow-2xl shadow-base-100 flex-1 ${themeColor === 'dark'
    ? 'shadow-white'
    : 'shadow-black'}"
>
  <div class="card-body items-center text-center p-1">
    <h2 class="card-title text-secondary text-3xl mb-2 mt-4">Próximas Consultas</h2>
    <div class="appointments flex flex-col h-full w-full">
      {#if data.isLoading}
        <div class="spinner-container flex items-center justify-center mt-20">
          <l-cardio size="150" stroke="10" speed="0.7" color="oklch(var(--s))"></l-cardio>
        </div>
      {:else if data.errorMessage}
        <p class="error text-error text-center font-bold text-xl mt-16">{data.errorMessage}</p>
      {:else if data.upcomingAppointments.length === 0}
        <p class="info text-info text-center font-bold text-xl mt-16">Não tens nenhuma consulta agendada.</p>
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
              {#each data.upcomingAppointments as appointment, index}
                <tr
                  class="bg-base-300 hover:bg-primary"
                  on:click={() => openModal(appointment)}
                  style="cursor: pointer;"
                >
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

{#if showModal && selectedAppointment}
  <dialog class="modal" open>
    <div class="modal-box flex flex-col">
      <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" on:click={closeModal}>X</button>
      <h3 class="flex-grow font-bold text-primary text-center text-3xl">Marcar Consulta como Terminada</h3>
      <div class="text text-base-content flex-grow">
        <p class="pt-4 text-center font-bold text-xl">
          Consulta de <span class="text-secondary font-bold">{selectedAppointment.specialty}</span>
          com Dr. {selectedAppointment.doctorName}
        </p>
        <p class="pt-2 text-center text-gray text-s pb-5">
          Agendada para o dia <span class="text-secondary font-bold">{selectedAppointment.date}</span>
          às <span class="text-secondary font-bold">{selectedAppointment.time}</span> horas
        </p>
      </div>
      <button class="btn btn-primary h-12 flex items-center justify-center mt-auto" on:click={markAsCompleted}
        >Marcar como Terminada</button
      >
    </div>
  </dialog>
{/if}
