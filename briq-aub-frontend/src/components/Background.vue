<template>
  <div class="background-selector" :style="cssVars">
    <div class="select ml-3">
      <!-- <label for="background">Select Background:</label> -->
      <select
        v-model="selectedBg"
        palceholder="Select Background"
        name="background"
        id="background"
        class="selectpicker"
      >
        <option v-for="bg in backgrounds" :value="bg" :key="bg">{{bg}}</option>
      </select>
    </div>
  </div>
</template>
<script>
/* eslint-disable */
export default {
  data() {
    return {
      backgrounds: ["art", "light", "green", "dark", "glass"],
      selectedBg: "light",
      bgColor: ""
    };
  },
  computed: {
    selectedBack: function() {
      console.log(this.selectedBg);
      document.body.className = this.selectedBg;
      return this.selectedBg;
    },
    cssVars() {
      return {
        "--theme": this.selectedBack
      };
    }
  }
};
</script>
<style lang="scss">
body {
  &.art {
    background-image: url("../assets/backgrounds/land.jpg");
  }

  &.bokeh {
    background-image: url("../assets/backgrounds/bokeh.jpg");
  }

  &.light {
    background-image: none;
    background-color: #ffffff;
  }

  &.green {
    background-image: url("../assets/backgrounds/green.jpg");
  }

  &.dark {
    background-color: rgba(63, 23, 62, 0.9);
    p {
      color: #ffffff;
    }

    .quote-container {
      background-color: rgba(0, 0, 0, 0.5);
      border-color: #ffffff;
      border-width: 2px;
    }
  }

  &.glass {
    background-image: url("../assets/backgrounds/glass.jpg");
  }

  background-size: cover;
}

select {
  outline: 0;
  background-image: none;
  width: 100%;
  height: 100%;
  color: #fff;
  cursor: pointer;
  border: 1px solid rgba(0, 0, 0, 0);
  border-radius: 3px;
  padding: 15px;
  background: rgba(0, 0, 0, 0.5);
  border-right-width: 15px;
}

.select {
  position: relative;
  display: block;
  width: 300px;
  line-height: 3;
  overflow: hidden;
  border-radius: 0.25em;
  padding-bottom: 10px;
}
</style>