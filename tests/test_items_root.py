"""Tests pour les routes API des items."""

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.item import Item


class TestGetItemsRoute:
    """Tests pour la route GET /items/."""

    def test_get_items_empty_database(self, client: TestClient):
        """Test que GET /items/ retourne une liste vide si la base est vide."""
        response = client.get("/items/")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_items_with_data(self, client: TestClient, session: Session):
        """Test que GET /items/ retourne tous les items."""
        # Créer des items de test
        item1 = Item(nom="Laptop", prix=999.99)
        item2 = Item(nom="Souris", prix=29.99)
        session.add(item1)
        session.add(item2)
        session.commit()

        response = client.get("/items/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["nom"] == "Laptop"
        assert data[1]["nom"] == "Souris"

    def test_get_items_with_pagination_skip(self, client: TestClient, session: Session):
        """Test la pagination avec le paramètre skip."""
        # Créer 5 items
        for i in range(5):
            item = Item(nom=f"Item {i}", prix=float(i * 10))
            session.add(item)
        session.commit()

        response = client.get("/items/?skip=2")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["nom"] == "Item 2"

    def test_get_items_response_model(self, client: TestClient, session: Session):
        """Test que la réponse correspond au modèle ItemResponse."""
        item = Item(nom="Test Item", prix=49.99)
        session.add(item)
        session.commit()
        session.refresh(item)

        response = client.get("/items/")

        assert response.status_code == 200
        data = response.json()[0]
        assert "id" in data
        assert "nom" in data
        assert "prix" in data
        assert data["nom"] == "Test Item"
        assert data["prix"] == 49.99


class TestGetItemRoute:
    """Tests pour la route GET /items/{item_id}."""

    def test_get_item_success(self, client: TestClient, session: Session):
        """Test la récupération d'un item existant."""
        item = Item(nom="Écran", prix=299.99)
        session.add(item)
        session.commit()
        session.refresh(item)

        response = client.get(f"/items/{item.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item.id
        assert data["nom"] == "Écran"
        assert data["prix"] == 299.99

    def test_get_item_not_found(self, client: TestClient):
        """Test que GET /items/{id} retourne 404 si l'item n'existe pas."""
        response = client.get("/items/9999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_item_invalid_id_type(self, client: TestClient):
        """Test avec un ID invalide (non entier)."""
        response = client.get("/items/invalid")

        assert response.status_code == 422  # Validation error


class TestCreateItemRoute:
    """Tests pour la route POST /items/."""

    def test_create_item_validation_missing_fields(self, client: TestClient):
        """Test que la validation échoue si des champs sont manquants."""
        item_data = {
            "nom": "Item Incomplet"
            # prix manquant
        }

        response = client.post("/items/", json=item_data)

        assert response.status_code == 422

    def test_create_item_validation_empty_nom(self, client: TestClient):
        """Test que le nom ne peut pas être vide."""
        item_data = {"nom": "", "prix": 10.0}

        response = client.post("/items/", json=item_data)

        assert response.status_code == 422

    def test_create_item_validation_negative_price(self, client: TestClient):
        """Test que le prix doit être positif."""
        item_data = {"nom": "Item Prix Négatif", "prix": -10.0}

        response = client.post("/items/", json=item_data)

        assert response.status_code == 422

    def test_create_item_validation_zero_price(self, client: TestClient):
        """Test que le prix ne peut pas être zéro."""
        item_data = {"nom": "Item Prix Zéro", "prix": 0.0}

        response = client.post("/items/", json=item_data)

        assert response.status_code == 422

    def test_create_item_validation_nom_too_long(self, client: TestClient):
        """Test que le nom ne peut pas dépasser 255 caractères."""
        item_data = {
            "nom": "a" * 256,  # 256 caractères
            "prix": 10.0,
        }

        response = client.post("/items/", json=item_data)

        assert response.status_code == 422


class TestUpdateItemRoute:
    """Tests pour la route PUT /items/{item_id}."""

    def test_update_item_validation_errors(self, client: TestClient, session: Session):
        """Test que la validation s'applique lors de la mise à jour."""
        item = Item(nom="Test", prix=50.0)
        session.add(item)
        session.commit()
        session.refresh(item)

        # Prix négatif
        update_data = {"prix": -10.0}
        response = client.put(f"/items/{item.id}", json=update_data)
        assert response.status_code == 422

        # Nom vide
        update_data = {"nom": ""}
        response = client.put(f"/items/{item.id}", json=update_data)
        assert response.status_code == 422


class TestDeleteItemRoute:
    """Tests pour la route DELETE /items/{item_id}."""

    def test_delete_item_success(self, client: TestClient, session: Session):
        """Test la suppression réussie d'un item."""
        item = Item(nom="À Supprimer", prix=25.0)
        session.add(item)
        session.commit()
        session.refresh(item)

        response = client.delete(f"/items/{item.id}")

        assert response.status_code == 204
        assert response.content == b""  # Pas de contenu pour 204

    def test_delete_item_removes_from_database(
        self, client: TestClient, session: Session
    ):
        """Test que l'item est bien supprimé de la base."""
        item = Item(nom="À Supprimer", prix=25.0)
        session.add(item)
        session.commit()
        session.refresh(item)
        item_id = item.id

        client.delete(f"/items/{item_id}")

        # Vérifier que l'item n'existe plus
        deleted_item = session.get(Item, item_id)
        assert deleted_item is None

    def test_delete_item_not_found(self, client: TestClient):
        """Test que DELETE /items/{id} retourne 404 si l'item n'existe pas."""
        response = client.delete("/items/9999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_delete_item_multiple_times(self, client: TestClient, session: Session):
        """Test qu'on ne peut pas supprimer deux fois le même item."""
        item = Item(nom="Test", prix=10.0)
        session.add(item)
        session.commit()
        session.refresh(item)

        # Première suppression
        response1 = client.delete(f"/items/{item.id}")
        assert response1.status_code == 204

        # Deuxième suppression
        response2 = client.delete(f"/items/{item.id}")
        assert response2.status_code == 404
