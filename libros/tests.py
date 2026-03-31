from django.test import TestCase, Client
from .models import Categoria, Genero, Autor, Libro


class TestLibros(TestCase):
    fixtures = ['dump_auth.json', 'dump_libreria.json']

    def setUp(self):
        self.client = Client()
        resauth = self.client.post('/api/token/', {
            'username': 'juan',
            'password': 'juan12345678'
        }, content_type='application/json')
        self.token = resauth.json().get('access', '')

    def test_generos_list(self):
        response = self.client.get('/api/generos/')
        assert response.status_code == 200

    def test_autores_list(self):
        response = self.client.get('/api/autores/')
        assert response.status_code == 200

    def test_libros_list(self):
        response = self.client.get('/api/libros/')
        assert response.status_code == 200

    def test_reporte_libros(self):
        response = self.client.get(
            '/api/reporte/libros/',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        assert response.status_code == 200