<script>
  import Card from "./Card.svelte";
  import StarIcon from "./StarIcon.svelte";

  let userRating = 0; // Definindo o rating inicial como 0

  function generateStars(clickedIndex) {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      const fill = i <= clickedIndex ? "#FFD700" : "#ccc";
      stars.push({ fill });
    }
    return stars;
  }

  function rateClinic(index) {
    // Definindo o userRating como o índice da estrela clicada
    userRating = index + 1;
    console.log("Estrela clicada:", userRating); // Imprimir o número da estrela clicada
  }
</script>

<Card>
  <div class="message">
    <p>Gostou do serviço? Dê-nos a sua avaliação!</p>
  </div>
  <div class="clinic-rating">
    <div class="stars">
      {#each generateStars(userRating) as { fill }, index}
        <button class="star-button" on:click={() => rateClinic(index)}>
          <StarIcon
            {fill}
            key={index}
            on:mouseover={() => (userRating = index + 1)}
            on:mouseout={() => (userRating = 0)}
          />
        </button>
      {/each}
      <div class="rating-send">
        <span class="clicked-star"></span>
        <p style="margin-right: 1rem;">{userRating}/5</p>
        <button>Enviar</button>
      </div>
    </div>
  </div>
</Card>

<style>
  .clinic-rating {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 16px;
  }

  .stars {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }

  .message {
    text-align: center;
    margin-bottom: 10px;
  }

  .message p {
    font-size: 18px;
    color: #333;
  }

  .clinic-rating {
    text-align: center;
  }

  .stars {
    margin-bottom: 10px;
  }

  .star-button {
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
  }

  .clicked-star {
    font-weight: bold;
    margin-right: 0.1rem;
  }

  .rating-send {
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
