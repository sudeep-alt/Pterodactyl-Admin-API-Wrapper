# -----------------------------------------------------------------------------
# PteroAdmin - Pterodactyl Admin API Wrapper
# Copyright (c) 2025 Sudeep
# All rights reserved.
#
# Licensed under the MIT License. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
#
# Author: Sudeep
# -----------------------------------------------------------------------------

import requests
import json

# ----------------- Object Wrappers -----------------
class User:
    def __init__(self, data):
        self.raw = data  
        attrs = data['attributes']
        self.id = attrs['id']
        self.username = attrs['username']
        self.email = attrs['email']
        self.first_name = attrs['first_name']
        self.last_name = attrs['last_name']
        self.root_admin = attrs['root_admin']
        self.created_at = attrs['created_at']
        self.updated_at = attrs['updated_at']

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"

    def __str__(self):
        return f"{self.username} ({self.email})"

class Server:
    def __init__(self, data):
        attrs = data['attributes']
        self.id = attrs['id']
        self.name = attrs['name']
        self.uuid = attrs['uuid']
        self.user = attrs['user']
        self.suspended = attrs.get('suspended', False)
        self.created_at = attrs['created_at']
        self.updated_at = attrs['updated_at']

    def __repr__(self):
        return f"<Server {self.name} (ID {self.id})>"

    def __str__(self):
        return f"{self.name} (ID {self.id})"

class Node:
    def __init__(self, data):
        """
        Accepts both styles:
        - {"data": {"attributes": {...}}}
        - {"object": "node", "attributes": {...}, "meta": {...}}
        """
        # Normalize wrapper
        if "data" in data:
            data = data["data"]

        attrs = data.get("attributes", data)

        self.id = attrs.get("id")
        self.name = attrs.get("name")
        self.fqdn = attrs.get("fqdn")
        self.scheme = attrs.get("scheme")
        self.memory = attrs.get("memory")
        self.disk = attrs.get("disk")
        self.upload_size = attrs.get("upload_size")
        self.daemon_base = attrs.get("daemon_base")
        self.uuid = attrs.get("uuid")
        self.public = attrs.get("public")
        self.created_at = attrs.get("created_at")
        self.updated_at = attrs.get("updated_at")

        self.raw = data  # keep full response in case you need it

    def __repr__(self):
        return f"<Node id={self.id} name={self.name} fqdn={self.fqdn}>"

    def __str__(self):
        return f"{self.name} ({self.fqdn}) - Memory: {self.memory}MiB, Disk: {self.disk}MiB"



class Location:
    def __init__(self, data):
        attrs = data['attributes']
        self.id = attrs['id']
        self.short = attrs['short']
        self.long = attrs['long']

    def __repr__(self):
        return f"<Location {self.short}: {self.long}>"

    def __str__(self):
        return f"{self.short}: {self.long}"

class Allocation:
    def __init__(self, data):
        attrs = data['attributes']
        self.id = attrs['id']
        self.ip = attrs['ip']
        self.port = attrs['port']
        self.is_default = attrs['is_default']

    def __repr__(self):
        return f"<Allocation {self.ip}:{self.port} {'(default)' if self.is_default else ''}>"

    def __str__(self):
        return f"{self.ip}:{self.port} {'(default)' if self.is_default else ''}"

class Egg:
    def __init__(self, data):
        self.raw = data
        attrs = data["attributes"]

        self.id = attrs["id"]
        self.uuid = attrs["uuid"]
        self.name = attrs["name"]
        self.description = attrs.get("description")
        self.docker_image = attrs.get("docker_image")
        self.startup = attrs.get("startup")
        self.nest_id = attrs.get("nest_id")  # <-- safe access
        self.author = attrs.get("author")
        self.created_at = attrs.get("created_at")
        self.updated_at = attrs.get("updated_at")

    def __repr__(self):
        return f"<Egg {self.name} (id={self.id})>"
    
class Nest:
    def __init__(self, data):
        self.raw = data
        attrs = data["attributes"]

        self.id = attrs["id"]
        self.uuid = attrs.get("uuid")
        self.name = attrs["name"]
        self.description = attrs.get("description")
        self.created_at = attrs.get("created_at")
        self.updated_at = attrs.get("updated_at")

    def __repr__(self):
        return f"<Nest {self.name} (id={self.id})>"


# ----------------- Pretty List Wrapper -----------------
class PrettyList(list):
    """Automatically formats list of objects when printed."""
    def __str__(self):
        return "\n".join(f" - {item}" for item in self)

# ----------------- Admin Wrapper -----------------
class PteroAdminError(Exception):
    pass

