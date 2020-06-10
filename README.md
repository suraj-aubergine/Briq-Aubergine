## Installation steps

- run ```docker-compose build```
- run ```docker-compose up```

### APIs

 - #### /get_quote_suggestion/ POST  
    - quoteId
    - newVote
 - #### /get_new_quote/ POST  --> POST API that returns a new quote on success
    - positiveSentiment
 - #### /get_quote/<quoteId> GET


The API endpoints needs to be fixed to proper route path format. e.g. /get_quote_suggestion/ to /suggested_quotes
