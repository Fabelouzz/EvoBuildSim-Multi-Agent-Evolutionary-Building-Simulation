import random
import os
import pandas as pd
"""
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
"""


class MaterialAgent:
    def __init__(self):
        self.inventory = {
            'doors': 51*3,  
            'outside_doors': 6*3,
            'windows': 96*3,
            'wall_modules': 57*3,
            'toilet_seats': 12*3,
            'tabs': 12*3,
            'shower_cabins': 12*3,
        }
        self.prices = {
        'doors': 2500,
        'outside_doors': 8500,
        'windows': 3450,
        'wall_modules': 75000,
        'toilet_seats': 2995,
        'tabs': 2350,
        'shower_cabins': 8300,
        }

    def restock_materials(self):
        # back to full capacity, 80% of 2 houses each for 4*3 builders
        restock_quantities = {
            'doors': 51*3,  
            'outside_doors': 6*3,
            'windows': 96*3,
            'wall_modules': 57*3,
            'toilet_seats': 12*3,
            'tabs': 12*3,
            'shower_cabins': 12*3,
        }
        for material, quantity in restock_quantities.items(): # Iterate over the restock quantities
            self.inventory[material] = quantity  # Reset to maximum capacity

    def process_request(self, materials_requested, building_agent):
        materials_provided = {}
        for material, quantity_requested in materials_requested.items():
            available_quantity = self.inventory.get(material, 0)
            
            if available_quantity > 0:
                cost_per_unit = self.prices[material]
                affordable_quantity = min(quantity_requested, building_agent.money // cost_per_unit, available_quantity)

                if affordable_quantity > 0:
                    cost = affordable_quantity * cost_per_unit
                    building_agent.money -= cost
                    self.inventory[material] -= affordable_quantity
                    materials_provided[material] = affordable_quantity
                    print(f"{building_agent.name} received {affordable_quantity} units of {material} for SEK {cost}.")
                else:
                    print(f"{building_agent.name} cannot afford any units of {material}.")
            else:
                # Print statement for when there is not enough material in the inventory
                print(f"Not enough {material} in inventory for {building_agent.name}'s request.")

        return materials_provided



    def __repr__(self):
        """
        Representation of a MaterialAgent object for debugging and logging.
        """
        return f"MaterialAgent Inventory: {self.inventory}"



class BuildingAgent:

    part_requirements = {
        'floor': {'windows': 11, 'doors': 7, 'wall_modules': 7, 'toilet_seats': 2, 'tabs': 2, 'shower_cabins': 2},
        'garret': {'windows': 3, 'doors': 1, 'wall_modules': 1},
        'hall': {'outside_doors': 1, 'windows': 1, 'wall_modules': 1}
    }


# Overall, attributes initialized inside __init__ are specific to each instance and may vary depending on the parameters passed during object creation, 
# while attributes initialized outside __init__ are shared among all instances of the class and have default values defined within the class.


    def __init__(self, name, priority_houses, build_order, buyprice, sellprice, money):
        """
        Initializes a BuildingAgent object with given attributes.

        :param priority_houses: An integer indicating the number of houses the agent prefers to build simultaneously (1 or 2).
        :param build_order: A list of strings indicating the preferred build order for parts of the house, e.g., ['floor', 'garret', 'hall'].
        :param money: A float representing the amount of money the agent is holding.
        """
        self.priority_houses = priority_houses
        self.current_focus_house = 0
        self.build_order = build_order
        self.money = money
        self.name = name
        self.houses_built = 0
        self.buyprice = buyprice
        self.sellprice = sellprice
        self.strategy_attributes = {'name': name, 'build_order': build_order, 'priority_houses': priority_houses, 'buyprice': buyprice, 'sellprice': sellprice}

        self.construction_progress = [
            {
                'floor': {'windows': 0, 'doors': 0, 'wall_modules': 0, 'toilet_seats': 0, 'tabs': 0, 'shower_cabins': 0},
                'garret': {'windows': 0, 'doors': 0, 'wall_modules': 0},
                'hall': {'outside_doors': 0, 'windows': 0, 'wall_modules': 0}
            } for _ in range(priority_houses)
        ]

        self.materials_needed = {'doors': 0, 'outside_doors': 0, 'windows': 0, 'wall_modules': 0, 'toilet_seats': 0, 'tabs': 0, 'shower_cabins': 0}
        self.excess_materials = {'doors': 0, 'outside_doors': 0, 'windows': 0, 'wall_modules': 0, 'toilet_seats': 0, 'tabs': 0, 'shower_cabins': 0}



    def __repr__(self):
        """
        Representation of a BuildingAgent object for debugging and logging.
        """
        return f"BuildingAgent Name: {self.name}, Priority Houses: {self.priority_houses}, Build Order: {self.build_order}, Money: {self.money}, Houses Built: {self.houses_built}, Buy Price: {self.buyprice}, Sell Price: {self.sellprice}"


    def check_materials_needed(self):
        materials_needed = {}

        # Reference the construction progress of the current focus house
        current_progress = self.construction_progress[self.current_focus_house] #for priority houses = 2

        for part in self.build_order:
            if all(current_progress[part][item] >= BuildingAgent.part_requirements[part][item] for item in BuildingAgent.part_requirements[part]):
                continue  # All required materials for this part are already acquired, move to the next part

            for material, required_quantity in BuildingAgent.part_requirements[part].items():
                acquired_quantity = current_progress[part].get(material, 0)
                if required_quantity > acquired_quantity:  # If more of this material is needed
                    materials_needed[material] = materials_needed.get(material, 0) + (required_quantity - acquired_quantity)

            if materials_needed:  # If any materials are needed for the current part, break the loop to focus on this part first
                break

        # Update the agent's materials_needed attribute
        self.materials_needed = materials_needed
        print(f"materials needed for {self.name}", materials_needed)

        return materials_needed



    def request_materials(self, material_agent):
        materials_needed = self.check_materials_needed()
        affordable_materials_needed = {}

        # Define current_progress at the start to ensure it's always available
        current_progress = self.construction_progress[self.current_focus_house]

        # Check how much of each needed material can be afforded
        for material, quantity_needed in materials_needed.items():
            cost_per_unit = material_agent.prices[material]
            affordable_quantity = min(quantity_needed, self.money // cost_per_unit)
            
            # Random chance to be forced to buy 3 extra units of a material
            if random.random() < 0.2:  # 
                excess_quantity = 1  # Fixed excess quantity
                if self.money >= (affordable_quantity + excess_quantity) * cost_per_unit:
                    affordable_quantity += excess_quantity  # Add excess quantity if affordable
                    print(f"{self.name} was forced to buy an additional {excess_quantity} units of {material}.")

            if affordable_quantity > 0:
                affordable_materials_needed[material] = affordable_quantity

        if affordable_materials_needed:
            current_part = next((part for part in self.build_order if any(current_progress[part][item] < BuildingAgent.part_requirements[part][item] for item in BuildingAgent.part_requirements[part])), None)
            if current_part:
                materials_provided = material_agent.process_request(affordable_materials_needed, self)
                for material, quantity in materials_provided.items():
                    # Update the focused house's progress with only the needed quantity
                    needed_quantity = min(materials_needed[material], quantity)
                    current_progress[current_part][material] += needed_quantity

                    # Any excess quantity is added to excess materials
                    excess_quantity = quantity - needed_quantity
                    if excess_quantity > 0:
                        self.excess_materials[material] = self.excess_materials.get(material, 0) + excess_quantity

                # Check if the current part is completed
                if all(current_progress[current_part][item] >= BuildingAgent.part_requirements[current_part][item] for item in BuildingAgent.part_requirements[current_part]):
                    print(f"{self.name} has completed {current_part}.")
                    
                    # Check if all parts of the current house are completed
                    if all(all(current_progress[part][item] >= BuildingAgent.part_requirements[part][item] for item in BuildingAgent.part_requirements[part]) for part in self.build_order):
                        self.houses_built += 1
                        print(f"{self.name} has completed house {self.houses_built} according to the build order.")
                        self.reset_construction_progress(self.current_focus_house)  # Reset the completed house's progress
                        self.sell_house()

        # Print current construction progress
        print(f"{self.name} is continuing construction. Current progress: {current_progress}")
        print(f"{self.name} has {self.money} SEK left.")
        if self.priority_houses == 1:
            print()
        if self.priority_houses == 2:
            print(f"{self.name} full construction progress: {self.construction_progress}", end="\n\n")


    def reset_construction_progress(self, house_index):
        """Reset construction progress for the specified house."""
        self.construction_progress[house_index] = {
            part: {material: 0 for material in requirements}
            for part, requirements in BuildingAgent.part_requirements.items()
        }


    def switch_focus(self):
        # Switch focus to the other house if priority_houses = 2
        if self.priority_houses == 2:
            self.current_focus_house = 1 - self.current_focus_house

    def sell_house(self):
        # Sell the house when all parts are completed
            print(f"{self.name} has {self.money} SEK before selling.")
            self.money += 900000
            print(f"{self.name} has sold house {self.houses_built} for 900000 SEK.")
            print(f"{self.name} has {self.money} SEK after selling.", end="\n\n")

def conduct_trading_round(builder_agents, material_agent):
    # Ensure builders have updated their materials_needed list
    for builder in builder_agents:
        builder.check_materials_needed()

    # Execute trades between builders
    for seller in builder_agents:
        for material, sell_quantity in seller.excess_materials.items():
            if sell_quantity <= 0:
                continue  # Skip if no excess material to sell

            for buyer in builder_agents:
                if buyer == seller or buyer.materials_needed.get(material, 0) <= 0:
                    continue  # Skip if the same builder or buyer doesn't need the material

                # Determine trade quantity based on what the buyer needs and what the seller has
                trade_quantity = min(buyer.materials_needed[material], sell_quantity)

                # Check if the buyer is willing to meet the seller's price
                if buyer.buyprice >= seller.sellprice:
                    print(f"{buyer.name} is buying {trade_quantity} units of {material} from {seller.name}.")
                    print(f"Before trade, {seller.name}'s {material}: {seller.excess_materials[material]}")
                    # Execute trade
                    trade_cost = trade_quantity * material_agent.prices[material] * seller.sellprice
                    print(f"trade cost: {trade_cost}")
                    if buyer.money >= trade_cost:
                        print(f"buyer money: {buyer.money}")
                        
                        # Update buyer's information
                        buyer.money -= trade_cost
                        buyer.materials_needed[material] -= trade_quantity
                        buyer.excess_materials[material] = buyer.excess_materials.get(material, 0) + trade_quantity
                        # Ensure we don't subtract more than available, preventing negative excess materials
                        actual_trade_quantity = min(sell_quantity, trade_quantity)

                        # Update seller's information
                        seller.money += trade_cost
                        if seller.excess_materials[material] >= actual_trade_quantity:
                            seller.excess_materials[material] -= actual_trade_quantity
                            print(f"After trade, {seller.name}'s {material}: {seller.excess_materials[material]}")

                        else:
                            print(f"Error: Attempting to reduce {material} below zero for seller {seller.name}.")
                            # Handle the error as appropriate, such as skipping the trade
                        
                        print(f"{buyer.name}: buyprice: {buyer.buyprice} >= {seller.name}: sellprice: {seller.sellprice} ")
                        print(f"{buyer.name} bought {actual_trade_quantity} units of {material} from {seller.name} at {trade_cost} SEK.")


    # Attempt to use any remaining excess materials for construction
    for builder in builder_agents:
        print(f"Initial {builder.name} construction progress: {builder.construction_progress[builder.current_focus_house]}")

        for material, quantity in builder.excess_materials.items():
            if quantity > 0 and builder.materials_needed.get(material, 0) > 0:
                # Determine how much of the excess material can be used for construction
                use_quantity = min(quantity, builder.materials_needed[material])

                # Update construction progress and excess materials
                current_progress = builder.construction_progress[builder.current_focus_house]
                for part in builder.build_order:
                    if material in BuildingAgent.part_requirements[part]:

                        current_progress[part][material] = min(current_progress[part].get(material, 0) + use_quantity, BuildingAgent.part_requirements[part][material])
                        print(f"{builder.name} put {use_quantity} units of excess {material} into his part {part}")  # Print after update

                        break  

                builder.excess_materials[material] -= use_quantity
                builder.materials_needed[material] = max(builder.materials_needed[material] - use_quantity, 0)
        print(f"Final {builder.name} construction progress: {builder.construction_progress[builder.current_focus_house]}")

def calculate_fitness_scores(builder_agents):
    fitness_scores = {}

    for agent in builder_agents:
        # Calculate the fitness score based on houses built and remaining money
        score = agent.houses_built + (agent.money / 1000000)
        fitness_scores[agent.name] = score
        print(f"Fitness Score for {agent.name}: {score:.2f}")

    return fitness_scores



def sort_agents_by_fitness(builder_agents):
    # Calculate fitness score for each agent and store it as an attribute
    for agent in builder_agents:
        agent.fitness_score = agent.houses_built + (agent.money / 1000000)

    # Sort agents based on fitness score, from high to low
    builder_agents.sort(key=lambda agent: agent.fitness_score, reverse=True)
    # at the end of each day, sort the agents by fitness score and print the results
    for agent in builder_agents:
        print(f"{agent.name}: Fitness Score = {agent.fitness_score}")





def write_stats_to_excel(builder_agents, start_money, forced_buy_chance, forced_buy_amount, file_name="agent_stats.xlsx"):
    # Prepare data for agents
    agent_data = []
    for agent in builder_agents:
        agent_stats = {
            "Name": agent.name,
            "Priority Houses": agent.priority_houses,
            "Build Order": ', '.join(agent.build_order),
            "Buy Price Multiplier": agent.buyprice,
            "Sell Price Multiplier": agent.sellprice,
            "Fitness Score": agent.houses_built + (agent.money / 1000000),
            "Amount of Houses Built": agent.houses_built,
            "Money": agent.money,
            "Number of Excess Material Items": sum(agent.excess_materials.values()),
            "Start Money": None,  # Placeholder for non-agent stats
            "Chance to Buy Excess Materials": None,  # Placeholder for non-agent stats
            "Standard Amount of Forced Excess Items": None  # Placeholder for non-agent stats
        }
        agent_data.append(agent_stats)


    # Convert agent data to a DataFrame
    df_agents = pd.DataFrame(agent_data)

    # Check if the file already exists
    if os.path.exists(file_name):
        # File exists, read existing data and append new data
        df_existing = pd.read_excel(file_name)
        df_final = pd.concat([df_existing, df_agents], ignore_index=True)
    else:
        # File doesn't exist, add non-agent stats in the first row and then append agent stats
        df_final = pd.concat([df_agents], ignore_index=True)

    # Write the DataFrame to an Excel file, without the index
    df_final.to_excel(file_name, index=False)

    print(f"Stats appended to {file_name}")

def write_stats_to_csv(builder_agents, start_money, forced_buy_chance, forced_buy_amount, file_name="agent_stats.csv"):
    # Prepare data for agents
    agent_data = []
    for agent in builder_agents:
        agent_stats = {
            "Name": agent.name,
            "Priority Houses": agent.priority_houses,
            "Build Order": ', '.join(agent.build_order),
            "Buy Price Multiplier": agent.buyprice,
            "Sell Price Multiplier": agent.sellprice,
            "Fitness Score": agent.houses_built + (agent.money / 1000000),
            "Amount of Houses Built": agent.houses_built,
            "Money": agent.money,
            "Number of Excess Material Items": sum(agent.excess_materials.values())
        }
        agent_data.append(agent_stats)

    # Convert agent data to a DataFrame
    df_agents = pd.DataFrame(agent_data)

    # Append to CSV, without index, adding a header only if the file is new
    with open(file_name, 'a', newline='') as f:
        df_agents.to_csv(f, header=f.tell()==0, index=False)

    print(f"Stats appended to {file_name}")


def extract_strategy_attributes(builder_agents):
    strategy_attributes = []
    for agent in builder_agents:
        attributes = {
            'build_order': agent.build_order,
            'priority_houses': agent.priority_houses,
            'buyprice': agent.buyprice,
            'sellprice': agent.sellprice
        }
        strategy_attributes.append(attributes)
    return strategy_attributes

import random

def roulette_wheel_selection(builder_agents):
    # Calculate fitness scores for all agents
    fitness_scores = [agent.houses_built + (agent.money / 1000000) for agent in builder_agents]
    cumulative_fitness = sum(fitness_scores)  # sum of all fitness scores
    selected_agents = []

    for _ in range(4):  # Select 4 agents for crossover
        selection_point = random.uniform(0, cumulative_fitness)  # Random point on the roulette wheel
        cumulative_sum = 0.0

        for agent, fitness_score in zip(builder_agents, fitness_scores):
            cumulative_sum += fitness_score
            if cumulative_sum > selection_point:
                selected_agents.append(agent)
                break  # Break the loop once an agent is selected

    return selected_agents



def perform_crossover(selected_agents):
    for i in range(0, len(selected_agents), 2):  # Iterate in pairs
        if i+1 < len(selected_agents):  # Check if there's a pair
            agent_a, agent_b = selected_agents[i], selected_agents[i+1]

            # Before swapping priority_houses, handle changes in construction progress
            for agent in (agent_a, agent_b):
                if agent.priority_houses == 2:  # Agent is working on 2 houses
                    # Check the counterpart's priority_houses to determine if it will change
                    counterpart_priority = agent_b.priority_houses if agent == agent_a else agent_a.priority_houses
                    if counterpart_priority == 1:  # If counterpart is working on only 1 house
                        # Move materials from the second house to excess_materials
                        for material, quantity in agent.construction_progress[1].items():
                            agent.excess_materials[material] = agent.excess_materials.get(material, 0) + sum(quantity.values())
                        # Remove the second dictionary in construction_progress
                        agent.construction_progress.pop()

            # Swap build_order and priority_houses
            agent_a.build_order, agent_b.build_order = agent_b.build_order, agent_a.build_order
            agent_a.priority_houses, agent_b.priority_houses = agent_b.priority_houses, agent_a.priority_houses
            
            # If an agent's priority_houses increased from 1 to 2, add a new dictionary to construction_progress
            for agent in (agent_a, agent_b):
                if len(agent.construction_progress) < agent.priority_houses:
                    agent.construction_progress.append({
                        'floor': {'windows': 0, 'doors': 0, 'wall_modules': 0, 'toilet_seats': 0, 'tabs': 0, 'shower_cabins': 0},
                        'garret': {'windows': 0, 'doors': 0, 'wall_modules': 0},
                        'hall': {'outside_doors': 0, 'windows': 0, 'wall_modules': 0}
                    })

            # Swap buyprice and sellprice
            agent_a.buyprice, agent_b.buyprice = agent_b.buyprice, agent_a.buyprice
            agent_a.sellprice, agent_b.sellprice = agent_b.sellprice, agent_a.sellprice

def perform_mutation(builder_agents, mutation_rate=0.1):
    for agent in builder_agents:
        mutated = False  # Flag to track if any mutation occurred for the current agent

        # Mutate build order with a chance defined by mutation_rate
        if random.random() < mutation_rate:
            original_order = agent.build_order[:]
            random.shuffle(agent.build_order)
            print(f"{agent.name} build order mutated from {original_order} to {agent.build_order}.")
            mutated = True

        # Mutate priority houses with a chance defined by mutation_rate
        if random.random() < mutation_rate:
            original_priority = agent.priority_houses
            agent.priority_houses = 2 if agent == 1 else 1
            print(f"{agent.name} priority houses mutated from {original_priority} to {agent.priority_houses}.")
            mutated = True

            # Adjust current_focus_house if priority_houses decreased
            if original_priority > agent.priority_houses:
                agent.current_focus_house = 0  # Reset to the first house

        # Mutate buyprice and sellprice directly with a new random integer between 1 and 8
        if random.random() < mutation_rate:
            original_buyprice = agent.buyprice
            agent.buyprice = random.randint(1, 8)
            print(f"{agent.name} buyprice mutated from {original_buyprice} to {agent.buyprice}.")
            mutated = True

        if random.random() < mutation_rate:
            original_sellprice = agent.sellprice
            agent.sellprice = random.randint(1, 8)
            print(f"{agent.name} sellprice mutated from {original_sellprice} to {agent.sellprice}.")
            mutated = True

        # Ensure construction_progress matches the mutated priority_houses
        if mutated:
            if agent.priority_houses < len(agent.construction_progress):
                # Move materials from removed houses to excess_materials and adjust construction_progress
                for removed_house in agent.construction_progress[agent.priority_houses:]:
                    for material, quantity in removed_house.items():
                        agent.excess_materials[material] = agent.excess_materials.get(material, 0) + sum(quantity.values())
                agent.construction_progress = agent.construction_progress[:agent.priority_houses]
                print(f"{agent.name} construction progress adjusted due to mutation in priority houses.")

            elif agent.priority_houses > len(agent.construction_progress):
                # Add new houses if priority_houses increased due to mutation
                for _ in range(agent.priority_houses - len(agent.construction_progress)):
                    agent.construction_progress.append({
                        'floor': {'windows': 0, 'doors': 0, 'wall_modules': 0, 'toilet_seats': 0, 'tabs': 0, 'shower_cabins': 0},
                        'garret': {'windows': 0, 'doors': 0, 'wall_modules': 0},
                        'hall': {'outside_doors': 0, 'windows': 0, 'wall_modules': 0}
                    })
                print(f"{agent.name} additional construction progress added due to mutation in priority houses.")


MaterialAgent1 = MaterialAgent()
# every agent has a unique strategy
# the agents at the top of the list starts with less money and the agents at the bottom of the list starts with more money
# this ensures that the advantage of being first to buy materials is balanced by the disadvantage of having less money
# after the first round of the competition, the agents are sorted by fitness score (houses built + (money/price of 1 house + 100k) (this happens every round aswell)
# and since fitness score is also based on money, the bottom agents will likely be the first to buy materials in round 2.
agent1 = BuildingAgent(name = "Krzysztof Wojcik", priority_houses=1, build_order=['floor', 'hall', 'garret'], buyprice = 1, sellprice = 2, money=1500000)
agent2 = BuildingAgent(name = "Ulf Stenhammare",priority_houses=1, build_order=['floor', 'garret', 'hall'], buyprice = 2, sellprice = 1, money=1550000)
agent3 = BuildingAgent(name = "Musa 1 of Mali",priority_houses=1, build_order=['garret', 'hall', 'floor'], buyprice = 1, sellprice = 1, money=1600000)
agent4 = BuildingAgent(name = "Florida Man",priority_houses=1, build_order=['garret', 'floor', 'hall'], buyprice = 2, sellprice = 3, money=1650000)
agent5 = BuildingAgent(name = "Thrall",priority_houses=1, build_order=['hall', 'floor', 'garret'], buyprice = 1, sellprice = 8, money=1700000)
agent6 = BuildingAgent(name = "Arthas Menethil",priority_houses=1, build_order=['hall', 'garret', 'floor'], buyprice = 8, sellprice = 1, money=1750000)
agent7 = BuildingAgent(name = "Kofi Dube", priority_houses=2, build_order=['floor', 'hall', 'garret'], buyprice = 4, sellprice = 3, money=1800000)
agent8 = BuildingAgent(name = "Kwame Juma",priority_houses=2, build_order=['floor', 'garret', 'hall'], buyprice = 4, sellprice = 5, money=1850000)
agent9 = BuildingAgent(name = "Heisenberg",priority_houses=2, build_order=['garret', 'hall', 'floor'], buyprice = 6, sellprice = 7, money=1900000)
agent10 = BuildingAgent(name = "Fabian",priority_houses=2, build_order=['garret', 'floor', 'hall'], buyprice = 5, sellprice = 6, money=1950000)
agent11 = BuildingAgent(name = "Robin",priority_houses=2, build_order=['hall', 'floor', 'garret'], buyprice = 6, sellprice = 5, money=2000000)
agent12 = BuildingAgent(name = "Hagarin",priority_houses=2, build_order=['hall', 'garret', 'floor'], buyprice = 3, sellprice = 4, money=2550000)

builder_agents = [agent1, agent2, agent3, agent4, agent5, agent6, agent7, agent8, agent9, agent10, agent11, agent12] 

days_to_simulate = 50

def main(days_to_simulate):
    


    for day in range(1, days_to_simulate + 1):
        print(f"\nDay {day}:")
        if day % 9 == 0:
            MaterialAgent1.restock_materials()
            print("MaterialAgent has restocked materials.", MaterialAgent1)

        # happy trading my builders!
        if day % 5 == 0:
            print("Trading Day!")
            conduct_trading_round(builder_agents, MaterialAgent1)

        else:
            for agent in builder_agents:
                agent.request_materials(MaterialAgent1)
                if agent.priority_houses == 2:
                    agent.switch_focus()  # Switch focus to the other house if priority_houses = 2



        if day % 6 == 0:
            print("Mutation day!")
            perform_mutation(builder_agents)


        # Genetic Algorithm steps every 15th day
        if day % 15 == 0:
            print("Genetic Algorithm day!:")
            # Sort agents by fitness score
            builder_agents.sort(key=lambda agent: agent.houses_built + (agent.money / 1000000), reverse=True)
            # Perform roulette wheel selection
            selected_agents = roulette_wheel_selection(builder_agents)
            print(f"Selected agents for crossover:{selected_agents}")
            for agent in selected_agents:
                print(f"Before the crossover, {agent.name} has the strategy attr: build order: {agent.build_order}, houses simultanious: {agent.priority_houses}, buyprice: {agent.buyprice}, sellprice: {agent.sellprice}")
            # Perform crossover among selected agents
            perform_crossover(selected_agents)
            print("Crossover completed.")
            for agent in selected_agents:
                print(f"Before the crossover, {agent.name} has the strategy attr build order: {agent.build_order}, houses simultanious: {agent.priority_houses}, buyprice: {agent.buyprice}, sellprice: {agent.sellprice}")

        print("--------------------")
        print(f"\nEnd of day {day} summary:")
        for agent in builder_agents:
            print(f"{agent.name} has built {agent.houses_built} houses. Current construction progress: {agent.construction_progress}", f"money: {agent.money}")
            print(f"{agent.name} excess materials {agent.excess_materials}", end="\n\n")
        print(MaterialAgent1)
        sort_agents_by_fitness(builder_agents)
        if day == days_to_simulate:
            write_stats_to_excel(builder_agents, start_money=1800000, forced_buy_chance=0.2, forced_buy_amount=1)
            write_stats_to_csv(builder_agents, start_money=1800000, forced_buy_chance=0.2, forced_buy_amount=1, file_name="agent_stats.csv")



if __name__ == "__main__":
    main(days_to_simulate)
