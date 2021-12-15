<script>
    import { cookies, token, userID, idProcess, isLoggedUser } from '$store/store.js'
    import Header from '$component/Header.svelte'

    const logout = () => {
        cookies.set('')
        token.set('')
        userID.set(-1)
        idProcess.set(-1)
        isLoggedUser.set(0)
    }

</script>


<svelte:head>
    <title> Gererencia </title>
</svelte:head>

<Header/>

<!--
<header class="header">
    
    <div style="width: 50%">
        <div>
            <span class="title"> Dashboard Gerencia </span>
        </div>
    </div>
    <div style="width: 50%">
        <div style="display: flex; justify-content: end">
            {#if $isLoggedUser == 0}
                <a href="/login"> Login </a>
            {:else}
                <a href="#" on:click={logout}> Logout </a>
            {/if}
        </div>
    </div>
</header>
-->

<slot />


<style>
    :global(body) {
        margin: 0 !important;
        background-color: #F3F2ED;
    }
    
</style>
