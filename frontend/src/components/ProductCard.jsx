import React from 'react'

export default function ProductCard({ p }) {
    return (
        <div className="card product-card">
            <img src={p.image_url} alt={p.name} />
            <div className="card-body">
                <h4>{p.name}</h4>
                <p className="price">₹{p.price_inr}</p>
                <p className="desc">{p.description}</p>
                <div className="actions">
                    <a className="btn" href={`/product/${p.id}`}>Details</a>
                    <a className="btn primary" href={`/add_to_cart/${p.id}`}>Add to cart</a>
                </div>
            </div>
        </div>
    )
}
