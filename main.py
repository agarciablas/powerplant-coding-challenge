from fastapi import FastAPI,Body
import uvicorn
import pandas as pd

app = FastAPI()

@app.post("/productionplan")
def productionplan(payload: dict = Body(...)):

    # Get hourly demand from payload
    load=payload['load']
    # Load de power plants in a frame
    plants=pd.json_normalize(payload["powerplants"])
    # Adjust pmax according to wind forecast
    plants.loc[plants.type=='windturbine','pmax'] = plants.loc[plants.type=='windturbine','pmax'] * payload['fuels']['wind(%)']/100 
    # Calculate the unitary production cost for each plant according to its technology
    plants.loc[plants.type=='gasfired','unitary_cost'] = ( 1 / plants.loc[plants.type=='gasfired','efficiency']) * payload['fuels']['gas(euro/MWh)'] + 0.3*payload['fuels']['co2(euro/ton)']
    plants.loc[plants.type=='turbojet','unitary_cost'] = ( 1 / plants.loc[plants.type=='turbojet','efficiency']) * payload['fuels']['kerosine(euro/MWh)'] 
    plants.loc[plants.type=='windturbine','unitary_cost'] = 0

    # Set the production variable to 0
    plants['p']=0

    # Sorting by unit cost we get the merit order
    plants=plants.sort_values(by=['unitary_cost'],ascending=True)

    unassigned=load
    for index, p in plants.iterrows(): # For each power plant
        # If the maximum production of the plant is not enough to cover the remaining demand
        if p['pmax']  < unassigned :
            plants.loc[index,'p']=p['pmax']
            unassigned=unassigned-p['pmax']
        else:
            # If the pmin constraint allows to allocate the pending demand, otherwise the following plant has to be programmed
            if unassigned >= p['pmin']:
                plants.loc[index,'p']=unassigned
                unassigned=0
    # Round to 1 decimal the final schedule 
    plants['p']=plants['p'].round(1)
    # Return the production planning       
    return plants[['name','p']].to_dict(orient='records')

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8888, log_level="info")