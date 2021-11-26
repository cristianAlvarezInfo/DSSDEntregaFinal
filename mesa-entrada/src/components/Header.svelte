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
        <span> Bandeja de entrada </span>
        <span> Bandeja de entrada persona </span>
        <a href="#" on:click={logout}> Logout </a>
    {:else}
        <a href="/login"> Login </a>
    {/if}
</nav>