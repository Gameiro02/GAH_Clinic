<script>
  import Login from "./Login.svelte";
  import ScheduleAppointment from "./ScheduleAppointment.svelte";
  import Payment from "./Payment.svelte";
  import Navbar from "./Navbar.svelte";
  import Calendar from "./Calendar.svelte";
  import WelcomePanel from "./WelcomePanel.svelte";
  import ClinicRating from "./ClinicRating.svelte";
  import AppointmentsPanel from "./AppointmentsPanel.svelte";
  import HistoryPanel from "./HistoryPanel.svelte";
</script>

<main>
  <Navbar />
  <WelcomePanel userName="Gameiro" />

  <div class="panels">
    <div>
      <ClinicRating averageRating={5} totalRatings={100} />
      <Calendar />
    </div>
    <AppointmentsPanel />
    <HistoryPanel />
  </div>
</main>

<style>
  .panels {
    display: flex;
  }
</style>
