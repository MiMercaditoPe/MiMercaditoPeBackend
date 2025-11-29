# grafo_distritos.py
from collections import defaultdict
import heapq

# Aristas reales aproximadas (km por carretera)
grafo_aristas = [
    (2, "Miraflores", "Barranco"), (2, "Barranco", "Miraflores"),
    (2, "Miraflores", "Surquillo"), (2, "Surquillo", "Miraflores"),
    (3, "Miraflores", "San Isidro"), (3, "San Isidro", "Miraflores"),
    (4, "San Isidro", "Lince"), (4, "Lince", "San Isidro"),
    (3, "Lince", "Jesús María"), (3, "Jesús María", "Lince"),
    (3, "Jesús María", "San Miguel"), (3, "San Miguel", "Jesús María"),
    (4, "Pueblo Libre", "Jesús María"), (4, "Jesús María", "Pueblo Libre"),
    (3, "San Isidro", "San Borja"), (3, "San Borja", "San Isidro"),
    (4, "San Borja", "Surquillo"), (4, "Surquillo", "San Borja"),
    (4, "San Borja", "Santiago de Surco"), (4, "Santiago de Surco", "San Borja"),
    (5, "Santiago de Surco", "La Molina"), (5, "La Molina", "Santiago de Surco"),
    (5, "Barranco", "Chorrillos"), (5, "Chorrillos", "Barranco"),
    (7, "Chorrillos", "Santiago de Surco"), (7, "Santiago de Surco", "Chorrillos"),
    (9, "Santiago de Surco", "Villa El Salvador"), (9, "Villa El Salvador", "Santiago de Surco"),
    (8, "San Miguel", "Callao"), (8, "Callao", "San Miguel"),
    (5, "Jesús María", "San Martín de Porres"), (5, "San Martín de Porres", "Jesús María"),
    (6, "San Martín de Porres", "Comas"), (6, "Comas", "San Martín de Porres"),
    (12, "Comas", "San Juan de Lurigancho"), (12, "San Juan de Lurigancho", "Comas"),
    (6, "Miraflores", "San Borja"), (6, "San Borja", "Miraflores"),
    (7, "Miraflores", "Santiago de Surco"), (7, "Santiago de Surco", "Miraflores"),
]

# Normalización de nombres
NORMALIZACION = {
    "Surco": "Santiago de Surco",
    "San Martin de Porres": "San Martín de Porres",
    "San Martín de Porres": "San Martín de Porres",
}

def normalizar_distrito(distrito: str) -> str:
    return NORMALIZACION.get(distrito.strip(), distrito.strip())

# Construir grafo
grafo = defaultdict(dict)
for dist, a, b in grafo_aristas:
    a_norm = normalizar_distrito(a)
    b_norm = normalizar_distrito(b)
    grafo[a_norm][b_norm] = dist
    grafo[b_norm][a_norm] = dist  # bidireccional

def distancia_entre_distritos(origen: str, destino: str) -> int:
    origen = normalizar_distrito(origen)
    destino = normalizar_distrito(destino)
    
    if origen == destino:
        return 0
    
    # Dijkstra
    cola = [(0, origen)]
    visitados = set()
    
    while cola:
        (costo, actual) = heapq.heappop(cola)
        if actual in visitados:
            continue
        visitados.add(actual)
        
        if actual == destino:
            return costo
            
        for vecino, peso in grafo[actual].items():
            if vecino not in visitados:
                heapq.heappush(cola, (costo + peso, vecino))
    
    return 999  # muy lejos o no conectado