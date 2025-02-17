import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext";
import "../../styles/cart.css";
import { useNavigate } from "react-router-dom";
"useclient";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";
import { imagenes } from "../../img/imagenes"; 

export const Cart = () => {
    const { store, actions } = useContext(Context);
    const navigate = useNavigate(); // Hook para redirigir al usuario
    const [loading, setLoading] = useState(false); // Para mostrar un indicador de carga

    const getProductImage = (productId) => {
        const imagen = imagenes.find(img => img.id === productId);
        return imagen ? imagen.url : ''; // Devolvemos la URL de la imagen si existe
    }

    useEffect(() => {
        actions.getCartFromAPI();
    }, []);

    // Calcular el total del carrito
    const totalAmount = store.cart.reduce((acc, product) => {
        const price = product.price && !isNaN(product.price) ? product.price : 0;
        return acc + price * product.quantity;
    }, 0).toFixed(2);

    // Función para manejar la creación de la orden
    const handleCreateOrder = async () => {
        setLoading(true);
        console.log("Intentando crear una orden...");
        const orderCreatedSuccessfully = await actions.checkout();
        setLoading(false);
        console.log("Resultado de la creación de la orden:", orderCreatedSuccessfully);

        if (orderCreatedSuccessfully) {
            console.log("Orden creada exitosamente.");
            // Detalles de la orden creada
            const createdOrder = {
                items: store.cart.map((product) => ({
                    product_id: product.id,
                    product_name: product.name,
                    price: product.price,
                    quantity: product.quantity,
                })),
                totalAmount: parseFloat(totalAmount),
            };
            console.log("Redirigiendo al resumen del pedido con los detalles:", createdOrder);
            // Redirigir al usuario al resumen de la orden
            navigate("/order-summary", { state: { orderDetails: createdOrder } });
        } else {
            console.error("Error: No se pudo crear la orden. Revisa los detalles del backend.");
        }
    };

    return (
        <div className="cart-container">
            {store.cart.length === 0 ? (
                <h2>Tu carrito está vacío.</h2>
            ) : (
                <>
                    {/* Contenedor de productos */}
                    <div className="cart-products">
                        <h2>Productos</h2>
                        <ul className="cart-items">
                            {store.cart.map((product, index) => {
                                const productImage = getProductImage(product.id); 
                                return (
                                    <li key={index} className="cart-item">
                                        <div className="cart-item-container">
                                            <img
                                                src={productImage} // Usamos la imagen del producto
                                                alt={product.name}
                                                className="cart-item-image"
                                            />
                                            <div className="cart-item-details">
                                                <span>{product.name}</span>
                                                <span>${product.price && !isNaN(product.price) ? product.price.toFixed(2) : 'N/A'}</span>
                                                <span>Cantidad: {product.quantity}</span>
                                                {/* Mostrar la descripción del producto */}
                                                <p className="product-description">{product.description}</p>
                                            </div>
                                            <button
                                                onClick={() => actions.removeFromCart(product.id)}
                                                className="remove-button"
                                            >
                                                X
                                            </button>
                                        </div>
                                    </li>
                                );
                            })}
                        </ul>
                        <button
                            onClick={actions.clearCart}
                            className="clear-cart-button"
                        >
                            Limpiar carrito
                        </button>
                    </div>

                    {/* Contenedor del total y botones */}
                    <div className="cart-summary">
                        <div className="total-container">
                            <h3>Total: ${totalAmount}</h3>
                        </div>
                        <button
                            onClick={handleCreateOrder}
                            className="checkout-button"
                            disabled={loading}
                        >
                            {loading ? "Procesando..." : "Realizar compra"}
                        </button>
                        <div className="paypal-button-container">
                            <PayPalScriptProvider
                                options={{
                                    clientId: "ATJCaAknFuveCgSzJhOyy5ZOLviAuWxXEPP518QPV60mJIxZkh8OJTaKnC3icv5jweOWBROONxqQGzTh",
                                }}
                            >
                                <PayPalButtons style={{ color: "blue", label: "pay" }} />
                            </PayPalScriptProvider>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};


