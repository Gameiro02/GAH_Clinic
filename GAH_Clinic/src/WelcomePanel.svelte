<script>
  import Calendar from "./Calendar.svelte";
  import { navigate } from "svelte-routing";

  export let userName;

  function goToAppointments() {
    console.log("Agendar Consulta");
    navigate("/schedule-appointment");
  }
</script>

<div class="card bg-base-200 shadow-xl flex-1" style="height: 30vh;">
  <div class="card-body items-center text-center">
    <h2 class="card-title text-base-content text-4xl mb-4">Bem-vindo <span class="text-primary">{userName}</span></h2>
    <p class="text-base-content mb-6">Hoje é um ótimo dia para cuidar da sua saúde e bem-estar.</p>
    <button class="btn btn-primary" on:click={goToAppointments}>Agendar Consulta</button>
  </div>
</div>

<style>
</style>
