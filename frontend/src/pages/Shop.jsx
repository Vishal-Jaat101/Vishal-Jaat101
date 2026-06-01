import React, { useEffect, useState } from 'react'
import ProductCard from '../components/ProductCard'

export default function Shop() {
    const [products, setProducts] = useState([])
    useEffect(() => {
        fetch('/api/products').then(r => r.json()).then(setProducts).catch(e => console.error(e))
    }, [])
    return (
        <div className="site">
            <header className="site-hero">
                <div className="hero-content">
                    <h1>Velmington — Where luxury meets street</h1>
                    <p>Handpicked premium hoodies. Crafted details, timeless style.</p>
                </div>
            </header>
            <main className="container">
                <h2>Featured Essentials</h2>
                <div className="products-grid">
                    {products.map(p => <ProductCard key={p.id} p={p} />)}
                </div>
            </main>
        </div>
    )
}
