The API server will start on `http://localhost:5000`

## 🔌 API Endpoints

### Authentication
- `POST /api/login` - User authentication and JWT token generation

### Products (Medicines)
- `GET /api/products/` - Fetch medicines with filtering and pagination
- `GET /api/products/{id}` - Get specific product details with relations

### Reviews & Ratings
- `GET /api/reviews/` - Get product reviews with pagination
- `GET /api/reviews/{id}` - Get specific review details
- `GET /api/reviews/stats/{product_id}` - Get review statistics and rating distribution

### Salt Composition
- `GET /api/salts/` - Get tablet salt content information
- `GET /api/salts/{id}` - Get specific salt information

### Product Descriptions
- `GET /api/description/` - Get product descriptions by type
- `GET /api/description/{id}` - Get specific description

## 🔧 Configuration

### Environment Configurations
- **Development**: Debug mode enabled, development database
- **Production**: Optimized for production deployment
- **Testing**: Separate test database configuration

### JWT Configuration
- **Access Token**: 10 minutes (configurable)
- **Refresh Token**: 30 days (configurable)
- **Secret Keys**: Environment-based for security

### CORS Configuration
Configured to accept requests from:
- `http://localhost:3000` (React development server)
