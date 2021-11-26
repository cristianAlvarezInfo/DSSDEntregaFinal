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
<nav style="display: flex; flex-direction: row">
    {#if $isLoggedUser == 1 }
        <a href="/bandejaGeneral"> Bandeja de entrada </a>
        <a href="/bandejaInterna"> Bandeja de entrada persona </a>
        <a href="#" on:click={logout}> Logout </a>
    {:else}
        <a href="/login"> Login </a>
    {/if}
</nav>