<script>
  import Navbar from "./Navbar.svelte";
  import WelcomePanel from "./WelcomePanel.svelte";
  import Empty from "./Cards/BookAppointment.svelte";
  import AppointmentsPanel from "./Cards/AppointmentsPanel.svelte";
  import BookAppointment from "./Cards/BookAppointment.svelte";
  import HistoryPanel from "./Cards/HistoryPanel.svelte";
  import { onMount } from "svelte";
  import { appointmentsData } from "./store.js";

  // Fetch appointments data
  async function fetchAppointments() {
    try {
      const tokenString = localStorage.getItem("jwt");
      if (tokenString) {
        const token = JSON.parse(tokenString);
        const response = await fetch(
          "http://gah-clinic.us-east-1.elasticbeanstalk.com/user/appointments/",
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

<main class="container mx-auto p-4">
  <Navbar />
  <div class="flex flex-col space-y-5">
    <div class="welcome">
      <WelcomePanel userName={localStorage.getItem("user")} />
    </div>
    <div class="flex flex-col md:flex-row space-y-5 md:space-y-0 md:space-x-5">
      <!-- <div>
          <Calendar />
          <ClinicRating averageRating={5} totalRatings={100} />
        </div> -->
      <AppointmentsPanel />
      <BookAppointment />
      <HistoryPanel />
    </div>
  </div>
</main>

<!-- <style>
  .welcome {
    display: flex;
    justify-content: center; /* Center the panel horizontally */
    margin-top: 10px;
  }

  .panels {
    display: flex;
    justify-content: center; /* Center the panels horizontally */
    margin-top: 10px;
  }

  .panels > div {
    margin: 0 10px; /* Add margin between panels if needed */
  }

  @media (max-width: 768px) {
    .panels {
      flex-direction: column; /* Change to column layout on small screens */
    }

    .panels > div {
      margin: 10px 0; /* Add margin between panels if needed */
    }
  }
</style> -->
