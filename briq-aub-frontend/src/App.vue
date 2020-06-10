<template>
  <div id="app">
    <Background/>
    <Quote/>
    <p> Developed with <span style="color: red">&#10084; </span> from Aubergine Solutions Pvt. Ltd. </p>
  </div>
</template>

<script>
import Quote from './components/Quote'
import Background from './components/Background'

export default {
  name: 'App',
  components: {
    Quote,
    Background
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
