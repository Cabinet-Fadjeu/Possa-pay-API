
def convertire (devise, to_devise, amount_1):
    print('convertissement5')
    """
    Convertit un montant d'une devise à une autre.
    """
    if devise == to_devise:
        receiver_amount=amount_1
    elif devise == 'XAF' and to_devise == 'EUR':
        receiver_amount=amount_1 / 655.957
    elif devise == 'EUR' and to_devise == 'XAF':
        receiver_amount=amount_1 * 655.957
    else:
            # Si aucune des conditions ci-dessus n'est remplie, lever une exception
        raise ValueError(f"La conversion entre {devise} et {to_devise} n'est pas définie.")
    return receiver_amount


# def convert_to_decimal(amount):
#     """
#     Convertit une chaîne de caractères représentant un montant en un objet Decimal.
#     """
#     try:
#         # Remplacer la virgule par un point et convertir en Decimal
#         return Decimal(str(amount).replace(',', '.'))
#     except (ValueError, InvalidOperation):
#         raise ValueError(f"Le montant '{amount}' n'est pas valide.")


