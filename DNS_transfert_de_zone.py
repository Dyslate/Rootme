import dns.query
import dns.zone
import dns.rdatatype
import dns.resolver
import traceback

# Paramètres
domain = "ch11.challenge01.root-me.org"
server = "challenge01.root-me.org"
port = 54011

try:
    # Résoudre le nom de domaine en une adresse IP
    server_ip = dns.resolver.resolve(server, "A")[0].to_text()

    # Lancer une requête AXFR (transfert de zone)
    zone_transfer = dns.query.xfr(server_ip, domain, port=port, rdtype=dns.rdatatype.AXFR)

    # Parcourir et imprimer tous les enregistrements obtenus
    for response in zone_transfer:
        for r in response.answer:
            if r.rdtype == dns.rdatatype.TXT:
                for txt_string in r:
                    print(txt_string)

except Exception as e:
    print("Erreur lors du transfert de zone :")
    traceback.print_exc()
