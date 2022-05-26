# MONOPOLY GAME
> Because this game is really big/editable, I created a special `readme.md` file for it!

> ## Game's datas
> 
> The game's datas is located in the `vars.py` file with the variable `initDatas`. <br>
> You can modify them by changing the value (*after the "="*)<br>
> 
> ## Game's datas list
> 
> #### `settings` **{ }**: *The settings object*
> 
> - #### `players` **[ ]** - **123**: *The minimum and maximum allowed players in game*
> 
> - #### `money` **{ }**: *Money related settings*
>   
>   - `name` **" "**: *The money's name*
>   - `symbol` **" "**: *The money's symbol*
>   - `values` **[ ]** - **123**: *The possible money values*
>   - `init` **[ ]** - **{ }**: *The initial player's economies*
>     - `value` **123**: *The money value*
>     - `count` **123**: *How many of this value*
> 
> - #### `constructions` **{ }**: *Constructions related settings*
>   
>   - `houses` **{ }**: *Houses related options*
>     
>     - `max` **123**: *The maximium houses buildable for a terrain*
>     - `rent` **[ ]** - **123**: *The coeficient by witch the default price of a house will by multiplied in function of the number of houses (take the last one if the more houses that the number of item inside this list).*
>     - `price` **123**: *The coeficient by witch the default price of a house will by multiplied to buy 1 house*
>   
>   - `hotels` **{ }**: *Hotels related options*
>     
>     - `max` **123**: *The maximium hotels buildable for a terrain*
>     - `rent` **[ ]** - **123**: *The coeficient by witch the default price of a hotel will by multiplied in function of the number of houses (take the last one if the more hotels that the number of item inside this list).*
>     - `price` **123**: *The coeficient by witch the default price of a hotel will by multiplied to buy 1 hotel*
>   
>   - `settings` **{ }**: *Main constructions related options*
>     
>     - `needAllCardsGroupBeforeBuilding` **0/1**: *If players need to have every card's group before doing construction*
>     - `needHousesBeforeHotels` **0/1**: *If a terrain needs to have the maximum amount of houses before building hotels*
>     - `accumulatePrices` **0/1**: *If, when calculating the price of a terrain, each price in function of the number of houses/hotels will be adding between them*
>     - `priceOfHousesAndHotels` **0/1**: *If, when the game calculate the price of a terrain, it will count the houses **and** the hotels, or just the hotels if there is hotels, else houses*
> 
> - #### `dice` **[ ]** - **123**: *The minimum/maximum dice value*
> 
> - #### `mortgageValue` **123**: *When a player mortgage a terrain, the initial value of the terrain will be added by this value, and the result of the operation will be added to the player's economies*
> 
> - #### `propertiesCost` **123**: *The property default rent in function of his initial cost*
> 
> - #### `prisonTime` **123**: *The default prison time (in laps)*
> 
> - #### `prisonCaseIndex` **123**: *When the player go to the prison, the case index to set he (in function of [the plate cases](#plate-----f-the-different-plates-cases)) (note: index `0` is the first case)*
> 
> - #### `packets` **{ }**: *The cards packets*
>   
>   > To edit packets, go to the definition of the `createPackets` function
>   
>   - `luck` ~ `community` **[ ]** - **f()**: *Where the cards object will be created (in function of the type of the card)*
>     
>     - `title` **" "**: *The title of the card*
>     
>     - `description` **" "**: *The description of the card*
>     
>     - `datas` **{ }**: *The different actions to do when the card is taked*
>       
>       - `give` **123**: *Give money to player (set a number <0 to remove money)*
>       
>       - `move` **{ }**: *Move the player where you want*
>         
>         - `to` **{ }**: *The location*
>           
>           - `name` **" "**: *The location name*
>           
>           - `type` **" "**: *The location type*
>           
>           - `index` **123**: *The location index*
>         
>         - `add` **123**: *The number of case to add from the current player location*
>         
>         - `instant` **0/1**: *if when player mooving the game check each cases*
>       
>       - `data` **{ }**: *changes datas of different things*
>         
>         - `player` **{ }**: *Changes datas of the player*
>       
>       - `players` **{ }**: *Different action to do to all others players (Work the same as the `datas` object)*
> 
> - #### `plate` **[ ]** - **{ }**: *The different plate's cases*
>   
>   > ### ***Function (to create cases)***
>   > 
>   > <u>`Default` **createCase()**</u>: *The default function to create a custom case*
>   > 
>   > - `card_name` **" "**: *The case's name*
>   > - `card_type` **" "**: *The case's type*
>   > - `card_datas` **{ }**: *The case's datas*
>   
>   > <u>`Property` **createProperty()**</u>: *Use this function to create a property case*
>   > 
>   > - `name` **" "**: *The terrain's name*
>   > - `cost` **123**: *The terrain's price*
>   > - `group` **" "**: *The terrain's group*
>   > - `allowConstructions` **0/1**: *If houses/hotels can be created on the terrain*
>   > - `more_datas` **{ }**: *The terrain's datas*
>   
>   > <u>`Packet` **createPacket()**</u>: *Use this function to create a packet case*
>   > 
>   > - `packet_type` **" "**: *The type of packet to take*
>   
>   - `name` **" "**: *The name of the case*
>   
>   - `type` **" "**: *The type of the case*
>   
>   - `data` **{ }**: *Differents datas associated with the case*
>     
>     - `money` **123**: *The cost of the case (or, for the starting case: the amount of money to give when the player pass on it)*
>     
>     - `group` **" "**: *The case's group (`None` if it doesn't has a group)*
>     
>     - `houses` **123**: *The number of houses in this terrain*
>     
>     - `hotels` **123**: The number of hotels in this terrain
>     
>     - `allowConstructions` **0/1**: *If houses/hotels* can be created on the terrain
>     
>     - `type` **" "**: *The type of the packet*
>     
>     - `calcValueBy` **" "**: *The behavior the the property's value calculator*
> 
> - #### `players` **[ ]** - **{ }**: *The list of the players' datas*:
>   
>   > *This settings is automatic: please don't modify it!*
>   
>   - `name` **" "**: *The player's name*
>   - `icon` **" "**: *The icon of the player (1 caracter)*
>   - `cards` **[ ]** - **{ }**: *The properties of the players* ([more informations](#plate-----f-the-different-plates-cases))
>   - `money` **[ ]** - **{ }**: *The economies of the player*
>   - `case` **123**: *The index of the current player's case*
>   - `prison` **123**: *The amount of prison laps the player needs to do*
> 
> - #### `cards` **[ ]** - **{ }**: *The list of the terrains' datas*:
>   
>   > *This setting is automatic: please don't modify it!* ([more informations](#plate-------the-different-plates-cases))
> 
> - #### `temp` **[ ]** - **{ }**: *Other variables*:
>   
>   > *This setting is automatic: please don't modify it!*
