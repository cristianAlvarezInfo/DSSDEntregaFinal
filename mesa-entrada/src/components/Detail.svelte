<script>
    export let sociedad = {};

    sociedad = sociedad.data;
</script>

<!--
{
   "case_id":"6",
   "task_id":"13",
   "assigned_id":"3",
   "data":{
      "id":1,
      "nombre":"Argentina",
      "fechaCreacion":"2021-11-26",
      "domicilioReal":"7 esq 60",
      "domicilioLegal":"1 y 54",
      "emailApoderado":"cris122.lp@gmail.com",
      "paisesExporta":[
         {
            "id":1,
            "codigo_gql":"AR"
         },  
      ],
      "estadosExporta":[
         {
            "id":1,
            "nombre_gql":"Ciudad Autónoma de Buenos Aires",
            "pais_gql":"AR"
         }
      ],
      "apoderado":{
         "nombre":"Lucio",
         "apellido":"Alvarez",
         "porcentajeAportesRealizados":80
      },
      "socios":[
         {
            "id":2,
            "nombre":"Marcos",
            "apellido":"Azcona",
            "porcentaje_aporte":20,
            "sociedad_id":1
         }
      ],
      "numero_expediente":null,
      "encrypted_id":"0",
      "id_caso":6,
      "file_id_drive":"1U1cPM0Qm3LINVP4qtXyew6NVd-ggGt8m"
   }
}
-->

<div>

    <p> Nombre: {sociedad.nombre} </p>
    <p> Fecha de Emision de Solicitud: {sociedad.fechaCreacion} </p>
    <p> Domicilio Real: {sociedad.domicilioReal} </p>
    <p> Domicilio Leal: {sociedad.domicilioLeal} </p>
    <p> Email Apoderado: {sociedad.emailApoderado} </p>
    <p> Nombre: {sociedad.nombre} </p>
    <p> Nombre: {sociedad.nombre} </p>
    <p> Estatuto: <a href="https://docs.google.com/document/d/"</p>
    <!--
        "paisesExporta":[
            {
               "id":1,
               "codigo_gql":"AR"
            },  
         ],
         "estadosExporta":[
            {
               "id":1,
               "nombre_gql":"Ciudad Autónoma de Buenos Aires",
               "pais_gql":"AR"
            }
         ],
    -->
    <p>
        Paises a los que exporta
        <ul>
        {#each sociedad.paisesExporta as paisExporta}
            <li>IATA: {sociedad.codigo_gql}</li> 
            <ul>
            {#each sociedad.estadosExporta as estadoExporta}
                {#if estadoExporta.pais_gql == paisExporta.codigo_gql}
                <li> { estadoExporta.nombre_gql } </li>
                {/if}
            {/each}
            </ul>
        {/each}
        </ul>
    </p>

</div>


