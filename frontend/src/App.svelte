<script>
  import { Router, Route, navigate } from "svelte-routing";
  import { onMount } from "svelte";
  import Login from "./Login.svelte";
  import Dashboard from "./Dashboard.svelte";
  import FacialRecognition from "./FacialRecognition.svelte";
  import AboutUs from "./AboutUs.svelte";
  import DoctorLogin from "./DoctorLogin.svelte";
  import DoctorDashboard from "./DoctorDashboard.svelte";
  import Appointments from "./Appointments.svelte";

  onMount(() => {
    document.documentElement.setAttribute("data-theme", "cupcake");
    // Redirect to /login if the current window location is the root
    const path = window.location.pathname;
    if (path === "/" || path === "/index.html") {
      navigate("/login");
    }
  });
</script>

<Router>
  <Route path="/appointmentAdmition" component={FacialRecognition} />
  <Route path="/appointments" component={Appointments} />
  <Route path="/login" component={Login} />
  <Route path="/dashboard" component={Dashboard} />
  <Route path="/about-us" component={AboutUs} />
  <Route path="/doctor-area" component={DoctorLogin} />
  <Route path="/doctor-dashboard/:id" component={DoctorDashboard} />
</Router>
