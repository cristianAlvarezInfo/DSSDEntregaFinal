<script>
    import { onMount } from 'svelte';
    import { cookies, token, userID, idProcess, isLoggedUser } from '$store/store.js'
    
    if($isLoggedUser == 1) window.location.replace('/')

    let isValidInfo = true;
    const userInfo = { username: '', password: '' };
    
    async function getUserId({ username }) {
      const formData = new FormData();
      formData.append("username", username);
      const opts = {
        method: "POST",
        body: formData,
      };
      let response = await fetch(
        "http://localhost:8000/api/bonita_user_id/",
        opts
      );
      response = await response.json();
      return response.user_id;
    };

    
    async function loginBonita({ username, password }) {
      const formData = new FormData();
      formData.append("username", username);
      formData.append("password", password);
      formData.append("role_name", "Mesa de entrada");
      const opts = {
        method: "POST",
        body: formData,
      };
      let response = await fetch(
        "http://localhost:8000/api/login_role_bonita/",
        opts
      );
      response = await response.json();
      return response;
    }

    async function login(event) {
      event.preventDefault();
      let { Cookie, Token, processID, ok } = await loginBonita(userInfo);
      console.log(Cookie, Token, processID, ok);
      if (ok) {
        const idUser = await getUserId(userInfo);
        cookies.set(Cookie.toString());
        token.set(Token.toString());
        userID.set(parseInt(idUser));
        idProcess.set(parseInt(processID))
        isLoggedUser.set(1);
        window.location.replace("/");
        console.log('Info actualizada ',$cookies,$token,$userID,$idProcess,$isLoggedUser)
      } else {
        isValidInfo = false;
      }
    }
    console.log('Stores ',$cookies,$token,$userID,$idProcess,$isLoggedUser)
</script>


<div>
    {JSON.stringify(userInfo)}
    <div style="display: flex; justify-content: center">
        <div style="width: 30%">
            {#if !isValidInfo}
            <div>
              <span> Los datos ingresados son invalidos </span>
              <hr />
            </div>
            {/if}
        <form>
            <div>
              <label for="username"> Username </label>
              <input
                bind:value={userInfo.username}
                type="text"
                placeholder="Ingrese su nombre de usuario"
              />
            </div>
            <div>
                <label for="password"> Password </label>
                <input
                  bind:value={userInfo.password}
                  type="password"
                  placeholder="Ingrese su password"
                />
            </div>
            <div>
                <button on:click={login}>Enviar</button>
            </div>
        </form>
      </div>
    </div>
</div>