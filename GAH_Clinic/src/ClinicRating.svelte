<script>
  import Card from "./Card.svelte";
  import StarIcon from "./StarIcon.svelte";

  export let averageRating;
  export let totalRatings;

  function calculatePercentage() {
    if (totalRatings === 0) return 0;
    return (averageRating / 5) * 100;
  }

  function generateStars() {
    const stars = [];
    const roundedRating = Math.round(averageRating);
    for (let i = 1; i <= 5; i++) {
      stars.push(i <= roundedRating ? { fill: "#FFD700" } : { fill: "#ccc" });
    }
    return stars;
  }
</script>

<Card>
  <div class="clinic-rating">
    <div class="stars">
      {#each generateStars() as { fill }, index}
        <StarIcon {fill} key={index} />
      {/each}
    </div>
    <span class="average">{averageRating.toFixed(1)}</span>
    <span class="total">({totalRatings} avaliações)</span>
  </div>
</Card>

<style>
  .clinic-rating {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
  }

  .stars {
    display: flex;
    align-items: center;
    margin-right: 10px;
  }

  .average {
    font-weight: bold;
  }

  .total {
    color: #666;
  }
</style>
