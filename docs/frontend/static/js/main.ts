<main>
    <section id=""add-jewelry"">
        <h2>Add Jewelry</h2>
        <form id=""add-jewelry-form"">
            <input type=""text"" name=""title"" placeholder=""Title"" required>
            <textarea name=""description"" placeholder=""Description""></textarea>
            <input type=""number"" name=""price"" placeholder=""Price"" step=""0.01"" required>
            <input type=""url"" name=""image_url"" placeholder=""Image URL"">
            <input type=""text"" name=""category"" placeholder=""Category"">
            <input type=""text"" name=""brand"" placeholder=""Brand"">
            <input type=""text"" name=""material"" placeholder=""Material"">
            <select name=""condition"">
                <option value="""">Select Condition</option>
                <option value=""New"">New</option>
                <option value=""Used"">Used</option>
                <option value=""Refurbished"">Refurbished</option>
            </select>
            <button type=""submit"">Add Jewelry</button>
        </form>
    </section>
    
    <section id=""scrape-jewelry"">
        <h2>Scrape Jewelry</h2>
        <form id=""scrape-jewelry-form"">
            <input type=""url"" name=""url"" placeholder=""URL to scrape"" required>
            <button type=""submit"">Scrape Jewelry</button>
        </form>
    </section>
    
    <section id=""search-jewelry"">
        <h2>Search Jewelry</h2>
        <form id=""search-form"">
            <input type=""text"" id=""search-input"" placeholder=""Search jewelry..."">
            <select id=""category-filter"">
                <option value="""">All Categories</option>
                <option value=""Rings"">Rings</option>
                <option value=""Necklaces"">Necklaces</option>
                <option value=""Earrings"">Earrings</option>
                <option value=""Bracelets"">Bracelets</option>
            </select>
            <input type=""number"" id=""min-price"" placeholder=""Min Price"">
            <input type=""number"" id=""max-price"" placeholder=""Max Price"">
            <button type=""submit"">Search</button>
        </form>
    </section>
    
    <section id=""jewelry-display"">
        <h2>Jewelry List</h2>
        <div id=""jewelry-list"">
            {% for item in jewelry %}
            <div class=""jewelry-item"">
                <h3>{{ item.title }}</h3>
                <p>{{ item.description }}</p>
                <p>Price: ${{ item.price }}</p>
                <p>Category: {{ item.category }}</p>
                <p>Brand: {{ item.brand }}</p>
                <p>Material: {{ item.material }}</p>
                <p>Condition: {{ item.condition }}</p>
                {% if item.image_url %}
                <img src=""{{ item.image_url }}"" alt=""{{ item.title }}"">
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </section>
</main>

<footer>
    <p>&copy; 2023 Jewelry Management System</p>
</footer>

<script src=""{{ url_for('static', filename='js/main.js') }}""></script>