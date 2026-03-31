from django.test import TestCase, Client
from .models import Categoria, OrganismoNorma, DocumentoTecnico


class TestDocTecnicos(TestCase):
    fixtures = ['dump_auth.json', 'dump_libreria.json']

    def setUp(self):
        self.client = Client()
        resauth = self.client.post('/api/token/', {
            'username': 'juan',
            'password': 'juan12345678'
        }, content_type='application/json')
        self.token = resauth.json().get('access', '')

    def test_organismos_list(self):
        response = self.client.get('/api/organismos/')
        assert response.status_code == 200

    def test_documentos_list(self):
        response = self.client.get('/api/documentos/')
        assert response.status_code == 200

    def test_reporte_documentos(self):
        response = self.client.get(
            '/api/reporte/documentos/',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        assert response.status_code == 200