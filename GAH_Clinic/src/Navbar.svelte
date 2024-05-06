<script>
  import logo from "../public/logo.svg";

  // Função para fazer logout, se necessário
  function handleLogout() {
    // Implemente a lógica de logout aqui
    console.log("Usuário deslogado");
    // Redirecionar para a página de login
  }

  function handleDashboardClick() {
    // Implemente a lógica de redirecionamento para o Dashboard
    console.log("Redirecionando para o Dashboard");
  }
  function handleAppointmentsClick() {
    // Implemente a lógica de redirecionamento para as consultas
    console.log("Redirecionando para as consultas");
  }

  function handlePaymentsClick() {
    // Implemente a lógica de redirecionamento para os pagamentos
    console.log("Redirecionando para os pagamentos");
  }

  function handleSupportClick() {
    // Implemente a lógica de redirecionamento para o suporte
    console.log("Redirecionando para o suporte");
  }

  function handleSettingsClick() {
    // Implemente a lógica de redirecionamento para as configurações
    console.log("Redirecionando para as configurações");
  }
</script>

<nav class="navbar">
  <div class="logo">
    <img src={logo} alt="GAH Logo" class="logo-img" />
  </div>
  <div class="menu">
    <a href="/" on:click={(event) => handleDashboardClick(event)}>Dashboard</a>
    <a href="/" on:click={(event) => handleAppointmentsClick(event)}
      >Minhas Consultas</a
    >
    <!-- <a href="/" on:click={(event) => handlePaymentsClick(event)}>Pagamentos</a> -->
    <a href="/" on:click={(event) => handleSupportClick(event)}>Suporte</a>
    <a href="/" on:click={(event) => handleSettingsClick(event)}
      >Configurações</a
    >
    <button on:click={(event) => handleLogout(event)}>Logout</button>
  </div>
</nav>

<style>
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #7fb1b3;
    color: #333;
    padding: 0.5rem 1rem;
    font-family: sans-serif;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    height: 60px;
  }

  .logo-img {
    display: block;
    width: 60px; /* Reduz a largura para 80px */
    height: 63px; /* Mantém a proporção da imagem */
  }

  .navbar .menu a,
  .navbar .menu button {
    color: white;
    text-decoration: none;
    margin-left: 1rem;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1rem;
    padding: 0.5rem;
    border-radius: 5px; /* Alinhado com a estética do botão do calendário */
  }

  .navbar .menu button {
    font-size: 1rem;
    padding: 0.5rem 1rem;
  }

  .navbar .menu a:hover,
  .navbar .menu button:hover {
    background-color: #666; /* Um leve escurecimento no hover */
  }
</style>
