<script>
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

    const eliminarSociedadApropiada = (taskID) => {
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
        await updateTaskState(sociedad.task_id)
    }
</script>

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
