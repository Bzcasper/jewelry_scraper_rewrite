document.addEventListener('DOMContentLoaded', function() {
    const addForm = document.getElementById('add-jewelry-form');
    const scrapeForm = document.getElementById('scrape-jewelry-form');
    const searchForm = document.getElementById('search-form');
    const jewelryList = document.getElementById('jewelry-list');
    
    addForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(addForm);
        const data = Object.fromEntries(formData.entries());
        
        fetch('/api/jewelry', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            location.reload();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
    
    scrapeForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(scrapeForm);
        const data = Object.fromEntries(formData.entries());
        
        fetch('/api/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            location.reload();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
    
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const query = document.getElementById('search-input').value;
        const category = document.getElementById('category-filter').value;
        const minPrice = document.getElementById('min-price').value;
        const maxPrice = document.getElementById('max-price').value;
        
        let url = `/api/search?q=${encodeURIComponent(query)}`;
        if (category) url += `&category=${encodeURIComponent(category)}`;
        if (minPrice) url += `&min_price=${minPrice}`;
        if (maxPrice) url += `&max_price=${maxPrice}`;
        
        fetch(url)
        .then(response => response.json())
        .then(data => {
            jewelryList.innerHTML = '';
            data.forEach(item => {
                const itemElement = document.createElement('div');
                itemElement.classList.add('jewelry-item');
                itemElement.innerHTML = `
                    <h3>${item.title}</h3>
                    <p>${item.description}</p>
                    <p>Price: $${item.price}</p>
                    <p>Category: ${item.category}</p>
                    <p>Brand: ${item.brand}</p>
                    <p>Material: ${item.material}</p>
                    <p>Condition: ${item.condition}</p>
                    <img src=""${item.image_url}"" alt=""${item.title}"">
                `;
                jewelryList.appendChild(itemElement);
            });
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
    });
    document.addEventListener('DOMContentLoaded', function() {
        const addForm = document.getElementById('add-jewelry-form');
        const scrapeForm = document.getElementById('scrape-jewelry-form');
        const searchForm = document.getElementById('search-form');
        const jewelryList = document.getElementById('jewelry-list');
        
        addForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(addForm);
            const data = Object.fromEntries(formData.entries());
            
            fetch('/api/jewelry', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                location.reload();
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
        
        scrapeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(scrapeForm);
            const data = Object.fromEntries(formData.entries());
            
            fetch('/api/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                location.reload();
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
        
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = document.getElementById('search-input').value;
            const category = document.getElementById('category-filter').value;
            const minPrice = document.getElementById('min-price').value;
            const maxPrice = document.getElementById('max-price').value;
            
            let url = `/api/search?q=${encodeURIComponent(query)}`;
            if (category) url += `&category=${encodeURIComponent(category)}`;
            if (minPrice) url += `&min_price=${minPrice}`;
            if (maxPrice) url += `&max_price=${maxPrice}`;
            
            fetch(url)
            .then(response => response.json())
            .then(data => {
                jewelryList.innerHTML = '';
                data.forEach(item => {
                    const itemElement = document.createElement('div');
                    itemElement.classList.add('jewelry-item');
                    itemElement.innerHTML = `
                        <h3>${item.title}</h3>
                        <p>${item.description}</p>
                        <p>Price: $${item.price}</p>
                        <p>Category: ${item.category}</p>
                        <p>Brand: ${item.brand}</p>
                        <p>Material: ${item.material}</p>
                        <p>Condition: ${item.condition}</p>
                        <img src=""${item.image_url}"" alt=""${item.title}"">
                    `;
                    jewelryList.appendChild(itemElement);
                });
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
        });