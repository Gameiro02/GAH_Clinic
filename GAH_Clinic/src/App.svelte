<script>
  import Login from "./Login.svelte";
  import ScheduleAppointment from "./ScheduleAppointment.svelte";
  import Payment from "./Payment.svelte";
  import Navbar from "./Navbar.svelte";
  import Calendar from "./Calendar.svelte";
  import WelcomePanel from "./WelcomePanel.svelte";
  import ClinicRating from "./ClinicRating.svelte";
</script>

<main>
  <Navbar />
  <WelcomePanel userName="Gameiro" />
  <ClinicRating averageRating={5} totalRatings={100} />
  <Calendar />
</main>
