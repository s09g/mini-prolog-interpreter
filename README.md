# mini-prolog
*a mini prolog interpreter on python*<br/>

I used backword chaining in this porgram. <br/>
It could save space in memory, but it took a longer time for sentance query compared with forward chaining.<br/>
However, for any knowledge base smaller than 10k sentances (rules and facts), it should complete in less than 10 seconds.


---
#### some datails
* Achieved parsing and generated syntax tree by using Python Lex-Yacc module
* converted rules and fact into conjunctive normal form
* used an indexed-based knowledge base
* used backward chaining for sentence query
* avoided infinite loop in searching by implementing set of support
