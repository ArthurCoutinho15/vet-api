import pytest

API_URL = "api/v1/tutors/"

@pytest.mark.asyncio
async def test_create_tutor(client):
    payload = {
        "name": "Arthur",
        "cpf": "123",
        "email": "arthur@email.com",
        "phone": "9999",
        "address": "BH"
    }
    
    response = await client.post(API_URL, json=payload)
    
    assert response.status_code == 201
    
    data = response.json()
    print(data)
    assert data["name"] == "Arthur"
    assert data["email"] == "arthur@email.com"
    
@pytest.mark.asyncio
async def test_get_tutors(client):
    response = await client.get(API_URL)
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
@pytest.mark.asyncio
async def test_get_tutor_by_id(client):
    payload = {
        "name": "Arthur",
        "cpf": "123",
        "email": "arthur@email.com",
        "phone": "9999",
        "address": "BH"
    }
    
    created_tutor = await client.post(API_URL, json=payload)
    tutor_id = created_tutor.json()["id"]
    
    response = await client.get(f"{API_URL}{tutor_id}")
    
    assert response.status_code == 200
    assert response.json()["name"] == "Arthur"
    
@pytest.mark.asyncio
async def test_get_tutor_not_found(client):
    response = await client.get("/tutors_/9999")
    
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_tutor(client):
    payload = {
        "name": "Teste",
        "cpf": "555",
        "email": "a@email.com",
        "phone": "2222",
        "address": "BH"
    }
    
    created = await client.post(API_URL, json=payload)
    tutor_id = created.json()["id"]
    
    update = {"name": "Arthur"}
    
    response = await client.put(f"{API_URL}{tutor_id}", json=update)
    
    assert response.status_code == 202 
    assert response.json()["name"] == "Arthur"