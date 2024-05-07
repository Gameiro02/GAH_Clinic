<script>
  import Navbar from "./Navbar.svelte";
  import Calendar from "./Calendar.svelte";
  import WelcomePanel from "./WelcomePanel.svelte";
  import ClinicRating from "./ClinicRating.svelte";
  import Pannel from "./Pannel.svelte";
  import { onMount } from "svelte";
  import { appointmentsData } from "./store.js";

  // Fetch appointments data
  async function fetchAppointments() {
    try {
      const tokenString = localStorage.getItem("jwt");
      if (tokenString) {
        const token = JSON.parse(tokenString);
        const response = await fetch(
          "http://localhost:8000/user/appointments/",
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
          data.isLoading = true;
          data.errorMessage = "";
          return data;
        });
      } else {
        throw new Error("No authentication token found. Please login");
      }
    } catch (error) {
      console.error(error.message);
      appointmentsData.update((data) => {
        data.isLoading = true;
        data.errorMessage = error.message;
        return data;
      });
    }
  }

  onMount(fetchAppointments);
</script>

<main>
  <Navbar />
  <div class="welcome">
    <WelcomePanel userName={localStorage.getItem("user")} />
  </div>
  <div class="panels">
    <div>
      <Calendar />
      <ClinicRating averageRating={5} totalRatings={100} />
    </div>
    <Pannel />
  </div>
</main>

<style>
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
</style>
