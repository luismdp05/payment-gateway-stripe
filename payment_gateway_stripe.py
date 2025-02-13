import os
import dotenv
import stripe
import stripe.error
import re

# Configuración del entorno

dotenv.load_dotenv()
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

stripe.api_key = STRIPE_SECRET_KEY

# Crear un método de pago manualmente
def create_payment_method() -> str:
    payment_types = ["card", "bank_account", "paypal", "google_pay", "apple_pay", "samsung_pay"]
    print("Tipos de métodos de pago disponibles:")
    for idx, payment_type in enumerate(payment_types):
        print(f"{idx + 1}. {payment_type}")

    selected_index = int(input("Seleccione el número del tipo de método de pago: ")) - 1
    selected_payment_type = payment_types[selected_index]

    if selected_payment_type == "card":
        test_cards = {
            "Visa": "tok_visa",
            "Visa (débito)": "tok_visa_debit",
            "Mastercard": "tok_mastercard",
            "Mastercard (débito)": "tok_mastercard_debit",
            "Mastercard (prepago)": "tok_mastercard_prepaid",
            "American Express": "tok_amex",
            "Discover": "tok_discover",
            "Diners Club": "tok_diners",
            "JCB": "tok_jcb",
            "UnionPay": "tok_unionpay"
        }
        print("Tarjetas de prueba disponibles:")
        for idx, (card_name, card_token) in enumerate(test_cards.items()):
            print(f"{idx + 1}. {card_name} - {card_token}")

        selected_card_index = int(input("Seleccione el número de la tarjeta de prueba: ")) - 1
        selected_card_token = list(test_cards.values())[selected_card_index]

        try:
            payment_method = stripe.PaymentMethod.create(
                type=selected_payment_type,
                card={
                    "token": selected_card_token
                }
            )
            print(f'Payment Method ID: {payment_method.id}')
        except stripe.error.StripeError as e:
            print(f'Error al crear el método de pago: {e.user_message}')
            return None

    elif selected_payment_type == "bank_account":
        account_number = input("Ingrese el número de cuenta bancaria: ")
        routing_number = input("Ingrese el número de ruta: ")
        account_holder_name = input("Ingrese el nombre del titular de la cuenta: ")
        account_holder_type = input("Ingrese el tipo de titular de la cuenta (individual/company): ")

        try:
            payment_method = stripe.PaymentMethod.create(
                type=selected_payment_type,
                bank_account={
                    "account_number": account_number,
                    "routing_number": routing_number,
                    "account_holder_name": account_holder_name,
                    "account_holder_type": account_holder_type
                }
            )
            print(f'Payment Method ID: {payment_method.id}')
        except stripe.error.StripeError as e:
            print(f'Error al crear el método de pago: {e.user_message}')
            return None

    elif selected_payment_type == "paypal":
        email = input("Ingrese el correo electrónico de PayPal: ")

        try:
            payment_method = stripe.PaymentMethod.create(
                type=selected_payment_type,
                paypal={
                    "email": email
                }
            )
            print(f'Payment Method ID: {payment_method.id}')
        except stripe.error.StripeError as e:
            print(f'Error al crear el método de pago: {e.user_message}')
            return None

    elif selected_payment_type == "google_pay":
        token = input("Ingrese el token de Google Pay: ")

        try:
            payment_method = stripe.PaymentMethod.create(
                type=selected_payment_type,
                google_pay={
                    "token": token
                }
            )
            print(f'Payment Method ID: {payment_method.id}')
        except stripe.error.StripeError as e:
            print(f'Error al crear el método de pago: {e.user_message}')
            return None

    elif selected_payment_type == "apple_pay":
        token = input("Ingrese el token de Apple Pay: ")

        try:
            payment_method = stripe.PaymentMethod.create(
                type=selected_payment_type,
                apple_pay={
                    "token": token
                }
            )
            print(f'Payment Method ID: {payment_method.id}')
        except stripe.error.StripeError as e:
            print(f'Error al crear el método de pago: {e.user_message}')
            return None

    elif selected_payment_type == "samsung_pay":
        token = input("Ingrese el token de Samsung Pay: ")

        try:
            payment_method = stripe.PaymentMethod.create(
                type=selected_payment_type,
                samsung_pay={
                    "token": token
                }
            )
            print(f'Payment Method ID: {payment_method.id}')
        except stripe.error.StripeError as e:
            print(f'Error al crear el método de pago: {e.user_message}')
            return None

    return payment_method.id

