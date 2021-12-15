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
      formData.append("role_name", "Gerencia");
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
</script>


<div>
  <div style="display: flex; justify-content: center; margin-top: 10%;">
    <div class="container-div">
        {#if !isValidInfo}
        <div class="error-msg error-container" style="margin-top: 20px">
            <span class="text-style" style="font-weight: 700; color: #151B25"> Los datos ingresados son invalidos </span>
        </div>
        {/if}
        <div class="container-form" style="padding-left: 10%; padding-top: 15%;">
          <form style="display: flex; flex-direction: column;">
            <div>
              <span class="text-style" style="color: #34D392">Iniciar Sesion</span>
            </div>  
            <div style="margin-top: 5%">
              <input
                bind:value={userInfo.username}
                type="text"
                class="input-text"
                placeholder="Ingrese su nombre de usuario"
              />
            </div>
            <div style="margin-top: 7%">
              <input
                bind:value={userInfo.password}
                type="password"
                class="input-text"
                placeholder="Ingrese su password"
              />
            </div>
            <div style="width: 100%; margin-top: 7%">
              <button class="submit-btn input-text" on:click={login}>Enviar</button>
            </div>
        </div>
    </div>
  </div>
</div>
  
<!--
<div>
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
-->

<style>
  .container-div {
    border-radius: 20px;
    height: 400px;
    width: 30%;
    background-color: white;
  }
  .container-form {
    display: flex; 
    justify-content: center;
    flex-direction: column;
  }
  .error-container {
    text-align: center; 
    height: 40px; 
    padding-top: 10px
  }
  .error-msg {
    background-color: #FB6666;
  }
  .text-style {
    font-family: Arial, Helvetica, sans-serif;
  }
  .input-text {
    width: 80%;
    height: 10px;
    padding: 10px;
  }
  .submit-btn {
    color: white;
    font-size: 22px;
    width: 85%;
    height: 50px;
    background-color: #34D392;
    border-color: #34D392;
  }
</style>