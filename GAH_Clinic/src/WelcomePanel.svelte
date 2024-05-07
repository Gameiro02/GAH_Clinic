<script>
  import Calendar from "./Calendar.svelte";
  import { navigate } from "svelte-routing";

  export let userName;

  function goToAppointments() {
    console.log("Agendar Consulta");
    navigate("/schedule-appointment");
  }
</script>

<div class="welcome-panel">
  <h1>Bem-vindo, <span>{userName}</span>!</h1>
  <p>Hoje é um ótimo dia para cuidar da sua saúde e bem-estar.</p>
  <button on:click={goToAppointments}>Agendar Consulta</button>
</div>

<style>
  .welcome-panel {
    flex: 1;
    background-color: #ebebeb;
    border: 1px solid #d3d3d5;
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    margin: 1rem;
    margin-top: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 100%;
  }

  .welcome-panel h1 {
    color: #333;
    font-size: 24px;
  }

  .welcome-panel p {
    color: #666;
    font-size: 16px;
  }
</style>
