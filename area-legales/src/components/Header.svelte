<script>
    import { cookies,token,userID,idProcess,isLoggedUser } from '$store/store' 

    const logout = () => {
        cookies.set('')
        token.set('')
        userID.set(-1)
        idProcess.set(-1)
        isLoggedUser.set(0)
    }


</script>
<nav class="navbar navbar-bg__color">
    <div style="width: 20%; padding-top: 20px; padding-left: 5px;"><span class="title text-color">Area de legales</span></div>
    <div class="navbar-opts" style="padding-top: 25px;">
        {#if $isLoggedUser == 1 }
          <a class="text-color" href="/bandejaGeneral"> Bandeja de entrada </a>
          <a class="text-color" href="/bandejaInterna"> Bandeja de entrada persona </a>
        {/if}
    </div>
    <div class="navbar-opts-end" style="padding-top: 20px; padding-right: 25px">
        {#if $isLoggedUser == 1}
          <a class="text-color" style="font-size: 21px" href="/" on:click={logout}> Logout </a>
        {:else}
          <a class="text-color" style="font-size: 21px" href="/login"> Login </a>
        {/if}
    </div>
</nav>  
<style scoped>
    *{
      font-family: Arial, Helvetica, sans-serif;
    }
    a {
      text-decoration: none;
    }
    .text-color{
      color: white;
    }
    .title {
      font-size: 25px;
    }
    .navbar {
      display: flex; 
      flex-direction: row;
      width: 100%;
      height: 80px;
    }
    .navbar-opts {
      width: 70%; 
      display: flex; 
      flex-direction: row; 
      justify-content: space-evenly;
      padding-top: 5px;
    }
    .navbar-opts-end {
      width: 10%; 
      display: flex; 
      justify-content: end; 
      padding-top: 5px;   
    }
    .navbar-bg__color {
        background-color: #127BAD;
    }
</style>

<!--<script>
    import { cookies,token,userID,idProcess,isLoggedUser } from '$store/store' 

    const logout = () => {
        cookies.set('')
        token.set('')
        userID.set(-1)
        idProcess.set(-1)
        isLoggedUser.set(0)
    }

</script>
<nav style="display: flex; flex-direction: row">
    <div style="margin-right: 10px"><span>Area legales</span></div>
    {#if $isLoggedUser == 1 }
        <div><a href="/bandejaGeneral"> Bandeja de entrada </a></div>
        <div style="margin-left: 10px"><a href="/bandejaInterna"> Bandeja de entrada persona </a></div>
        <div style="margin-left: 10px"><a href="#" on:click={logout}> Logout </a></div>
    {:else}
        <a href="/login"> Login </a>
    {/if}
</nav>  -->