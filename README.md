This Multi-Agent System (MAS) is an simulation platform that models a competitive environment where multiple building agents, 
each with unique strategies, compete to construct houses as efficiently and profitably as possible.
The system integrates simple economic behaviors, 
trading dynamics, and evolutionary algorithms to explore and optimize construction strategies under variable market conditions.
Each agent in the simulation possesses individualized attributes like build order, financial strategies (buyprice and sellprice),
and the capability to work on multiple houses simultaneously. This diversity introduces a rich variety of tactics and outcomes.
The system includes a Material Agent that manages a market with a finite inventory of construction materials. 
Agents will strategically purchase these materials, build houses, and sell them for profit.
a forced buy can occur, where an agent is forced to buy 3 extra units of a material, for some extra randomness in the system.
 On reoccuring trading days, agents can trade excess materials among themselves. This feature introduces an 
additional layer of strategy as agents must decide when to buy, sell, or trade based on their current needs and future projections.
The simulation incorporates genetic algorithms to drive evolutionary improvements in agent strategies. Every few days, agents undergo a roullete wheel 
selection process based on their 'fitness', which considers both the number of houses built and their financial health. 
Successful strategies are crossbred, promoting the development of more effective building strategies over time.
To maintain genetic diversity and adaptability, the system occasionally mutates agent attributes. This mutation can alter build orders, financial strategies, 
and the number of houses an agent aims to build simultaneously, allowing the system to explore new and potentially more effective strategies.
Comprehensive tracking of each agent's performance is conducted, including the number of houses builtz    , remaining funds, and material inventory. 
This data is periodically saved to external files in Excel and CSV formats for further analysis and visualization
Below are some static requirements and prices for building a house and buying materials.

Requirements to build 1 house:
Total Windows: 8 (bedrooms) + 3 (living room) + 1 (hall) + 3 (garret) = 15 windows
Total Doors: 4 (bedrooms) + 2 (bathrooms) + 1 (living room) + 1 (garret) = 8 doors (interior)
Total Outside Doors: 1 (hall) = 1 outside door
Total Wall Modules: 4 (bedrooms) + 2 (bathrooms) + 1 (living room) + 1 (hall) + 1 (garret) = 9 wall modules
Total Toilet Seats: 2 (bathrooms) = 2 toilet seats
Total Tabs: 2 (bathrooms) = 2 tabs
Total Shower Cabins: 2 (bathrooms) = 2 shower cabins

Requirements for 4 building agents to build 2 houses each. 
Total Windows: 15 windows/house * 8 houses = 120 windows
Total Interior Doors: 8 doors/house * 8 houses = 64 interior doors
Total Outside Doors: 1 outside door/house * 8 houses = 8 outside doors
Total Wall Modules: 9 wall modules/house * 8 houses = 72 wall modules
Total Toilet Seats: 2 toilet seats/house * 8 houses = 16 toilet seats
Total Tabs: 2 tabs/house * 8 houses = 16 tabs
Total Shower Cabins: 2 shower cabins/house * 8 houses = 16 shower cabins

Warehouse storage capacity for each item with 80% of the requirements for 8 houses:
rounded down to the nearest whole number
Windows: 120 * 0.8 = 96 windows
Interior Doors: 64 * 0.8 = 51 interior doors
Outside Doors: 8 * 0.8 = 6 outside doors
Wall Modules: 72 * 0.8 = 57 wall modules 
Toilet Seats: 16 * 0.8 = 12 toilet seats
Tabs: 16 * 0.8 = 12 tabs
Shower Cabins: 16 * 0.8 = 12 shower cabins

requirements for each section of the house:
Floor: 4 bedrooms, 2 bathrooms, 1 living room.
Floor components: 
4 bedrooms = 8 windows, 4 doors, 4 wall modules
2 bathrooms =  2 doors, 2 wall modules, 2 toilet seats, 2 tabs, 2 shower cabins
1 living room = 3 windows, 1 door, 1 wall module
total floor requirements : 11 windows, 7 doors, 7 wall modules, 2 toilet seats, 2 tabs, 2 shower cabins

Hall: 1 outside-door, 1 window, 1 wall module
Garret: 3 windows, 1 door, 1 wall module

prices
Item           Quantity    Price    Description
Door           1           2500     Inside door for the rooms and the toilet, etc.
Outside-Door   1           8500     door only for hall
Window         1           3450     All windows are the same.
Wall-Module    1           75000    A 4-wall module making a room
Toilet-Seat    1           2995
Tab            1           2350
Shower Cabin   1           8300

total cost for 1 house:
15 windows * 3450 = 51750
8 doors * 2500 = 20000
1 outside door * 8500 = 8500
9 wall modules * 75000 = 675000
2 toilet seats * 2995 = 5990
2 tabs * 2350 = 4700
2 shower cabins * 8300 = 16600
total cost = 782540
sell price = 900000

How to Use:
Clone the Repository and navigate to the project directory.
Run the Simulation by executing main(days_to_simulate) with your desired number of days.
Analyze Results using the generated Excel and CSV files containing detailed performance metrics.
EvoBuildSim is ideal for exploring multi-agent systems, evolutionary algorithms, and strategic resource management in a competitive environment.
