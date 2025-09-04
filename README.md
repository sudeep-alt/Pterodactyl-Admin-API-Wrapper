# PteroAdmin

**Python wrapper for the Pterodactyl Application API**

Easily manage your Pterodactyl server resources programmatically using Python. This wrapper supports **Users, Servers, Nodes, Locations, Allocations, Eggs, and Nests**.

**Author:** Sudeep

---

## **Installation (Local)**

1. **Clone the repository**

```bash
git clone https://github.com/YourUsername/PteroAdmin.git
```

2. **Move the `PteroAdmin.py` file to your project folder** (or anywhere your Python code can import it from).

3. **Install dependencies**

```bash
pip install requests
```

4. **Import in your project**

```python
from PteroAdmin import AdminClient, PteroAdminError
```

---

## **Setup**

1. **Create an Application API Key** in your Pterodactyl panel:

   * Go to **Admin Panel → API → Application Keys → Create New Key**
   * Give it a **name**, eg. `MyAPIKey`
   * **Select All Permissions** (both **read** and **write**)
   * Copy the key safely, you’ll need it in your Python code

2. **Initialize the client**

```python
import pprint
from PteroAdmin import AdminClient, PteroAdminError

pp = pprint.PrettyPrinter(indent=2)

API_KEY = "your_application_api_key_here"
API_URL = "http://yourpanel.example.com"

client = AdminClient(API_KEY, API_URL)
```
---

# PteroAdmin

**Python wrapper for the Pterodactyl Admin API**

Easily manage your Pterodactyl server resources programmatically using Python. This wrapper supports **Users, Servers, Nodes, Locations, Allocations, Eggs, and Nests**.

**Author:** Sudeep

---

## **Installation (Local)**

Since this is not published on PyPI, you can install it locally:

1. **Clone the repository**

```bash
git clone https://github.com/YourUsername/PteroAdmin.git
```

2. **Move the `PteroAdmin.py` file to your project folder** (or anywhere your Python code can import it from).

3. **Install dependencies**

```bash
pip install requests
```

4. **Import in your project**

```python
from PteroAdmin import AdminClient, PteroAdminError
```

---

## **Usage**

### **Setup**

```python
import pprint
from PteroAdmin import AdminClient, PteroAdminError

pp = pprint.PrettyPrinter(indent=2)

API_KEY = "your_application_api_key"
API_URL = "http://yourpanel.example.com"

client = AdminClient(API_KEY, API_URL)
```

---

### **User Management**

```python
# List all users
users = client.list_users()
for u in users:
    pp.pprint(u.__dict__)

# Get a specific user
user = client.get_user(user_id=3)
pp.pprint(user.__dict__)

# Create a new user
new_user = client.create_user(
    email="test@example.com",
    username="tester",
    first_name="Test",
    last_name="User",
    password="password123"
)
pp.pprint(new_user.__dict__)

# Delete a user
client.delete_user(user_id=3)
```

---

### **Server Management**

```python
# List all servers
servers = client.list_servers()
for s in servers:
    pp.pprint(s.__dict__)

# Get a specific server
server = client.get_server(server_id=1)
pp.pprint(server.__dict__)
```

---

### **Locations & Nodes**

```python
# List locations
locations = client.list_locations()
for loc in locations:
    pp.pprint(loc.__dict__)

# Get a specific location
location = client.get_location(location_id=1)
pp.pprint(location.__dict__)

# List nodes
nodes = client.list_nodes()
for node in nodes:
    pp.pprint(node.__dict__)

# Get a specific node
node = client.get_node(node_id=9)
pp.pprint(node.raw)
```

---

### **Allocations**

```python
# List allocations on a node
allocs = client.list_allocations(node_id=9)
for a in allocs:
    pp.pprint(a.__dict__)

# Create a new allocation
new_alloc = client.create_allocation(node_id=9, ip="123.123.123.123", ports=[25565, 25566])
pp.pprint(new_alloc.__dict__)
```

---

### **Eggs & Nests**

```python
# List nests
nests = client.list_nests()
for n in nests:
    pp.pprint(n.__dict__)

# Get a specific nest
nest = client.get_nest(nest_id=1)
pp.pprint(nest.__dict__)

# List eggs in a nest
eggs = client.list_eggs(nest_id=1)
for e in eggs:
    pp.pprint(e.__dict__)

# Get a specific egg
egg = client.get_egg(nest_id=1, egg_id=2)
pp.pprint(egg.__dict__)
```

---

### **Error Handling**

All API errors are raised as `PteroAdminError` exceptions:

```python
try:
    client.get_user(9999)
except PteroAdminError as e:
    print(f"API Error: {e}")
```

---

### **Notes**

* Make sure your **API Key** has application-level access.
* The wrapper currently works with **Pterodactyl Application API v1**.
* For Pterodactyl API documentation, see [here](https://pterodactyl-api-docs.netvpx.com/)

---
