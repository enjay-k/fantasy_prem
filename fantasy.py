import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# this is the fantasy premier league api url
fantasy_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

# this makes a get request from the api endpoint using the requests package
req = requests.get(fantasy_url)

# the request as a json file
fantasy_json = req.json()

print("DICT KEYS\n", fantasy_json.keys())

elements_data = pd.DataFrame(fantasy_json["elements"])
element_types_data = pd.DataFrame(fantasy_json["element_types"])
teams_data = pd.DataFrame(fantasy_json["teams"])

# print all columns from elements_data
# print(elements_data.columns)

# choose the useful data
chosen_elements_data = elements_data[["second_name", "team", "element_type", 
                                      "selected_by_percent", "now_cost", 
                                      "minutes", "transfers_in", "form", 
                                      "value_season", "total_points", "id"]]

# print(chosen_elements_data.head())


# mapping the player position from element_types_data to element_type
chosen_elements_data["position"] = chosen_elements_data.element_type.map(
    element_types_data.set_index("id").singular_name)

# print(chosen_elements_data.head())

# mapping the team name
chosen_elements_data["team"] = chosen_elements_data.team.map(
    teams_data.set_index("id").name)

chosen_elements_data["value"] = chosen_elements_data.value_season.astype(
    float)

# display the most valuable players (by value) in descending order
# print(chosen_elements_data.sort_values("value", ascending=False).head(10))

# filter out players who've played 0 minutes
chosen_elements_data = chosen_elements_data.loc[chosen_elements_data.value > 0]

# create pivot table on the position coloumn
pivot = chosen_elements_data.pivot_table(
    index="position", values="value", aggfunc=np.mean).reset_index()
print("\n\nPOSITIONS IN ORDER OF VALUE\n", pivot.sort_values(
    "value", ascending=False))

# pivot table on the team column
team_pivot = chosen_elements_data.pivot_table(
    index="team", values="value", aggfunc=np.mean).reset_index()
print("\n\nTEAMS IN ORDER OF VALUE\n", team_pivot.sort_values(
    "value", ascending=False))

forward_data = chosen_elements_data.loc[chosen_elements_data.position == "Forward"]
midfielder_data = chosen_elements_data.loc[chosen_elements_data.position == "Midfielder"]
defender_data = chosen_elements_data.loc[chosen_elements_data.position == "Defender"]
goalkeeper_data = chosen_elements_data.loc[chosen_elements_data.position == "Goalkeeper"]

goalkeeper_data.value.hist()
plt.title("Goalkeeper value histogram")
plt.show()
print("\n\nMOST VALUABLE GKs\n", goalkeeper_data.sort_values(
    "value", ascending=False).head(10))
top_goalkeeper_data = goalkeeper_data.sort_values(
    "value", ascending=False).head(10)
print("\n\nHIGH-VALUE GKs WITH MOST POINTS\n", 
      top_goalkeeper_data.sort_values("total_points", ascending=False))

defender_data.value.hist()
plt.title("Defender value histogram")
plt.show()
print("\n\nMOST VALUABLE DFs\n", defender_data.sort_values(
    "value", ascending=False).head(20))
top_defender_data = defender_data.sort_values(
    "value", ascending=False).head(20)
print("\n\nHIGH-VALUE DFs WITH MOST POINTS\n", 
      top_defender_data.sort_values("total_points", ascending=False))

midfielder_data.value.hist()
plt.title("Midfielder value histogram")
plt.show()
print("\n\nMOST VALUABLE MFs\n", midfielder_data.sort_values(
    "value", ascending=False).head(20))
top_midfielder_data = midfielder_data.sort_values(
    "value", ascending=False).head(20)
print("\n\nHIGH-VALUE MFs WITH MOST POINTS\n", 
      top_midfielder_data.sort_values("total_points", ascending=False))

forward_data.value.hist()
plt.title("Forward value histogram")
plt.show()
print("\n\nMOST VALUABLE FWs\n", forward_data.sort_values(
    "value", ascending=False).head(15))
top_forward_data = forward_data.sort_values(
    "value", ascending=False).head(15)
print("\n\nHIGH-VALUE FWs WITH MOST POINTS\n", 
      top_forward_data.sort_values("total_points", ascending=False))

#print(chosen_elements_data.head())