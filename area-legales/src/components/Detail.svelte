 <script>
    import { cookies, token, userID } from '$store/store'
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
      await Promise.all([
        fetch(URL, { method:"POST", body: setBody("tramiteValido",true,"java.lang.Boolean",caseID) }),
        fetch(URL, { method:"POST", body: setBody("numeroExpediente",true,"java.lang.String",sociedad.numero_expediente) }),
        fetch(URL, { method:"POST", body: setBody("estatuto",true,"java.lang.String","/prueba/prueba") }),
      ])
      await updateTaskState(taskID);
      window.location.replace('/bandejaGeneral')
    }

    async function rechazarSociedad() {
      console.log('Rechazamos!')
      textoCorrecciones = `${textoCorrecciones}. URL de correccion: http://localhost:8000/SA/correciones_area_legales/${sociedad.id}/${caseID}`
      console.log(textoCorrecciones);
      URL = "http://localhost:8000/api/update_variable/";
      await Promise.all([
        fetch(URL, { method:"POST", body: setBody("tramiteValido",false,"java.lang.Boolean",caseID) }),
        fetch(URL, { method:"POST", body: setBody("mensajeMesaInfo",textoCorrecciones,"java.lang.String",caseID) }),
        fetch(URL, { method:"POST", body: setBody("cambiosSugeridos",textoCorrecciones,"java.lang.String",caseID) }),
      ])
      await updateTaskState(taskID)
      window.location.replace('/bandejaGeneral')
    }
</script>

<div>
   {caseID} {taskID}  {JSON.stringify(sociedad)}
    <p> Nombre: {sociedad.nombre} </p>
    <p> Fecha de Emision de Solicitud: {sociedad.fechaCreacion} </p>
    <p> Domicilio Real: {sociedad.domicilioReal} </p>
    <p> Domicilio Leal: {sociedad.domicilioLeal} </p>
    <p> Email Apoderado: {sociedad.emailApoderado} </p>
    <p> Nombre: {sociedad.nombre} </p>
    <p> Nombre: {sociedad.nombre} </p>
    <p> Estatuto: <a href="https://docs.google.com/document/d/"></a> </p>
   <div>
      {#if sociedad.paisesExporta &&  sociedad.paisesExporta.length}
      Paises a los que exporta
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
 
   <div style="margin-top: 20px">
      <button on:click={confirmarSociedad}> Aceptar </button>
      <button style="margin-left: 10px" on:click={() => sociedadRechazada = true}> Rechazar </button>
      {#if sociedadRechazada}
      <div>
        {textoCorrecciones}
        <input type="text" bind:value={textoCorrecciones} /> 
        <button on:click={rechazarSociedad}> Enviar </button>
      </div>
      {/if}
   </div>
   

</div>


