% Travel Agent Knowledge Base

% Facts about destinations
% destination(destination_name, country, continent, destination_type, cost)
destination(paris, france, europe, city, 800).
destination(rome, italy, europe, city, 700).
destination(barcelona, spain, europe, city, 650).
destination(london, uk, europe, city, 750).
destination(santorini, greece, europe, beach, 900).
destination(bali, indonesia, asia, beach, 1200).
destination(kyoto, japan, asia, city, 1100).
destination(newyork, usa, north_america, city, 1000).
destination(cancun, mexico, north_america, beach, 850).
destination(cairo, egypt, africa, historical, 950).
destination(mauritius, mauritius, africa, beach, 1300).
destination(sydney, australia, oceania, city, 1500).
destination(queenstown, newzealand, oceania, adventure, 1400).
destination(swiss_alps, switzerland, europe, mountain, 1100).
destination(rocky_mountains, usa, north_america, mountain, 950).
destination(andes, chile, south_america, mountain, 1200).
destination(himalayas, nepal, asia, mountain, 900).
destination(dolomites, italy, europe, mountain, 1050).
destination(banff, canada, north_america, mountain, 1150).
destination(meru, tanzania, africa, mountain, 1050). 
destination(ossa, tasmania, australia, mountain, 1020).

% Facts about seasons and best times to visit
best_season(paris, spring).
best_season(paris, autumn).
best_season(rome, spring).
best_season(rome, autumn).
best_season(barcelona, summer).
best_season(london, summer).
best_season(santorini, summer).
best_season(bali, dry_season). % April-October
best_season(kyoto, spring). % Cherry blossoms
best_season(kyoto, autumn). % Fall colors
best_season(newyork, autumn).
best_season(newyork, spring).
best_season(cancun, winter).
best_season(cancun, spring).
best_season(cairo, winter).
best_season(cairo, spring).
best_season(mauritius, winter).
best_season(mauritius, spring).
best_season(sydney, summer).
best_season(sydney, spring).
best_season(queenstown, summer).
best_season(queenstown, winter). 
best_season(swiss_alps, winter).
best_season(swiss_alps, summer).
best_season(rocky_mountains, summer).
best_season(rocky_mountains, autumn).
best_season(andes, summer).
best_season(himalayas, spring).
best_season(himalayas, autumn).
best_season(dolomites, summer).
best_season(dolomites, winter).
best_season(banff, summer).
best_season(banff, winter).
best_season(meru, summer).
best_season(meru, winter).
best_season(ossa, summer). 
best_season(ossa, autumn). 

% Facts about activities available at destinations
activities(paris, [sightseeing, museum_visits, shopping, dining]).
activities(rome, [historical_sites, food_tours, shopping, religious_sites]).
activities(barcelona, [beach, architecture, nightlife, food]).
activities(london, [museums, theater, shopping, historical_sites]).
activities(santorini, [beach, sunset_views, wine_tasting, romantic_getaway]).
activities(bali, [beach, surfing, yoga, cultural_tours]).
activities(kyoto, [temples, gardens, cultural_experiences, hiking]).
activities(newyork, [sightseeing, shopping, broadway, museums]).
activities(cancun, [beach, snorkeling, nightlife, mayan_ruins]).
activities(cairo, [pyramids, historical_sites, nile_cruise, museum]).
activities(mauritius, [beach, water_sports, hiking, luxury_resorts]).
activities(sydney, [beach, opera_house, hiking, wildlife]).
activities(queenstown, [adventure_sports, hiking, skiing, scenic_views]).
activities(swiss_alps, [skiing, hiking, mountain_climbing, scenic_railways]).
activities(rocky_mountains, [hiking, wildlife_viewing, camping, photography]).
activities(andes, [trekking, mountain_climbing, cultural_tours, stargazing]).
activities(himalayas, [trekking, mountaineering, buddhist_monasteries, yoga]).
activities(dolomites, [skiing, hiking, via_ferrata, mountain_biking]).
activities(banff, [skiing, hiking, hot_springs, wildlife_photography]).
activities(meru, [hiking, wildlife_viewing, photography, camping]).
activities(ossa, [hiking, rock_climbing, nature_photography, camping]). 

% Facts about budget levels
budget_level(low, 0, 500).
budget_level(medium, 501, 1000).
budget_level(high, 1001, 2000).


% Rules for destination recommendations

% Recommend by continent
recommend_destination(Continent, BudgetLevel, Destination) :-
    destination(Destination, _, Continent, _, Cost),
    budget_level(BudgetLevel, MinBudget, MaxBudget),
    Cost >= MinBudget,
    Cost =< MaxBudget.

% Recommend by type (beach, city, historical, adventure)
recommend_destination_type(Type, BudgetLevel, Destination) :-
    destination(Destination, _, _, Type, Cost),
    budget_level(BudgetLevel, MinBudget, MaxBudget),
    Cost >= MinBudget,
    Cost =< MaxBudget.

% Recommend by country
recommend_destination_country(Country, BudgetLevel, Destination) :-
    destination(Destination, Country, _, _, Cost),
    budget_level(BudgetLevel, MinBudget, MaxBudget),
    Cost >= MinBudget,
    Cost =< MaxBudget.

% Get destination details
get_destination_details(Destination, Country, Continent, Type, Cost) :-
    destination(Destination, Country, Continent, Type, Cost).

% Get best seasons for a destination
get_best_seasons(Destination, Seasons) :-
    findall(Season, best_season(Destination, Season), Seasons).

% Get activities for a destination
get_activities(Destination, Activities) :-
    activities(Destination, Activities).

% Calculate total cost for multiple people
calculate_total_cost(Destination, NumberOfPeople, TotalCost) :-
    destination(Destination, _, _, _, CostPerPerson),
    TotalCost is CostPerPerson * NumberOfPeople.

% Find destinations within budget
destinations_within_budget(MaxBudget, Destination) :-
    destination(Destination, _, _, _, Cost),
    Cost =< MaxBudget.

% Find cheapest destination in a continent
cheapest_in_continent(Continent, Destination, Cost) :-
    destination(Destination, _, Continent, _, Cost),
    \+ (destination(Other, _, Continent, _, OtherCost), 
        OtherCost < Cost, Other \= Destination).

% Additional useful rules:

% Find destinations by type and continent
recommend_destination(Continent, Type, BudgetLevel, Destination) :-
    destination(Destination, _, Continent, Type, Cost),
    budget_level(BudgetLevel, MinBudget, MaxBudget),
    Cost >= MinBudget,
    Cost =< MaxBudget.

% Find similar destinations (same type and similar budget)
similar_destinations(Destination, SimilarDest, MaxPriceDifference) :-
    destination(Destination, _, _, Type, Cost1),
    destination(SimilarDest, _, _, Type, Cost2),
    Destination \= SimilarDest,
    PriceDiff is abs(Cost1 - Cost2),
    PriceDiff =< MaxPriceDifference.

% Find destinations with specific activity
destination_with_activity(Activity, Destination) :-
    activities(Destination, Activities),
    member(Activity, Activities).