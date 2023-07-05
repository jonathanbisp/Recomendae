import './Login.css'

function Login(){
    return (
    <div class="login-screen">
        <form>
            <button id="login-close-button" class="close-button" type="button">x</button>
            <h2>Login</h2>
            <input type="text" placeholder="Usuário" />
            <input type="password" placeholder="Senha" />
            <button type="submit">Entrar</button>
        </form>
    </div>)
}

export default Login