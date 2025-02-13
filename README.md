## Proceso de Instalación

Sigue estos pasos para instalar y configurar la pasarela de pago con Stripe:

1. **Clonar el repositorio**:
    ```bash
    git clone https://github.com/luismdp05/payment-gateway-stripe.git
    cd payment-gateway-stripe
    ```

2. **Crear un entorno virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configurar variables de entorno**:
    Crea un archivo `.env` en la raíz del proyecto y añade tus claves de API de Stripe:
    ```
    STRIPE_PUBLIC_KEY=tu_clave_publica
    STRIPE_SECRET_KEY=tu_clave_secreta
    ```

5. **Iniciar el servidor**:
    ```bash
    python app.py
    ```

¡Listo! Ahora deberías tener la pasarela de pago con Stripe funcionando en tu entorno local.

Tomado de:

**Lógica aplicada a proyectos reales [2025]**

Proyectos para practicar lógica y aprender a implementar diferentes funcionalidades reales y habituales en todo tipo de aplicaciones.

**Web**: [retosdeprogramacion.com/logica-aplicada](https://retosdeprogramacion.com/logica-aplicada)

**YouTube**: https://www.youtube.com/watch?v=gOWCCkUq2nc&t=555s

@mouredev


