from fastapi import FastAPI, Depends, HTTPException,status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import Address_model,update_Address_model
from database import getDb,Address
from math import radians, sin, cos, sqrt, atan2

app = FastAPI()

# Create a new address
@app.post("/api/addresses/")
def create_address(address: Address_model, db: Session = Depends(getDb)):

    if address.latitude > 90 or address.latitude < -90:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="wrong latitude")
    
    if address.longitude > 180 or address.longitude < -180:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong longitude")
    
    add = Address(latitude=address.latitude,longitude=address.longitude)
    db.add(add)
    db.commit()
    db.refresh(add)

    return JSONResponse(status_code=status.HTTP_201_CREATED,content=jsonable_encoder(add))


@app.get("/api/addresses/filter")
def read_addresses_within_distance(latitude: float, longitude: float, distance: float, db: Session = Depends(getDb)):
    
    
    earth_radius_km = 6371

    addresses = db.query(Address).all()

    filtered_addresses = []
    for address in addresses:
        lat1, lon1 = radians(latitude), radians(longitude)
        lat2, lon2 = radians(address.latitude), radians(address.longitude)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance_km = earth_radius_km * c


        if distance_km <= distance:
            filtered_addresses.append(address)

    filtered_addresses = jsonable_encoder(filtered_addresses)

    return JSONResponse(status_code=status.HTTP_200_OK,content=filtered_addresses)


# Retrieve all addresses
@app.get("/api/addresses/")
def all_address(db: Session = Depends(getDb)):
    address = db.query(Address).all()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Addresses Empty")
    return JSONResponse(status_code=status.HTTP_200_OK,content=jsonable_encoder(address))

# Retrieve an address by id
@app.get("/api/addresses/{address_id}")
def read_address(address_id: int, db: Session = Depends(getDb)):
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Addresse not found")
    
    return JSONResponse(status_code=status.HTTP_200_OK,content=jsonable_encoder(address))

# Update an address
@app.put("/api/addresses/")
def update_address(address: update_Address_model, db: Session = Depends(getDb)):
    address = jsonable_encoder(address)

    
    if address.get('latitude') and  address['latitude'] > 90 or address['latitude'] < -90:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="wrong latitude")
    
    if address.get('longitude')  and address['longitude'] > 180 or address['longitude'] < -180:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong longitude")
    
    db_address = db.query(Address).filter(Address.id == address['id']).first()
    
    if not db_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    

    for key, value in address.items():
        setattr(db_address, key, value)
    db.commit()
    db.refresh(db_address)
    
    return JSONResponse(status_code=status.HTTP_200_OK,content=jsonable_encoder(db_address))

# Delete an address
@app.delete("/api/addresses/{address_id}")
def delete_address(address_id: int, db: Session = Depends(getDb)):
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    db.delete(address)
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK,content='Address deleted')


