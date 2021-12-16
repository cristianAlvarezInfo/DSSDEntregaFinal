<script>
    import Modal from '$component/ModalV1.svelte';

    export let selectedModal = -1;
    export let sociedad = {};

    function closeModal(){ 
        selectedModal = -1;
      }
</script>

<Modal class="modal-width">
    <div class="inline-end">
      <span on:click={closeModal}>X</span> 
    </div>
    <div class="column-container">
      <div class="column-container" style="margin-top: 10px">
        <span class="modal-title">Nombre de la Sociedad</span>
        <span class="modal-text" style="padding-top: 8px">{ sociedad.data.nombre }</span>                         
      </div>
      <div class="column-container" style="margin-top: 20px">
        <span class="modal-title">Domicilio legal</span>
        <span class="modal-text" style="padding-top: 8px">{ sociedad.data.domicilioLegal }</span>
      </div>
      <div class="column-container" style="margin-top: 20px">
        <span class="modal-title">Domicilio real</span>
        <span class="modal-text" style="padding-top: 8px">{ sociedad.data.domicilioReal }</span>
      </div>
      <div class="column-container" style="margin-top: 20px">
        <span class="modal-title">Estatuto</span>
        <a href={`http://localhost:8000/pdf_viewer/${sociedad.data.id}/`} target="_blank">Ver Estatuto</a>
      </div>
      <div class="column-container" style="margin-top: 20px">
        <span class="modal-title">Datos del apoderado </span>
        <span class="modal-text" style="padding-top: 8px"><strong>Nombre:</strong> { sociedad.data.apoderado.nombre }</span>
        <span class="modal-text" style="padding-top: 8px"><strong>Apellido:</strong> { sociedad.data.apoderado.apellido }</span>
        <span class="modal-text" style="padding-top: 8px"><strong>Email:</strong> { sociedad.data.emailApoderado}</span>
        <span class="modal-text" style="padding-top: 8px"><strong>Porcentaje Aportes:</strong> { sociedad.data.apoderado.porcentajeAportesRealizados }%</span>
      </div>

      <div class="column-container" style="margin-top: 20px">
        <span class="modal-title">Datos de Socios </span>
        {#each sociedad.data.socios as socio}
          <div class="column-container" >
            <span class="modal-text" style="padding-top: 8px"><strong>Nombre:</strong> { socio.nombre }</span>
            <span class="modal-text" style="padding-top: 8px"><strong>Apellido:</strong> { socio.apellido }</span>
            <span class="modal-text" style="padding-top: 8px"><strong>Porcentaje Aportes:</strong> { socio.porcentaje_aporte }%</span>
          </div>  
          <hr>
        {/each}
      </div>

      <div>
        {#if sociedad.data.paisesExporta &&  sociedad.data.paisesExporta.length}
        <span class="modal-title">Paises a los que exporta</span>
        <ul>
        {#each sociedad.data.paisesExporta as paisExporta}
            <li>IATA: {paisExporta.codigo_gql}</li> 
            <ul>
            {#each sociedad.data.estadosExporta as estadoExporta}
                {#if estadoExporta.pais_gql == paisExporta.codigo_gql}
                <li> { estadoExporta.nombre_gql } </li>
                {/if}
            {/each}
            </ul>
        {/each}
        </ul>
        {/if}
     </div>
    </div>
  </Modal>

  


  
<style>
    .inline-container {
      display: flex;
      flex-direction: row;
    }
    .column-container {
      display: flex;
      flex-direction: column;
    }
    .container-table{
      display: flex;
      justify-content: center;
    }
    *{
      font-family: Arial, Helvetica, sans-serif;
    }
    td{
      width: 200px;
    }
    tr{
      height: 70px;
    }
    .inline-end {
      display: flex;
      justify-content: end;
    }
    .modal-title {
      font-weight: 700;
      font-size: 20px;
    }
    .modal-text{
      font-size: 13;
    }
    .option-btn {
      width: 100px;
      height: 30px;
      color: white;
      padding-top: 10px;
      border-radius: 6px;
      text-align: center;
    }
    .btn-apropiarse {
      background-color: green;
    }
    .btn-detalle {
      background-color: blue;
    }
  
  </style>
  