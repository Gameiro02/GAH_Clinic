<script>
  import { navigate } from "svelte-routing";
  import ModalSa from "./ModalSa.svelte";

  export let userName;
  export let userRole;

  // function goToAppointments() {
  //   console.log("Agendar Consulta");
  //   navigate("/schedule-appointment");
  // }
</script>

<div class="card bg-base-200 shadow-2xl shadow-base-100 flex-1">
  <div class="card-body items-center text-center flex-col">
    <h2 class="card-title text-base-content text-4xl">
      Bem-vindo <span class="text-primary">{userName}</span>
    </h2>
    <p class="text-base-content font-bold">Hoje é um ótimo dia para cuidar da sua saúde e bem-estar.</p>
    <!-- <button class="btn btn-primary mt-4">Agendar Consulta</button> -->
    <!-- if its a doctor dont show the modal -->
    {#if userRole !== "doctor"}
      <ModalSa />
    {/if}
  </div>
</div>

<style>
</style>
