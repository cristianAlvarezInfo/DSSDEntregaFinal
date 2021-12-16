<script>
    import DetailModalBandejaInterna from '$component/DetailModalBandejaInterna.svelte';
    import { cookies, token, userID } from '$store/store';
    $: segments = [];
    
    async function getTasks() {
      const formData = new FormData();
      formData.append("cookies", $cookies);
      formData.append("token", $token);
      formData.append("task_name", 'Evaluacion de tramite');
      const opts = {
        method: 'POST',
        body: formData
      }
      const URL = "http://localhost:8000/api/get_sociedades_anonimas_by_task_name/";
      let response = await fetch(URL, { method: 'POST',body: formData });
      response = await response.json();
      if (!response.ok) { return }
      console.log(response);
      segments = response.data.filter(e => e.assigned_id == $userID) 
      return Promise.resolve();
    };
    const eliminarSociedadApropiada = (taskID) => {
        segments = segments.filter(e => {
            e.task_id != taskID
        })
    }

    const openedDetails = []
    function closeModal(){ 
        selectedModal = -1;
      }
    let selectedModal = -1;
    
</script>

<div>
    {#await getTasks() }
        Trayendo sociedad anonimas. Espere :)
    {:then}
        {#if segments && segments.length}
        <div class="container-table">
          <table>
            <thead>
              <td>Nombre Sociedad</td>
              <td>Email Apoderado</td>
              <td>Fecha de pedido</td>
              <td>Domicilio legal</td>
              <td>Domicilio Real</td>
              <td>Estatuto</td>
              <td>Opciones</td>
            </thead>
            <tbody>
              {#each segments as sociedad, i}
               
                <tr>
                  <td>{ sociedad.data.nombre }</td>
                  <td>{ sociedad.data.emailApoderado }</td>
                  <td>{ sociedad.data.fechaCreacion }</td>
                  <td>{ sociedad.data.domicilioLegal }</td>
                  <td>{ sociedad.data.domicilioReal }</td>
                  <td><a href={`http://localhost:8000/pdf_viewer/${sociedad.data.id}/`} target="_blank">Ver Estatuto</a></td>
                  <td>
                    <div class="inline-container">                      
                      <div class="option-btn btn-detalle" on:click={() => selectedModal = i}> Detalle </div>
                      {#if selectedModal == i}
                        <DetailModalBandejaInterna {sociedad} bind:selectedModal={selectedModal} />
                      {/if}
                    </div>
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
        {:else}
        <div>
            No hay tareas pendientes
        </div> 
        {/if}
    {/await}
</div>



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
    .btn-Aceptar {
      background-color: green;
    }
    .btn-Rechazar {
      background-color: red;
    }
    .btn-detalle {
      background-color: blue;
    }
  
  </style>