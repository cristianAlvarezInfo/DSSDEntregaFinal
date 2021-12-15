<script>
    import Header from '$component/Header.svelte'
</script>

<svelte:head>
    <title> Home </title>
</svelte:head>

<Header />

<slot />


<style>
    :global(body) {
      margin: 0 !important;
      background-color: #F3F2ED;
    }
  </style>