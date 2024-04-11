<template>
  <div id="app">
    <router-link to="/">Home</router-link> <!-- Adicione um link para a página inicial -->
    <router-link to="/about">About</router-link> <!-- Adicione um link para a página "About" -->
    <router-view /> <!-- Aqui serão renderizados os componentes correspondentes às rotas -->
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
