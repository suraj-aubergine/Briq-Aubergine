<template>
  <div class="rating row">
    <!-- <div class="col">Rate this Quote:</div> -->
    <div class="col ml-auto text-right">
      <span>{{ stars }} of {{ maxStars }}</span>
      <ul class="list">
        <li v-for="star in maxStars" :class="{ 'active': star <= stars }" class="star" :key="star">
          <icon :name="star <= stars ? 'star' : 'regular/star'" @click="rateQuote(star)" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import Icon from "vue-awesome/components/Icon";
import "vue-awesome/icons/star";
import "vue-awesome/icons/regular/star";

export default {
  components: { Icon },
  data() {
    return {
      stars: 0,
      maxStars: 5
    };
  },
  computed: {},
  methods: {
    rateQuote(star) {
      this.stars = star;
      this.$root.$emit("postRating", this.stars);
    }
  }
};
</script>

<style scoped>
.rating {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  font-size: 14px;
  color: #ffffff;
  text-align: right;
  position: absolute;
  left: 15px;
  right: 15px;
}
.list {
  margin: 0 0 5px 0;
  padding: 0;
  list-style-type: none;
}
.list:hover .star {
  color: #f3d23e;
}
.star {
  display: inline-block;
  cursor: pointer;
}
.star:hover ~ .star:not(.active) {
  color: inherit;
}
.active {
  color: #f3d23e;
}
</style>
