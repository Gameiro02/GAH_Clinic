<script>
  import { onMount } from "svelte";
  import WelcomePanel from "./WelcomePanel.svelte";
  import Navbar from "./Navbar.svelte";
  import DoctorAppointments from "./Cards/DoctorAppointments.svelte";
  import DoctorHistoryPanel from "./Cards/DoctorHistoryPanel.svelte";
  import { doctorsAppointments } from "./store";
  import { DOMAIN } from "./config.js";

  let selectedDoctor = null;
  const doctors = [
    { id: 1, name: "Pedro Pais" },
    { id: 2, name: "Afonso Mora" },
    { id: 3, name: "Mariana Filho" },
    { id: 4, name: "Carlos Sousa" },
  ];

  async function fetchAppointments(doctorId) {
    try {
      const tokenString = localStorage.getItem("jwt");
      if (!tokenString) {
        throw new Error("No authentication token found. Please login");
      }

      const token = JSON.parse(tokenString);
      const response = await fetch(
        `${DOMAIN}/doctors/${doctorId}/appointments/`,
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
        } else if (response.status === 404) {
          throw new Error("Doctor not found");
        }
        throw new Error("Failed to fetch appointments");
      }

      const result = await response.json();
      if (result.status !== "success" || !Array.isArray(result.appointments)) {
        throw new Error(
          "Data format error: Expected an array of appointments."
        );
      }

      doctorsAppointments.update((data) => {
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
    } catch (error) {
      console.error(error.message);
      doctorsAppointments.update((data) => {
        data.isLoading = false;
        data.errorMessage = error.message;
        return data;
      });
    }
  }

  onMount(() => {
    // Get the id from the last digit of the URL
    const url = window.location.href;
    const id = url.substring(url.lastIndexOf("/") + 1);

    // Get the doctor object from the id
    selectedDoctor = doctors.find((doctor) => doctor.id == id);

    fetchAppointments(id);

    // Handle case where doctor is not found
    if (!selectedDoctor) {
      selectedDoctor = { name: "Unknown Doctor" };
    }
  });
</script>

<main class="flex flex-col mx-auto w-screen h-screen px-6 pt2 pb-6">
  <Navbar />
  <div class="flex flex-col flex-grow space-y-5">
    <div class="welcome">
      <WelcomePanel
        userRole={"doctor"}
        userName={selectedDoctor ? selectedDoctor.name : "Loading..."}
      />
    </div>
    <div
      class="flex flex-col flex-grow md:flex-row space-y-5 md:space-y-0 md:space-x-5"
    >
      <DoctorHistoryPanel />
      <DoctorAppointments />
    </div>
  </div>
</main>
