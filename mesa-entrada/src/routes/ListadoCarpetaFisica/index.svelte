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


    const exportToPdf = async (sociedad) => {
        const template = `
            <h1> Nombre {{nombre}} </h1>
            <h1> Fecha Creacion {{fecha_creacion}} </h1>
            <h1> Domicilio real {{domicilio_real}} </h1>
            <h1> Domicilio lgeal {{domicilio_legal}} </h1>
            <h1> Apoderado {{nombre_apoderado}} </h1>
        `
        const context = {
            nombre: sociedad.nombre,
            fecha_creacion: sociedad.fechaCreacion,
            domicilio_real: sociedad.domicilioReal,
            domicilio_legal: sociedad.domicilioLegal,
            email_apoderado: sociedad.emailApoderado,
        }
        const compiledTemplate = Handlebars.compile(template)(context);
        const fileName = `./${sociedad.nombre}${sociedad.fechaCreacion}.pdf`
        const opts = {
           method: "POST",
           body: JSON.stringify({ filename: filename, content: compiledTemplate, idSociedad: sociedad.id })
        }
        await Promise.all([
            fetch('http://localhost:8000/api/save_carpeta_fisica/', opts);
            // updateTaskState(sociedad.task_id);
        ])
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
            <li style="margin-left: 10px"><button on:click={ exportToPdf(sociedad.data) }>Generar carpeta fisica</button></li>
        {/each}
        </ul>
        {:else}
        <div v-else>
            No hay tareas pendientes
        </div> 
        {/if}
    {/await}
</div>
