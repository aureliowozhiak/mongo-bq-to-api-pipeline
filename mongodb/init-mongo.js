// Criar banco de dados e collection
db = db.getSiblingDB('ecommerce');
db.createCollection('purchases');

// Função para gerar data aleatória nos últimos 30 dias
function randomDate() {
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - 30);
    return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
}

// Função para gerar um produto aleatório
function randomProduct() {
    const products = [
        { name: "Smartphone", price: 1999.99, category: "Eletrônicos" },
        { name: "Notebook", price: 4999.99, category: "Eletrônicos" },
        { name: "Smart TV", price: 2999.99, category: "Eletrônicos" },
        { name: "Fone de Ouvido", price: 299.99, category: "Acessórios" },
        { name: "Mouse", price: 99.99, category: "Acessórios" },
        { name: "Teclado", price: 199.99, category: "Acessórios" },
        { name: "Monitor", price: 899.99, category: "Eletrônicos" },
        { name: "Cadeira Gamer", price: 1299.99, category: "Móveis" },
        { name: "Mesa Gamer", price: 799.99, category: "Móveis" },
        { name: "Webcam", price: 399.99, category: "Acessórios" }
    ];
    return products[Math.floor(Math.random() * products.length)];
}

// Função para gerar um cliente aleatório
function randomCustomer() {
    const firstNames = ["João", "Maria", "Pedro", "Ana", "Lucas", "Julia", "Carlos", "Beatriz", "Rafael", "Fernanda"];
    const lastNames = ["Silva", "Santos", "Oliveira", "Souza", "Ferreira", "Pereira", "Costa", "Rodrigues", "Almeida", "Nascimento"];
    const cities = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador", "Brasília", "Curitiba", "Fortaleza", "Manaus", "Recife", "Porto Alegre"];
    
    return {
        name: `${firstNames[Math.floor(Math.random() * firstNames.length)]} ${lastNames[Math.floor(Math.random() * lastNames.length)]}`,
        email: `cliente${Math.floor(Math.random() * 1000)}@email.com`,
        city: cities[Math.floor(Math.random() * cities.length)]
    };
}

// Função para gerar uma compra
function generatePurchase() {
    const product = randomProduct();
    const quantity = Math.floor(Math.random() * 3) + 1;
    const customer = randomCustomer();
    
    return {
        customer: customer,
        product: product,
        quantity: quantity,
        total_price: product.price * quantity,
        purchase_date: randomDate(),
        payment_method: ["Cartão de Crédito", "Boleto", "PIX"][Math.floor(Math.random() * 3)],
        status: ["Concluído", "Em processamento", "Enviado"][Math.floor(Math.random() * 3)]
    };
}

// Gerar e inserir 1000 compras
const purchases = [];
for (let i = 0; i < 1000; i++) {
    purchases.push(generatePurchase());
}

// Inserir em lotes de 100 para melhor performance
const batchSize = 100;
for (let i = 0; i < purchases.length; i += batchSize) {
    const batch = purchases.slice(i, i + batchSize);
    db.purchases.insertMany(batch);
}

// Criar índices para melhor performance
db.purchases.createIndex({ "purchase_date": 1 });
db.purchases.createIndex({ "customer.email": 1 });
db.purchases.createIndex({ "product.category": 1 });

print("Dados de compras inseridos com sucesso!"); 