import pytest
from application import app, db
from application.models import Entry

@pytest.fixture
def client():
  app.config['TESTING'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  
  with app.test_client() as client:
    with app.app_context():
      db.create_all()
    yield client
    with app.app_context():
      db.session.remove()
      db.drop_all()

def test_hello_world(client):
  response = client.get('/')
  assert response.status_code == 200
  data = response.get_json()
  assert data['message'] == 'Hello World!'
  assert data['description'] == 'Journal API'

def test_get_entries(client):
  entry = Entry(date='2023-09-20', title='Test Entry', content='This is a test entry', tag='Test', author='Test Author')
  db.session.add(entry)
  db.session.commit()

  response = client.get('/entries')
  assert response.status_code == 200
  data = response.get_json()
  assert len(data) == 1
  assert data[0]['title'] == 'Test Entry'

def test_get_entry(client):
  entry = Entry(date='2023-09-20', title='Test Entry', content='This is a test entry', tag='Test', author='Test Author')
  db.session.add(entry)
  db.session.commit()

  response = client.get(f'/entries/{entry.id}')
  assert response.status_code == 200
  data = response.get_json()
  assert data['title'] == 'Test Entry'

def test_create_entry(client):
  data = {
    'date': '2023-09-20',
    'title': 'New Entry',
    'content': 'This is a new entry',
    'tag': 'New',
    'author': 'New Author'
  }
  response = client.post('/entries', json=data)
  assert response.status_code == 201
  data = response.get_json()
  assert data['title'] == 'New Entry'

def test_update_entry(client):
  entry = Entry(date='2023-09-20', title='Test Entry', content='This is a test entry', tag='Test', author='Test Author')
  db.session.add(entry)
  db.session.commit()

  data = {'title': 'Updated Entry'}
  response = client.patch(f'/entries/{entry.id}', json=data)
  assert response.status_code == 200
  data = response.get_json()
  assert data['title'] == 'Updated Entry'

def test_delete_entry(client):
  entry = Entry(date='2023-09-20', title='Test Entry', content='This is a test entry', tag='Test', author='Test Author')
  db.session.add(entry)
  db.session.commit()

  response = client.delete(f'/entries/{entry.id}')
  assert response.status_code == 200
  data = response.get_json()
  assert data['message'] == 'Entry deleted'
