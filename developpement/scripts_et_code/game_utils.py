import math

def move_towards(target_pos, current_pos, speed):
    """
    Déplace progressivement une position actuelle vers une position cible à une vitesse donnée.
    
    :param target_pos: Tuple (x, y) représentant la position cible
    :param current_pos: Tuple (x, y) représentant la position actuelle
    :param speed: Vitesse de déplacement
    :return: Nouvelle position (x, y)
    """
    target_x, target_y = target_pos
    current_x, current_y = current_pos

    # Calculer la distance entre les deux points
    distance = math.hypot(target_x - current_x, target_y - current_y)

    # Si on est proche du point cible, arrêter le déplacement
    if distance < speed:
        return target_x, target_y

    # Calculer la direction du mouvement
    direction_x = (target_x - current_x) / distance
    direction_y = (target_y - current_y) / distance

    # Mettre à jour la position
    new_x = current_x + direction_x * speed
    new_y = current_y + direction_y * speed

    return new_x, new_y

def round_coordinates(coords):
    """
    Arrondit une liste ou un tuple de coordonnées flottantes à des entiers.
    
    :param coords: Liste ou tuple contenant des coordonnées (flottantes ou entières).
    :return: Tuple contenant les coordonnées arrondies.
    """
    return list(map(lambda x: round(float(x)), coords))

