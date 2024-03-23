import unittest
from main import create_app
from config import TestConfig
from exts import db

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app(TestConfig)

        self.client=self.app.test_client(self)

        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()
    
    def test_hello_world(self):
        hello_response=self.client.get('/recipes/hello')
        json=hello_response.json
        self.assertEqual(json,{"message":"Hello World"})
    
    def test_signup(self):
        signup_response=self.client.post('/auth/signup',
            json={"name": "Shubham",
                "email":"Skamdar@gmail.com",
                "password": "password"})
        
        status_code=signup_response.status_code
        self.assertEqual(status_code, 201)
    
    def test_login(self):
        signup_response=self.client.post('/auth/signup',
            json={"name": "Shubham",
                "email":"Skamdar@gmail.com",
                "password": "password"})
        
        login_response=self.client.post('auth/login',
            json={"email":"Skamdar@gmail.com",
                  "password":"password"})
        status_code=login_response.status_code
        self.assertEqual(status_code,200)

    def test_get_all_recipes(self):
        response=self.client.get('/recipes/Recipes')
        # print(response.json)
        # print(response.status_code)
        status_code=response.status_code
        self.assertEqual(status_code,200)

    def test_get_one_recipe_none(self):
        response=self.client.get('/recipes/Recipe/{id}')
        status_code=response.status_code
        self.assertEqual(status_code,404)
    
    def test_get_one_recipe(self):
        self.client.post('/auth/signup',
            json={"name": "Shubham",
                "email":"Skamdar@gmail.com",
                "password": "password"})
        login_response=self.client.post('auth/login',
            json={"email":"Skamdar@gmail.com",
                  "password":"password"})
        access_token=login_response.json["access token"]
        
        create_response=self.client.post('recipes/Recipes',
            json={"title":"Gulab Jamun",
                "description":"A tasty Indian desert"},
            headers={"Authorization":f"Bearer {access_token}"}
            )
        id=1
        get_one=self.client.get(f'/recipes/Recipe/{id}')
        json=get_one.json
        
        self.assertEqual(json,{'id': 1, 'title': 'Gulab Jamun', 'description': 'A tasty Indian desert'})

    def test_create_recipe(self):
        self.client.post('/auth/signup',
            json={"name": "Shubham",
                "email":"Skamdar@gmail.com",
                "password": "password"})
        login_response=self.client.post('auth/login',
            json={"email":"Skamdar@gmail.com",
                  "password":"password"})
        access_token=login_response.json["access token"]
        
        create_response=self.client.post('recipes/Recipes',
            json={"title":"Gulab Jamun",
                "description":"A tasty Indian desert"},
            headers={"Authorization":f"Bearer {access_token}"}
            )
        status_code=create_response.status_code
        # print(create_response.json)
        self.assertEqual(status_code,201)
        
    def test_update_recipe(self):
        self.client.post('/auth/signup',
            json={"name": "Shubham",
                "email":"Skamdar@gmail.com",
                "password": "password"})
        login_response=self.client.post('auth/login',
            json={"email":"Skamdar@gmail.com",
                  "password":"password"})
        access_token=login_response.json["access token"]
        
        create_response=self.client.post('recipes/Recipes',
            json={"title":"Gulab Jamun",
                "description":"A tasty Indian desert"},
            headers={"Authorization":f"Bearer {access_token}"}
            )
        id=1
        update_response=self.client.put(f'/recipes/Recipe/{id}',
            json={"title":"Ras malai",
                  "description":"A Tastier Indian Desert"},
            headers={"Authorization":f"Bearer {access_token}"})
        # print(update_response.json)
        # print(update_response.status_code)
        get_one=self.client.get(f'/recipes/Recipe/{id}')
        self.assertEqual(update_response.json,get_one.json)


    def test_delete_recipe(self):
        self.client.post('/auth/signup',
            json={"name": "Shubham",
                "email":"Skamdar@gmail.com",
                "password": "password"})
        login_response=self.client.post('auth/login',
            json={"email":"Skamdar@gmail.com",
                  "password":"password"})
        access_token=login_response.json["access token"]
        
        create_response=self.client.post('recipes/Recipes',
            json={"title":"Gulab Jamun",
                "description":"A tasty Indian desert"},
            headers={"Authorization":f"Bearer {access_token}"}
            )
        id=1
        delete_response=self.client.delete(f'/recipes/Recipe/{id}',
            headers={"Authorization":f"Bearer {access_token}"})
        # print(delete_response.json)
        # print(delete_response.status_code)
        status_code=delete_response.status_code
        self.assertEqual(status_code,200)
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
            
