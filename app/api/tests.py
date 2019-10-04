from django.urls import reverse, resolve
from .views import PizzaViewSet
from rest_framework import status
from rest_framework.test import APITestCase


class TestAPI(APITestCase):

    def setUp(self):
        customer_data_1 = {"name": "Sambit", "phone_number": "+4915204088293"}
        resp = self.client.post("/api/customers/", customer_data_1)

        customer_data_2 = {"name": "Sambo", "phone_number": "+919432945089"}
        resp = self.client.post("/api/customers/", customer_data_2)

        pizza_data = {"chicken":  {"flavour": "Chicken",
                                   "description": "Pizza With Chicken Stuffing."},
                      "veg": {"flavour": "Veg",
                              "description": "Pizza With Vegetables Stuffing."}
                      }

        resp = self.client.post(
            "/api/pizzas/", pizza_data["chicken"])
        resp = self.client.post(
            "/api/pizzas/", pizza_data["veg"])

    def test_pizza_count(self):
        response = self.client.get("/api/pizzas/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_customer_count(self):
        response = self.client.get("/api/customers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_create_new_order_without_customers(self):
        order_data = {
        }
        response = self.client.post("/api/orders/", order_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_new_order_without_items(self):
        customers_ids = [i["id"]
                         for i in self.client.get("/api/customers/").json()]
        order_data = {
            "customer": customers_ids[0],
        }
        response = self.client.post("/api/orders/", order_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_new_order_with_items_blank(self):
        customers_ids = [i["id"]
                         for i in self.client.get("/api/customers/").json()]
        order_data = {
            "customer": customers_ids[0],
            "items": []
        }
        response = self.client.post("/api/orders/", order_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_new_order_with_items_invalid_pizza_id(self):
        customers_ids = [i["id"]
                         for i in self.client.get("/api/customers/").json()]
        order_data = {
            "customer": customers_ids[0],
            "items": [
                {
                    "pizza": "hello world",
                    "count": 10,
                    "size": 1
                }
            ]
        }
        response = self.client.post("/api/orders/", order_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_new_order_with_items_invalid_count(self):
        customers_ids = [i["id"]
                         for i in self.client.get("/api/customers/").json()]
        pizza_ids = [i["id"]
                     for i in self.client.get("/api/customers/").json()]
        order_data = {
            "customer": customers_ids[0],
            "items": [
                {
                    "pizza": pizza_ids[0],
                    "count": -10,
                    "size": 2,
                }
            ]
        }
        response = self.client.post("/api/orders/", order_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_new_order_with_items_invalid_size(self):
        customers_ids = [i["id"]
                         for i in self.client.get("/api/customers/").json()]
        pizza_ids = [i["id"]
                     for i in self.client.get("/api/customers/").json()]
        order_data = {
            "customer": customers_ids[0],
            "items": [
                {
                    "pizza": pizza_ids[0],
                    "count": -10,
                    "size": "bigmama",
                }
            ]
        }
        response = self.client.post("/api/orders/", order_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_update_order_with_invalid_customer_id(self):
        customers_ids = [i["id"]
                         for i in self.client.get("/api/customers/").json()]
        pizza_ids = [i["id"]
                     for i in self.client.get("/api/customers/").json()]
        order_data = {
            "customer": customers_ids[0],
            "items": [
                {
                    "pizza": pizza_ids[0],
                    "count": 10,
                    "size": 1,
                }
            ]
        }
        response = self.client.post("/api/orders/", order_data, format="json")
        order_id = response.json()["id"]

        order_update = {
            "id": order_id,
            "customer": 123123123
        }

        response = self.client.put("/api/orders/", order_update, format="json")
        self.assertEqual(response.status_code, 405)

    def test_order_from_a_customer_cannot_be_updated_by_another_customer(self):
        customers_ids = [i["id"]
                         for i in self.client.get("/api/customers/").json()]
        pizza_ids = [i["id"]
                     for i in self.client.get("/api/customers/").json()]
        order_data = {
            "customer": customers_ids[0],
            "items": [
                {
                    "pizza": pizza_ids[0],
                    "count": 10,
                    "size": 2,
                }
            ]
        }
        response = self.client.post("/api/orders/", order_data, format="json")
        order_id = response.json()["id"]

        order_update = {
            "id": order_id,
            "customer": customers_ids[1],
            "status": 3
        }

        response = self.client.put(
            f"/api/orders/{order_id}/", order_update, format="json")
        self.assertEqual(response.status_code, 400)

    def test_add_an_item(self):
        customers_ids = [i["id"]
                         for i in self.client.get("/api/customers/").json()]
        pizza_ids = [i["id"]
                     for i in self.client.get("/api/pizzas/").json()]
        order_data = {
            "customer": customers_ids[0],
            "items": [
                {
                    "pizza": pizza_ids[0],
                    "count": 10,
                    "size": 2,
                },
                {
                    "pizza": pizza_ids[1],
                    "count": 15,
                    "size": 1
                }
            ]
        }
        response = self.client.post("/api/orders/", order_data, format="json")
        order = response.json()
        order_update = {
            "id": order["id"],
            "customer": customers_ids[0],
            "items": [
                {
                    "pizza": pizza_ids[1],
                    "count": 20,
                    "size": 2
                }
            ]
        }
        response = self.client.put(
            f"/api/orders/{order['id']}/", order_update, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["items"]), 3)

    def test_update_an_item_with_id(self):
        customers_ids = [i["id"]
                         for i in self.client.get("/api/customers/").json()]
        pizza_ids = [i["id"]
                     for i in self.client.get("/api/pizzas/").json()]
        order_data = {
            "customer": customers_ids[0],
            "items": [
                {
                    "pizza": pizza_ids[0],
                    "count": 10,
                    "size": 2,
                },
                {
                    "pizza": pizza_ids[1],
                    "count": 15,
                    "size": 1
                }
            ]
        }
        response = self.client.post("/api/orders/", order_data, format="json")
        order = response.json()
        order_update = {
            "id": order["id"],
            "customer": customers_ids[0],
            "items": [
                {
                    "id": order["items"][0]["id"],
                    "pizza": pizza_ids[1],
                    "count": 20,
                    "size": 1
                }
            ]
        }
        response = self.client.put(
            f"/api/orders/{order['id']}/", order_update, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["items"]), 2)

    def test_update_an_item_with_same_pizza_id(self):
        customers_ids = [i["id"]
                         for i in self.client.get("/api/customers/").json()]
        pizza_ids = [i["id"]
                     for i in self.client.get("/api/pizzas/").json()]
        order_data = {
            "customer": customers_ids[0],
            "items": [
                {
                    "pizza": pizza_ids[0],
                    "count": 10,
                    "size": 2,
                },
                {
                    "pizza": pizza_ids[1],
                    "count": 15,
                    "size": 1
                }
            ]
        }
        response = self.client.post("/api/orders/", order_data, format="json")
        order = response.json()
        order_update = {
            "id": order["id"],
            "customer": customers_ids[0],
            "items": [
                {
                    "pizza": pizza_ids[1],
                    "count": 20,
                    "size": 1
                }
            ]
        }
        response = self.client.put(
            f"/api/orders/{order['id']}/", order_update, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["items"]), 2)

    def test_delete_an_item(self):
        customers_ids = [i["id"]
                         for i in self.client.get("/api/customers/").json()]
        pizza_ids = [i["id"]
                     for i in self.client.get("/api/pizzas/").json()]
        order_data = {
            "customer": customers_ids[0],
            "items": [
                {
                    "pizza": pizza_ids[0],
                    "count": 10,
                    "size": 2,
                },
                {
                    "pizza": pizza_ids[1],
                    "count": 15,
                    "size": 1
                }
            ]
        }
        response = self.client.post("/api/orders/", order_data, format="json")
        order = response.json()
        order_update = {
            "id": order["id"],
            "customer": customers_ids[0],
            "items": [
                {
                    "id": order["items"][0]["id"],
                    "pizza": order["items"][0]["pizza"],
                    "count": 0,
                    "size": 1
                }
            ]
        }
        response = self.client.put(
            f"/api/orders/{order['id']}/", order_update, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["items"]), 1)

    def test_delete_an_order(self):
        customers_ids = [i["id"]
                         for i in self.client.get("/api/customers/").json()]
        pizza_ids = [i["id"]
                     for i in self.client.get("/api/pizzas/").json()]
        order_data = {
            "customer": customers_ids[0],
            "items": [
                {
                    "pizza": pizza_ids[0],
                    "count": 10,
                    "size": 2,
                },
                {
                    "pizza": pizza_ids[1],
                    "count": 15,
                    "size": 1
                }
            ]
        }
        response = self.client.post("/api/orders/", order_data, format="json")
        order = response.json()
        response = self.client.delete(
            f"/api/orders/{order['id']}/")
        self.assertEqual(response.status_code, 204)

    def test_filter(self):
        customers_ids = [i["id"]
                         for i in self.client.get("/api/customers/").json()]
        pizza_ids = [i["id"]
                     for i in self.client.get("/api/pizzas/").json()]
        order_data = {
            "customer": customers_ids[0],
            "items": [
                {
                    "pizza": pizza_ids[0],
                    "count": 10,
                    "size": 2,
                },
                {
                    "pizza": pizza_ids[1],
                    "count": 15,
                    "size": 1
                }
            ]
        }
        self.client.post("/api/orders/", order_data, format="json")
        self.client.post("/api/orders/", order_data, format="json")
        self.client.post("/api/orders/", order_data, format="json")
        self.client.post("/api/orders/", order_data, format="json")

        order_data["customer"] = customers_ids[1]
        self.client.post("/api/orders/", order_data, format="json")
        self.client.post("/api/orders/", order_data, format="json")

        response = self.client.get(
            f"/api/orders/", {"customer": customers_ids[0]})
        orders = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(orders), 4)

        response = self.client.get(
            f"/api/orders/", {"customer": customers_ids[1]})
        order = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(order), 2)
