<script>
    import { onMount } from 'svelte';
    import Chart from 'svelte-frappe-charts';
  
    let data = {};
    let data_length=0;
  
    onMount(async () => {
        let response = await fetch('http://localhost:8000/api/cases_by_task/')
        response = await response.json();
        console.log(response["tasks"])
        let task=response["tasks"]
        let resp_values=Object.values(task)
        data_length=resp_values.filter(value=> parseInt(value)!=0).length
        console.log(data_length)
        data = {
          labels: Object.keys(task),
            datasets: [
                {
                    values: Object.values(task)
                }
            ]  
        };
    })
  

</script>
{#if data_length }
    <Chart data={data} type="pie" />
{:else}
    <div>
        <span>No hay datos para mostrar</span>
    </div>
{/if}
    
  