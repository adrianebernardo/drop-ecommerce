# DRØP — E-Commerce Streetwear 🖤

Plataforma de e-commerce voltada para a cultura streetwear, unindo identidade visual, experiência de navegação e funcionalidades completas de uma aplicação web — do catálogo de produtos ao fechamento de pedidos.

A proposta visual utiliza uma estética streetwear/editorial, com contraste em preto e branco, tipografia **Barlow Condensed**, limites nítidos e foco em uma experiência de navegação moderna.

---

## 📸 Galeria

<div align="center">

### Vitrine Inicial
<img src="./view1.png" alt="Vitrine Inicial" width="700"/>

### Catálogo de Coleções
<img src="./view2.png" alt="Catálogo de Coleções" width="700"/>

### Finalização de Compras
<img src="./view3.png" alt="Finalização de Compras" width="700"/>

</div>

---

## ✨ Funcionalidades

- Exibição de produtos e coleções
- Consulta de produtos através da API
- Cadastro, atualização e exclusão de produtos
- Controle de estoque
- Carrinho de compras
- Finalização de pedidos
- Armazenamento de produtos e pedidos no banco de dados
- Consulta de pedidos através do número do pedido
- Integração entre Front-End, Back-End e banco de dados

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Front-End | HTML5, CSS3, JavaScript Vanilla |
| Back-End | Python, FastAPI, Uvicorn |
| Banco de dados | SQLite |
| Imagens / Assets | Unsplash |
| Inspiração visual / UI | Pinterest |
| AI Assistant utilizado no desenvolvimento | Claude |

---

## 🔌 Backend e API

O backend foi desenvolvido com **FastAPI** e faz a comunicação entre a interface e o banco **SQLite**.

### Endpoints de produtos
```
GET    /products/
GET    /products/{id}
POST   /products/
PUT    /products/{id}
DELETE /products/{id}
```

### Endpoints de pedidos
```
POST   /orders/
GET    /orders/{order_number}
```

Os pedidos recebem automaticamente um identificador no formato `DRP-XXXXXXXX`.

> Exemplo de teste realizado: `DRP-456E9A74`

---

## 🗄️ Banco de dados

O projeto utiliza **SQLite**.

- **`products`** — armazena nome, descrição, preço, estoque, categoria, imagens, tamanhos e status.
- **`orders`** — armazena número do pedido, status, data de criação, dados do cliente, forma de pagamento, itens e valor total.

---

## 📁 Estrutura do projeto

```
drop-ecommerce/
│
├── frontend/
│   ├── assets/
│   ├── css/
│   ├── app.js
│   ├── index.html
│   ├── collections.html
│   ├── checkout.html
│   ├── about.html
│   └── admin.html
│
├── backend/
│   ├── models/
│   │   └── schemas.py
│   ├── routes/
│   │   ├── products.py
│   │   └── orders.py
│   ├── database.py
│   └── main.py
│
├── .gitignore
├── README.md
└── ...
```

---

## 👤 Sobre

A página **About** apresenta a criadora, a proposta do projeto e os créditos. O DRØP não é apenas uma vitrine visual: por trás da interface existe um backend em **FastAPI/Python** e um banco **SQLite** responsáveis por produtos e pedidos.

---

## 🙌 Créditos

- **Backend:** FastAPI (Python)
- **Database:** SQLite
- **AI Assistant:** Claude
- **Inspiração / UI:** Pinterest
- **Assets / Imagens:** Unsplash

---

## 🔗 Links da autora

- **LinkedIn:** [linkedin.com/in/adriane-bernardo](https://www.linkedin.com/in/adriane-bernardo/)
- **GitHub:** [github.com/adrianebernardo](https://github.com/adrianebernardo)
