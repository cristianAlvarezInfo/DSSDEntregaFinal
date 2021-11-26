<script>
    import Detail from '$component/Detail.svelte';
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
    
</script>

<div>
    {#await getTasks() }
        Trayendo sociedad anonimas. Espere :)
    {:then}
        {#if segments && segments.length}
        <ul style="display: flex; flex-direction: column;  list-style:none;">
        {#each segments as sociedad, i}
                <div style="display: flex; flex-direction: row; margin-top: 10px">
                    <li> { sociedad.data.nombre } </li>
                    <li style="margin-left: 10px"> { sociedad.data.emailApoderado } </li>
                    <li style="margin-left: 10px"><button on:click={() => openedDetails[i] = !openedDetails[i] || false}> Ver detalle </button></li>
                </div>
                <div>
                    {#if openedDetails[i]}
                    <li>
                        <Detail {sociedad} />
                    </li>
                    {/if}
                </div>
        {/each}
        </ul>
        {:else}
        <div v-else>
            No hay tareas pendientes
        </div> 
        {/if}
    {/await}
</div>
