<script>
    import { isLoggedUser } from '$store/store.js'


    import ChartCasesByTask from '$component/ChartCasesByTask.svelte'
    import ChartsetCasesByDate from '$component/ChartsetCasesByDate.svelte'
    import Dashboard from '$component/Dashboard.svelte'
</script>

{#if $isLoggedUser == 1}
<div class="container">
    <div style="margin-top: 30px; display: flex; flex-direction: row">
        <div style="margin-right: 100px; width: 300px; text-align: center">
            <label> Casos por tarea </label>
            <ChartCasesByTask />
        </div>
        <div style="margin-right: 100px; width: 300px; text-align: center">
            <label> Solicitudes de altas por dia </label>
            <ChartsetCasesByDate />
        </div>
        <div style="margin-right: 100px; width: 300px; text-align: center">
            <label> Altas aprobadas por dia </label>
            <Dashboard />
        </div>
    </div>
</div>
{/if}

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