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
    <div style="margin-right: 10px"><span>Area legales</span></div>
    {#if $isLoggedUser == 1 }
        <div><a href="/bandejaGeneral"> Bandeja de entrada </a></div>
        <div style="margin-left: 10px"><a href="/bandejaInterna"> Bandeja de entrada persona </a></div>
        <div style="margin-left: 10px"><a href="#" on:click={logout}> Logout </a></div>
    {:else}
        <a href="/login"> Login </a>
    {/if}
</nav>  