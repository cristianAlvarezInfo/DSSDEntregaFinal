<script>
    import DetailModal from '$component/DetailModal.svelte';
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
      let response = await fetch(URL, { method: 'POST', body: formData });
      response = await response.json();
      if (!response.ok) { return }
      console.log(response);
      segments = response.data.filter(e => e.assigned_id == "") 
      return Promise.resolve();
    };

    const eliminarSociedadApropiada = (taskID) => {
        segments = segments.filter(e => {
            e.task_id != taskID
        })
    }

    async function apropiarse(taskID) {
      eliminarSociedadApropiada(taskID)
      const formData = new FormData();
      formData.append("cookies", $cookies);
      formData.append("token", $token);
      formData.append("user_id", $userID);
      formData.append("task_id", taskID);
      const opts = {
        method: "POST",
        body: formData
      };
      const URL = 'http://localhost:8000/api/assign_task_to_user/';
      let response = await fetch(URL, opts);
      response = await response.json();
    }

    
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
                    <div class="option-btn btn-apropiarse" style="margin-right: 10px" on:click={ apropiarse(sociedad.task_id) }> Apropiarse </div>
                    <div class="option-btn btn-detalle" on:click={() => selectedModal = i}> Detalle </div>
                    {#if selectedModal == i}
                      <DetailModal {sociedad} bind:selectedModal={selectedModal} />
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
  .btn-apropiarse {
    background-color: green;
  }
  .btn-detalle {
    background-color: blue;
  }

</style>



<!--
  <div>
    {#await getTasks() }
        Trayendo sociedad anonimas. Espere :)
    {:then}
        {#if segments && segments.length}
        <ul style="display: flex; flex-direction: column;  list-style:none;">
        {#each segments as sociedad}
                <br>
                <li> { sociedad.data.nombre } </li>
                <li style="margin-left: 10px"> { sociedad.data.emailApoderado } </li>
                <li style="margin-left: 10px"><button on:click={ apropiarse(sociedad.task_id) }>Apropiarse</button></li>
        {/each}
        </ul>
        {:else}
        <div v-else>
            No hay tareas pendientes
        </div> 
        {/if}
    {/await}
</div>
-->