class AdminClient:
    """Pterodactyl Admin API Wrapper (Application API)."""
    def __init__(self, api_key: str, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _request(self, method: str, endpoint: str, data: dict = None):
        url = f"{self.base_url}/api/application{endpoint}"
        try:
            res = requests.request(method, url, headers=self.headers, json=data)
            res.raise_for_status()
            return res.json() if res.text else {}
        except requests.RequestException as e:
            if e.response is not None and e.response.text:
                try:
                    error_json = e.response.json()
                    detail = error_json.get('errors', error_json)
                    raise PteroAdminError(f"API error: {detail}")
                except json.JSONDecodeError:
                    raise PteroAdminError(f"API error: {e.response.text}")
            raise PteroAdminError(f"API error: {e}")

    # ----------------- User Management -----------------
    def list_users(self):
        data = self._request("get", "/users")
        return PrettyList(User(u) for u in data['data'])

    def get_user(self, user_id):
        data = self._request("get", f"/users/{user_id}")
        # handle both response formats
        if "data" in data:
            return User(data["data"])
        elif "attributes" in data:
            return User(data)
        else:
            raise PteroAdminError(f"Unexpected response: {data}")

    def create_user(self, email, username, first_name, last_name, password):
    
        if not email or not username or not password:
                raise ValueError("email, username, and password are required fields.")
        if len(password) < 8:
                raise ValueError("Password must be at least 8 characters.")

        payload = {
                "email": email,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "password": password
            }

        data = self._request("post", "/users", payload)
        # Some APIs return {"data": {...}}, some return {"object": "user", "attributes": {...}}
        if "data" in data:
            return User(data["data"])
        elif "attributes" in data:  # full object has "attributes" key
            return User(data)
        else:
            raise PteroAdminError(f"Unexpected response: {data}")


    def delete_user(self, user_id):
        data = self._request("delete", f"/users/{user_id}")

        # handle both response formats
        if "data" in data:
            return User(data["data"])
        elif "attributes" in data:
            return User(data)
        else:
            raise PteroAdminError(f"Unexpected response: {data}")

    # ----------------- Server Management -----------------
    def list_servers(self):
        data = self._request("get", "/servers")
        return PrettyList(Server(s) for s in data['data'])

    def get_server(self, server_id):
        data = self._request("get", f"/servers/{server_id}")
        return Server(data['data'])

    # full create_server as before, omitted for brevity
    # suspend, unsuspend, delete as before

    # ----------------- Locations -----------------
    def list_locations(self):
        data = self._request("get", "/locations")
        return PrettyList(Location(l) for l in data['data'])

    def get_location(self, location_id):
        data = self._request("get", f"/locations/{location_id}")
        # handle both response formats
        if "data" in data:
            return Location(data["data"])
        elif "attributes" in data:
            return Location(data)
        else:
            raise PteroAdminError(f"Unexpected response: {data}")

    # ----------------- Nodes -----------------
    def list_nodes(self):
        data = self._request("get", "/nodes")
        return PrettyList(Node(n) for n in data['data'])

    def get_node(self, node_id):
        data = self._request("get", f"/nodes/{node_id}")
        # handle both response formats
        if "data" in data:
            return Node(data["data"])
        elif "attributes" in data:
            return Node(data)
        else:
            raise PteroAdminError(f"Unexpected response: {data}")


    def create_node(
    self,
    name: str,
    location_id: int,
    fqdn: str,
    scheme: str = "https",
    behind_proxy: bool = False,
    memory: int = 0,
    memory_overallocate: int = 0,
    disk: int = 0,
    disk_overallocate: int = 0,
    daemon_sftp: int = 2022,
    daemon_port: int = 8080,
    description: str = "",
    public: bool = True,
    upload_size: int = 100
):
        payload = {
            "name": name,
            "location_id": location_id,
            "fqdn": fqdn,
            "scheme": scheme,
            "behind_proxy": behind_proxy,
            "memory": memory,
            "memory_overallocate": memory_overallocate,
            "disk": disk,
            "disk_overallocate": disk_overallocate,
            "daemon_sftp": daemon_sftp,
            "daemon_listen": daemon_port,
            "description": description,
            "public": public,
            "upload_size": upload_size
        }

        data = self._request("post", "/nodes", payload)
        return Node(data)   # <-- always pass to Node



    # ----------------- Allocations -----------------
    def list_allocations(self, node_id):
        data = self._request("get", f"/nodes/{node_id}/allocations")
        return PrettyList(Allocation(a) for a in data['data'])

    def create_allocation(self, node_id, ip, ports: list):
        payload = {"ip": ip, "ports": ports}
        data = self._request("post", f"/nodes/{node_id}/allocations", payload)
        return Allocation(data['data'])

    # ----------------- Eggs -----------------
    def list_eggs(self, nest_id):
        data = self._request("get", f"/nests/{nest_id}/eggs")
        return PrettyList(Egg(e) for e in data['data'])

    def get_egg(self, nest_id, egg_id):
        data = self._request("get", f"/nests/{nest_id}/eggs/{egg_id}")
        return Egg(data['data'])
    
     # ----------------- Nests -----------------
    def list_nests(self):
        data = self._request("get", "/nests")
        return PrettyList(Nest(n) for n in data["data"])

    def get_nest(self, nest_id):
        data = self._request("get", f"/nests/{nest_id}")
        return Nest(data)





# © 2025 Sudeep
# -----------------------------------------------------------------------------
