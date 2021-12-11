<script>
    import { onMount } from 'svelte';
    import Chart from 'svelte-frappe-charts';
  
    let data = {};
  
    onMount(async () => {
        let response = await fetch('http://localhost:8000/api/cases_by_date/')
        response = await response.json();
        console.log(response["tasks"])
        let task=response["tasks"]
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

{#if Object.keys(data) && Object.keys(data).length }
    <Chart data={data} type="bar" />
{/if}
  