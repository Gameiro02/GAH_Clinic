<script>
  import Calendar from "./Calendar.svelte";
  // Props passada para o componente, por exemplo, ao usar <WelcomePanel userName="João" />
  export let userName;

  // Função para navegar para a página de agendamento
  function goToAppointments() {
    console.log("Redirecionando para a página de agendamento");
  }
</script>

<div class="welcome-panel">
  <h1>Bem-vindo, <span>{userName}</span>!</h1>
  <p>Hoje é um ótimo dia para cuidar da sua saúde e bem-estar.</p>
  <button on:click={goToAppointments}>Agendar Consulta</button>
</div>

<style>
  .welcome-panel {
    background-color: #ebebeb;
    border: 1px solid #d3d3d5;
    border-radius: 5px;
    padding: 20px;
    text-align: center;
    padding: 25px 25px;
    margin: 15px;
    margin-top: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    max-width: 1380px;
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
