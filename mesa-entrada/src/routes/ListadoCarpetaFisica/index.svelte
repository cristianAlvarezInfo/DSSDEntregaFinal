<script>
    import  DetailModal  from '$component/DetailModal.svelte';
    import Handlebars from 'handlebars';
    import pdf from 'html-pdf';
    import path from 'path'

    import { cookies, token, userID } from '$store/store';
    $: segments = [];

    async function updateTaskState(taskID){
      const formData = new FormData();
      formData.append("cookies", $cookies);
      formData.append("token", $token);
      formData.append("user_id", $userID);
      formData.append("new_state", "completed");
      formData.append("task_id", taskID);
      const opts = {
        method: "POST",
        body: formData
      }
      URL = 'http://localhost:8000/api/change_task_state/'
      await fetch(URL, opts)
    }


    async function getTasks() {
      const formData = new FormData();
      formData.append("cookies", $cookies);
      formData.append("token", $token);
      formData.append("task_name", 'Generación  Carpeta fisica');
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

    const eliminarSociedadCarpeta = (taskID) => {
        segments = segments.filter(e => {
            e.task_id != taskID
        })
    }
    function setBody(variableName, valueVariable, typeVariable, caseID) {
      const formData = new FormData();
      formData.append("cookies", $cookies);
      formData.append("token", $token);
      formData.append("variable_name", variableName);
      formData.append("value_variable", valueVariable);
      formData.append("type_variable", typeVariable);
      formData.append("case_id", caseID);
      return formData;
    }


    const exportToPdf = async (sociedad) => {
        eliminarSociedadCarpeta(sociedad.task_id);

        const template = `
            Nombre {{nombre}} 
            Fecha Creacion {{fecha_creacion}} 
            Domicilio real {{domicilio_real}} 
            Domicilio lgeal {{domicilio_legal}} 
            Apoderado {{nombre_apoderado}} 
            Numero expediente {{num_expediente}}
        `
        const context = {
            nombre: sociedad.data.nombre,
            fecha_creacion: sociedad.data.fechaCreacion,
            domicilio_real: sociedad.data.domicilioReal,
            domicilio_legal: sociedad.data.domicilioLegal,
            email_apoderado: sociedad.data.emailApoderado,
            num_expediente: sociedad.data.numero_expediente,
        }
        const compiledTemplate = Handlebars.compile(template)(context);
        const fileName = `${sociedad.data.nombre}${sociedad.data.fechaCreacion}.pdf`
        const opts = {
           method: "POST",
           body: JSON.stringify({ filename: fileName, content: compiledTemplate, idSociedad: sociedad.data.id })
        }
        
        const URL = "http://localhost:8000/api/update_variable/";
        const email = `Ya esta lista la carpeta fisica para retirar. Numero de expediente: ${sociedad.data.numero_expediente}`
        
        await fetch('http://localhost:8000/api/save_carpeta_fisica/', opts)
        await fetch(URL, { method:"POST", body: setBody("mensajeMesaInfo",email,"java.lang.String",sociedad.case_id) })
        await updateTaskState(sociedad.task_id);

    }

    function dropSociedadCarpeta(sociedad){
        return segments.filter(e => e.data.id == sociedad.data.id);
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
                      <div class="option-btn btn-apropiarse" style="margin-right: 10px" on:click={ exportToPdf(sociedad) }> 
                          Generar carpeta fisica 
                      </div>
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

<!--
<div>
    {#await getTasks() }
        Trayendo sociedad anonimas. Espere :)
    {:then}
        {#if segments && segments.length}
        <ul style="display: flex; flex-direction: column;  list-style:none;">
        {#each segments as sociedad}
            {JSON.stringify(sociedad)}
            <br>
            <li> { sociedad.data.nombre } </li>
            <li style="margin-left: 10px"> { sociedad.data.emailApoderado } </li>
            <li style="margin-left: 10px"><button on:click={ exportToPdf(sociedad) }>Generar carpeta fisica</button></li>
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
      font-size: 11px !important;
      background-color: green;
    }
    .btn-detalle {
      background-color: blue;
    }
  
  </style>
  
