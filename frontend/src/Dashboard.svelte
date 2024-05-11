<script>
  import Navbar from "./Navbar.svelte";
  import WelcomePanel from "./WelcomePanel.svelte";
  import AppointmentsPanel from "./Cards/AppointmentsPanel.svelte";
  import HistoryPanel from "./Cards/HistoryPanel.svelte";
  import { onMount } from "svelte";
  import { appointmentsData } from "./store.js";
  import { DOMAIN } from "./config.js";

  // Fetch appointments data
  async function fetchAppointments() {
    try {
      const tokenString = localStorage.getItem("jwt");
      if (tokenString) {
        const token = JSON.parse(tokenString);
        const response = await fetch(
          `${DOMAIN}/user/appointments/`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        if (!response.ok) {
          if (response.status === 401) {
            throw new Error("Authorization failed. Please login again");
          } else if (response.status === 500) {
            throw new Error("Server error. Please try again later");
          }
          throw new Error("Failed to fetch appointments");
        }

        const result = await response.json();
        if (
          result.status !== "success" ||
          !Array.isArray(result.appointments)
        ) {
          throw new Error(
            "Data format error: Expected an array of appointments."
          );
        }

        appointmentsData.update((data) => {
          data.upcomingAppointments = result.appointments.filter(
            (app) => app.status !== "finished"
          );
          data.pastAppointments = result.appointments.filter(
            (app) => app.status === "finished"
          );
          data.missingPaymentAppointments = result.appointments.filter(
            (app) => app.status === "waiting for payment"
          );
          data.isLoading = false;
          data.errorMessage = "";
          return data;
        });
      } else {
        throw new Error("No authentication token found. Please login");
      }
    } catch (error) {
      console.error(error.message);
      appointmentsData.update((data) => {
        data.isLoading = false;
        data.errorMessage = error.message;
        return data;
      });
    }
  }

  onMount(fetchAppointments);
</script>

<main class="flex flex-col mx-auto w-screen h-screen px-6 pt2 pb-6">
  <Navbar />
  <div class="flex flex-col flex-grow space-y-5">
    <div class="welcome">
      <WelcomePanel userName={localStorage.getItem("user")} />
    </div>
    <div class="flex flex-col flex-grow md:flex-row space-y-5 md:space-y-0 md:space-x-5">
      <HistoryPanel />
      <AppointmentsPanel />
    </div>
  </div>
</main>