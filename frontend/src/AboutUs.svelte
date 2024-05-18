<script>
  import Navbar from "./Navbar.svelte";
  import { theme } from "./store.js";

  $: themeColor = $theme;
</script>

<Navbar />
<div
  class="flex flex-col items-center justify-center bg-base-100 ${themeColor === 'dark'
    ? 'shadow-white'
    : 'shadow-black'} overflow-hidden h-screen"
>
  <div class="w-full max-w-4xl flex flex-col items-center h-full">
    <div class="card w-full bg-base-200 shadow-lg rounded-lg overflow-hidden h-[80vh] lg:h-[80vh] mt-4 lg:mt-0">
      <div class="card-body flex flex-col lg:flex-row p-6 h-full">
        <div class="about-us flex-1 pr-0 lg:pr-4 overflow-auto">
          <h2 class="card-title text-secondary text-4xl pb-4 mb-4">Sobre Nós</h2>
          <p class="text-lg leading-relaxed mb-4 text-justify text-base-content">
            Somos uma clínica de bem-estar e fisioterapia dedicada a proporcionar o melhor cuidado para nossos
            pacientes.
          </p>
          <p class="text-lg leading-relaxed mb-1 text-justify text-base-content">
            Conheça nossas especialidades e o nosso corpo clinico:
          </p>
          <div class="collapse collapse-arrow bg-base-200">
            <input type="radio" name="my-accordion-2" checked="checked" />
            <div class="collapse-title text-xl font-medium text-secondary">Massagem</div>
            <div class="collapse-content">
              <p class="text-base-content text-justify">
                As nossas massagens terapêuticas são projetadas para aliviar a tensão muscular, melhorar a circulação
                sanguínea e promover o relaxamento.
              </p>
            </div>
          </div>
          <div class="collapse collapse-arrow bg-base-200">
            <input type="radio" name="my-accordion-2" />
            <div class="collapse-title text-xl font-medium text-secondary">Fisioterapia</div>
            <div class="collapse-content">
              <p class="text-base-content text-justify">
                Oferecemos tratamentos de fisioterapia personalizados para ajudar na recuperação de lesões, melhorar a
                mobilidade e fortalecer a musculatura.
              </p>
            </div>
          </div>
          <div class="collapse collapse-arrow bg-base-200">
            <input type="radio" name="my-accordion-2" />
            <div class="collapse-title text-xl font-medium text-secondary">Psicologia</div>
            <div class="collapse-content">
              <p class="text-base-content text-justify">
                Os nossos psicólogos estão aqui para tratar sua saúde mental, oferecendo terapia para lidar com o
                stress, ansiedade, depressão e outros desafios emocionais.
              </p>
            </div>
          </div>
          <div class="collapse collapse-arrow bg-base-200">
            <input type="radio" name="my-accordion-2" />
            <div class="collapse-title text-xl font-medium text-secondary">Ortopedia</div>
            <div class="collapse-content">
              <p class="text-base-content text-justify">
                A nossa equipa de ortopedia trata uma variedade de condições músculares e esqueléticas, proporcionando
                cuidados abrangentes para ossos, articulações e músculos.
              </p>
            </div>
          </div>
        </div>
        <div class="w-full lg:w-1/3 pt-4 lg:pt-0 lg:pl-4 flex items-stretch">
          <div class="carousel rounded-box shadow-md w-full h-64 lg:h-full">
            <div class="carousel-item w-full h-full">
              <img
                src="https://img.daisyui.com/images/stock/photo-1559703248-dcaaec9fab78.jpg"
                class="w-full h-full object-cover"
                alt="Carrossel de Imagens"
              />
            </div>
            <div class="carousel-item w-full h-full">
              <img
                src="https://img.daisyui.com/images/stock/photo-1565098772267-60af42b81ef2.jpg"
                class="w-full h-full object-cover"
                alt="Carrossel de Imagens"
              />
            </div>
            <div class="carousel-item w-full h-full">
              <img
                src="https://img.daisyui.com/images/stock/photo-1572635148818-ef6fd45eb394.jpg"
                class="w-full h-full object-cover"
                alt="Carrossel de Imagens"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
