<script>
    import { onMount } from 'svelte';
    import { getArchiveCasesDistributedByDate } from '../metrics/service'
    
    import Chart from 'svelte-frappe-charts';

    let data = {};
    let data_length=0;
    onMount(async () => {
        console.log("Dashboard!!!")
        let response = await fetch('http://localhost:8000/api/get_archived_cases/')
        response = await response.json();
        const cases = getArchiveCasesDistributedByDate(response.tasks);
        let resp_values=Object.values(cases)
        data_length=resp_values.filter(value=> parseInt(value)!=0).length
        data = {
            labels: Object.keys(cases),
            datasets: [
                {
                    values: Object.values(cases)
                }
            ]  
        };
    })
  
</script>

{#if Object.keys(data) && Object.keys(data).length }
    <Chart data={data} type="line" />
{:else}
    <div>
        <span>No hay datos para mostrar</span>
    </div>
{/if}