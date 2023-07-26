from ldap3 import Server, Connection, ALL, SUBTREE, ALL_ATTRIBUTES

server_address = 'challenge01.root-me.org'
server_port = 54013
server = Server(server_address, port=server_port, get_info=ALL)

conn = Connection(server, auto_bind=True)

search_base = 'ou=anonymous,dc=challenge01,dc=root-me,dc=org'
search_filter = '(objectclass=*)'
search_scope = SUBTREE

if not conn.search(search_base, search_filter, search_scope, attributes=ALL_ATTRIBUTES):
    print(f"La recherche a échoué : {conn.result}")
else:
    for entry in conn.entries:
        if 'mail' in entry:
            print("Le flag est : ", entry['mail'])
