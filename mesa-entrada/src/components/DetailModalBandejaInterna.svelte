<script>
    import Modal from '$component/ModalV1.svelte';
    import { cookies,token,userID,idProcess,isLoggedUser } from '$store/store' 

    export let selectedModal = -1;
    export let sociedad = {};

    const caseID = sociedad.case_id;
    const taskID = sociedad.task_id;
    sociedad = sociedad.data;
    
    let textoCorrecciones;
    let inputFechaLimiteCorreccion;
    let sociedadRechazada = false;
    $: fechaLimiteCorreccion = inputFechaLimiteCorreccion && formatDate();

    function formatDate() {
      const actualDate = new Date(inputFechaLimiteCorreccion);
      actualDate.setDate(actualDate.getDate() + 1);
      let day = actualDate.getDate();
      let month = actualDate.getMonth();

      const year = actualDate.getFullYear().toString();
      console.log(month);
      month = (month + 1 == 13) ? '01' : (month + 1).toString();
      day = day < 10 ? `0${day}` : day.toString();

      return `${day}-${month}-${year}`;
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

    async function updateTaskState(){
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

    async function confirmarSociedad() {      
      URL = "http://localhost:8000/api/update_variable/";
      const texto = "El tramite fue aprobado por mesa de entradas. Ahora sera enviado al area de legales"
      await Promise.all([
        fetch(URL, { method:"POST", body: setBody("informacionAprobada",true,"java.lang.Boolean",caseID) }),
        fetch(URL, { method:"POST", body: setBody("emailApoderado",sociedad.emailApoderado,"java.lang.String",caseID) }),
        fetch(URL, { method:"POST", body: setBody("mensajeMesaInfo",texto,"java.lang.String",caseID) }),
        fetch(URL, { method:"POST", body: setBody("id_pedido",parseInt(sociedad.id),"java.lang.Integer",caseID) }),
      ])
      await updateTaskState();
      window.location.replace('/bandejaGeneral')
    }

    async function rechazarSociedad() {
      textoCorrecciones = `${textoCorrecciones}. URL de correccion: http://localhost:8000/SA/correciones_mesa_entrada/${sociedad.id}/${fechaLimiteCorreccion}/${caseID}`
      console.log(textoCorrecciones);
      URL = "http://localhost:8000/api/update_variable/";
      await Promise.all([
        fetch(URL, { method:"POST", body: setBody("informacionAprobada",false,"java.lang.Boolean",caseID) }),
        fetch(URL, { method:"POST", body: setBody("emailApoderado",sociedad.emailApoderado,"java.lang.String",caseID) }),
        fetch(URL, { method:"POST", body: setBody("vencimientoCorreccion",fechaLimiteCorreccion,"java.lang.String",caseID) }),
        fetch(URL, { method:"POST", body: setBody("mensajeMesaInfo",textoCorrecciones,"java.lang.String",caseID) }),
        fetch(URL, { method:"POST", body: setBody("id_pedido",parseInt(sociedad.id),"java.lang.Integer",caseID) }),
      ])
      await updateTaskState()
      window.location.replace('/bandejaGeneral')
    }

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
        <span class="modal-text" style="padding-top: 8px">{ sociedad.nombre }</span>                         
      </div>
      <div class="column-container" style="margin-top: 20px">
        <span class="modal-title">Domicilio legal</span>
        <span class="modal-text" style="padding-top: 8px">{ sociedad.domicilioLegal }</span>
      </div>
      <div class="column-container" style="margin-top: 20px">
        <span class="modal-title">Domicilio real</span>
        <span class="modal-text" style="padding-top: 8px">{ sociedad.domicilioReal }</span>
      </div>
      <div class="column-container" style="margin-top: 20px">
        <span class="modal-title">Estatuto</span>
        <a href={`http://localhost:8000/pdf_viewer/${sociedad.id}/`} target="_blank">Ver Estatuto</a>
      </div>
      <div class="column-container" style="margin-top: 20px">
        <span class="modal-title">Datos del apoderado </span>
        <span class="modal-text" style="padding-top: 8px"><strong>Nombre:</strong> { sociedad.apoderado.nombre }</span>
        <span class="modal-text" style="padding-top: 8px"><strong>Apellido:</strong> { sociedad.apoderado.apellido }</span>
        <span class="modal-text" style="padding-top: 8px"><strong>Email:</strong> { sociedad.emailApoderado}</span>
        <span class="modal-text" style="padding-top: 8px"><strong>Porcentaje Aportes:</strong> { sociedad.apoderado.porcentajeAportesRealizados }%</span>
      </div>

      <div class="column-container" style="margin-top: 20px">
        <span class="modal-title">Datos de Socios </span>
        {#each sociedad.socios as socio}
          <div class="column-container" >
            <span class="modal-text" style="padding-top: 8px"><strong>Nombre:</strong> { socio.nombre }</span>
            <span class="modal-text" style="padding-top: 8px"><strong>Apellido:</strong> { socio.apellido }</span>
            <span class="modal-text" style="padding-top: 8px"><strong>Porcentaje Aportes:</strong> { socio.porcentaje_aporte }%</span>
          </div>  
          <hr>
        {/each}
      </div>

      <div>
        {#if sociedad.paisesExporta &&  sociedad.paisesExporta.length}
        <span class="modal-title">Paises a los que exporta</span>
        <ul>
        {#each sociedad.paisesExporta as paisExporta}
            <li>IATA: {paisExporta.codigo_gql}</li> 
            <ul>
            {#each sociedad.estadosExporta as estadoExporta}
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
    <div style="margin-top: 20px">
      <div class="inline-container">
          <div class="option-btn btn-Aceptar" on:click={confirmarSociedad}> Aceptar </div>
          <div class="option-btn btn-Rechazar" style="margin-left: 10px" on:click={() => sociedadRechazada = true}> Rechazar </div>          
      </div>
      {#if sociedadRechazada}
      <div class="column-container" style="align-items:center; margin-top: 20px">
         <span class="modal-titles"> Correcciones </span>
         <input type="text" style="margin-top: 5px; width: 40%; height: 50px" bind:value={textoCorrecciones} /> 
         <input type="date" style="margin-top: 5px; width: 40%" bind:value={inputFechaLimiteCorreccion} />
         <div class="option-btn btn-Enviar" style="margin-top: 5px; width: 40%" on:click={rechazarSociedad}> Enviar </div>
      </div>
      {/if}
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
      padding-top: 8px;
      border-radius: 6px;
      text-align: center;
    }
    .btn-Aceptar {
      background-color: green;
    }
    .btn-Rechazar {
      background-color: red;
    }
    
    .btn-Enviar {
      background-color: blue;
    }


  </style>
  