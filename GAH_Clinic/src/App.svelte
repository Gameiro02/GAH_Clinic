<script>
  import { Router, Route, Link, navigate } from 'svelte-routing';
  import { onMount } from 'svelte';
  import Login from './Login.svelte';
  import Dashboard from './Dashboard.svelte';
  import WelcomePanel from './WelcomePanel.svelte';
  import ScheduleAppointment from './ScheduleAppointment.svelte';

  onMount(() => {
    // Redirect to /login if the current window location is the root
    const path = window.location.pathname;
    if (path === '/' || path === '/index.html') {
      navigate('/login');
    }
  });
</script>

<Router>
  <nav>
    <!-- Navigation can be added here if needed -->
  </nav>
  <Route path="/login" component={Login} />
  <Route path="/dashboard" component={Dashboard} />
  <Route path="/schedule-appointment" component={ScheduleAppointment} />
</Router>
