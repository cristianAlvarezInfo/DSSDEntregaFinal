<script>
    import ChartCasesByTask from '$component/ChartCasesByTask.svelte'
    import ChartsetCasesByDate from '$component/ChartsetCasesByDate.svelte'
    let selectedOption = 0; // Representa el tipo de grafico seleccionado
</script>


<div class="container">
    <div class="nav-metrics nav-metrics-border">
        <div class="metric-width" on:click={() => selectedOption = 0}>
            <span> Casos por tarea </span>
        </div>
        <div class="metric-width" on:click={() => selectedOption = 1}>
            <span> Solicitudes de altas por dia </span>
        </div>
        <div class="metric-width" on:click={() => selectedOption = 2}>
            <span> Grafico3 </span>
        </div>
    </div>
    <div style="margin-top: 30px">
        Grafico
        {#if selectedOption == 0}
            <ChartCasesByTask />
        {:else if selectedOption == 1}
            <ChartsetCasesByDate />
        {:else}
            Chart 3
        {/if}
    </div>
</div>

<style scoped>
    .container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .nav-metrics-border {
        border: solid;
        border-width: 1px;
        border-radius: 8px;
        border-color: black;
    }

    .nav-metrics {
        width:  650px;
        height: 30px;
        display: flex;
        flex-direction: row;
        text-align: center;
    }

    .metric-width {
        width: 33%;
    }

</style>