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
    <div style="width: 20%; padding-top: 20px; padding-left: 5px;"><span class="title text-color">Dashboards</span></div>
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
      color: black;
    }
    .title {
      font-size: 25px;
    }
    .navbar {
      display: flex; 
      flex-direction: row;
      width: 100%;
      height: 80px;
      justify-content: space-between;
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
        background-color: #34D392;
    }
</style>