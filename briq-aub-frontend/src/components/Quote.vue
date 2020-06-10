<template>
  <div>
    <div class="container">
      <div v-if="loaded" class="quote-container p-5 mt-5 light-theme">
        {{quote}}
        <p class="author mt-2">- {{author}}</p>
        <Rating v-if="loaded" />
      </div>
      <button class="btn btn-info my-5" id="getQuote" @click="getSimilarQuote()">{{get_quote}}</button>
    </div>
  </div>
</template>
<script>
/* eslint-disable */
import axios from "axios";
import Rating from "./Rating";

axios.defaults.baseURL = `http://0.0.0.0:8000`;

export default {
  components: { Rating },
  data() {
    return {
      loaded: false,
      get_quote: "Get Quote",
      quoteId: "",
      author: "",
      quote: ""
    };
    
  },
  mounted() {
    this.getRandomQuote();
    this.$root.$on("postRating", vote => {
      axios
        .post("/get_quote_suggestion/", {
          "quoteId": this.quoteId,
          "newVote": vote
        })
        .then(function(response) {
          console.log(response);
        });
    });
  },
  methods: {
    getRandomQuote() {
      axios
        .get("https://programming-quotes-api.herokuapp.com/quotes/random")
        .then(response => {
          this.loaded = true;
          this.quoteId = response.data.id;
          this.quote = response.data.en;
          this.author = response.data.author;
          this.get_quote = "Get Another Quote";
        });
    },
    getSimilarQuote() {
      axios
        .post("/get_new_quote/", {
          positiveSentiment: 0.12743020057678223
        })
        .then(response => {
          let res = response.data._source;
          this.quoteId = res.id;
          this.quote = res.en;
          this.author = res.author;
          this.get_quote = "Get Another Quote";
        });
    }
  }
};
</script>
<style lang="scss">
label {
  color: #fff;
}
.quote-container {
  border: 15px solid rgba(63,23,62,.9);
  text-align: center;
  margin: 0px auto;
  font-size: 36px;
  letter-spacing: 3px;
  margin-top: 0;
  position: relative;

  .author {
    font-size: 30px;
    font-style: italic;
  }

  &.light-theme {
    background: rgba(63,23,62,.9);
    color: #ffffff;
    text-shadow: -1px -1px 0px #223322, 0px 0px 0px #332233, 2px 2px 0px #332233;
  }

  &.dark-theme {
    background: #000000;
    color: #ffffff;
    text-shadow: -1px -1px 0px #223322, 0px 0px 0px #332233, 2px 2px 0px #332233;
  }
}
</style>