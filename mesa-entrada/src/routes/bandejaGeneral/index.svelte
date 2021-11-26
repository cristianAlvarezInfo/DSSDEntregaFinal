<script>
    import { cookies, token, userID } from '$store/store';
    $: segments = [];

    async function getTasks() {
      const formData = new FormData();
      formData.append("cookies", $cookies);
      formData.append("token", $token);
      formData.append("task_name", 'Validacion de formulario');
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



</script>

<div>
    {#await getTasks() }
        Trayendo sociedad anonimas. Espere :)
    {:then}
        {#if segments && segments.length}
        <ul style="display: flex; flex-direction: row;  list-style:none;">
        {#each segments as sociedad}
                <br>
                <li> { sociedad.data.nombre } </li>
                <li> { sociedad.data.emailApoderado } </li>
                <li><button on:click={ apropiarse(sociedad.task_id) }>Apropiarse</button></li>
        {/each}
        </ul>
        {:else}
        <div v-else>
            No hay tareas pendientes
        </div> 
        {/if}
    {/await}
</div>