# Crear un intento de pago
def create_payment_intent(customer_id ,payment_method_id: str,product_id: str, amount: int, currency: str) -> str:

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount = amount,
            currency = currency,
            payment_method = payment_method_id,
            payment_method_types=["card"],
            customer = customer_id,
            confirm = True,
            metadata = {
                "product_id": product_id
            }
        )

        print(f'Payment Intent ID: {payment_intent.id} realizado con éxito')

    except stripe.error.CardError as e:
        print(f'Error en la tarjeta: {e.user_message}')
    except stripe.error.StripeError as e:
        print(f'Error de Stripe: {e.user_message}')
        

    return payment_intent.id

def is_valid_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def create_user():
    email = input("Ingrese el correo electrónico del usuario: ")
    
    while not is_valid_email(email):
        print("Correo electrónico no válido. Por favor, ingrese un correo electrónico válido.")
        email = input("Ingrese el correo electrónico del usuario: ")

    try:
        existing_customers = stripe.Customer.list(email=email)
        if existing_customers['data']:
            customer_id = existing_customers["data"][0]["id"]
            print(f'El usuario con el correo {email} ya existe con ID: {customer_id}')
            return customer_id

        name = input("Ingrese el nombre del usuario: ")
        customer = stripe.Customer.create(
            name=name,
            email=email
        )
        print(f'Customer {name} creado correctamente con ID: {customer.id}')
        return customer.id
    except stripe.error.StripeError as e:
        print(f'Error al crear el usuario: {e.user_message}')
        return None

def user_has_payment_method(customer_id):
    try:
        payment_methods = stripe.PaymentMethod.list(
            customer=customer_id
        )
        return len(payment_methods['data']) > 0
    except stripe.error.StripeError as e:
        print(f'Error al verificar los métodos de pago: {e.user_message}')
        return False

# Agregar un método de pago a un usuario
def add_payment_method_to_customer(customer_id, payment_method_id):

    try:
        payment_method = stripe.PaymentMethod.attach(
            payment_method_id,
            customer = customer_id
        )

        print(f'Método de pago {payment_method.id} agregado correctamente al usuario con ID: {customer_id}')
    except stripe.error.StripeError as e:
        print(f'Error al agregar el método de pago: {e.user_message}')

# Obtener los productos, permitir la selección y obtener el precio
def get_product_and_price():
    products = stripe.Product.list()
    print("Productos disponibles:")
    for idx, product in enumerate(products['data']):
        price_data = stripe.Price.list(product=product['id'])['data'][0]
        price = price_data['unit_amount']
        currency = price_data['currency']
        quantity = price_data['inventory']['quantity'] if 'inventory' in price_data else 'N/A'
        print(f"{idx + 1}. {product['name']} - Precio: {price / 100} {currency.upper()} - Cantidad: {quantity} (ID: {product['id']})")

    selected_index = int(input("Seleccione el número del producto que desea comprar: ")) - 1
    selected_product_id = products['data'][selected_index]['id']
    quantity = int(input("Ingrese la cantidad que desea comprar: "))
    
    price_id = price_data['id']
    amount = price_data['unit_amount']
    currency = price_data['currency']

    return selected_product_id, price_id, amount, currency, quantity

# Pruebas
customer_id = create_user()

if customer_id:
    if user_has_payment_method(customer_id):
        print(f'El usuario con ID: {customer_id} ya tiene un método de pago.')
        payment_methods = stripe.PaymentMethod.list(
            customer=customer_id
        )
        payment_method_id = payment_methods['data'][0]['id']
    else:
        payment_method_id = create_payment_method()
        if payment_method_id:
            add_payment_method_to_customer(customer_id, payment_method_id)

    product_id, price_id, amount, currency, quantity = get_product_and_price()
    create_payment_intent(customer_id, payment_method_id, product_id, amount * quantity, currency)