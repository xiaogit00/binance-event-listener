# binance-event-listener
A service for keeping an open connection and listening to Binance Websockets, and keeping track of status of trades + updating DB.

Most of the code is in `main.py`. sample_api folder contains sample websocket events. 

## Running the code:
- Go to `main.py` and run. But first, need to set up LocalDB and make sure .env files are correct.


## Steps for Setting up Local DB:

### 1. Make sure postgresql and psql (cli) is installed
- `brew install postgresql`
- To start: `brew services start postgresql`
- To stop: `brew services stop postgresql`
- To enter psql in terminal: `psql postgres` -> you're now in postgres! 

### 2. Create the db
- Within terminal (not psql), run `createdb db_name`  
- run `psql -l` to list the DBs created  
- to dropDB: `dropdb db_name`  
- To connect and use a single db: `psql -d database -U user -W` i.e. `psql -d tradingbot -U guoleibing -W`   -> for password, it's usually nothing, just enter

### 3. Operating with the db
- Once inside db, run: `\d` to list all tables
- Create the orders table:

```
CREATE TABLE orders (
	order_id BIGINT,
	status VARCHAR(16),
	direction VARCHAR(6),
	symbol VARCHAR(16),
	order_type VARCHAR(24),
	ask_price DECIMAL,
	filled_price DECIMAL,
	side VARCHAR(4),
	created_at TIMESTAMP,
	updated_at TIMESTAMP
);

```
- Check that orders table created: `SELECT * FROM orders;`

### Optional: Creating some test records:

```sql
INSERT INTO orders VALUES 
(1, 'NEW', 'LONG', 'SOLUSDT', 'MARKET_ORDER', 169.30, 169.50, 'BUY', '2025-05-26 14:00:00', '2025-05-26 14:00:00'),
(1, 'FILLED', 'LONG', 'SOLUSDT', 'MARKET_ORDER', 189.30, 169.50, 'BUY', '2025-05-26 14:00:00', '2025-05-26 13:00:00'),
(1, 'NEW', 'LONG', 'SOLUSDT', 'STOP_ORDER', 173.30, 169.50, 'BUY', '2025-05-26 14:00:00', '2025-05-26 15:00:00');
```

### 4. Ensure that the .env file has the following parameters so that `main.py` can run (edit it as per necessary):  
BINANCE_API_KEY=  
DB_NAME=your_local_db_name  
DB_USER= (tends to be your mac admin user)  
DB_PASSWORD= (tends to be nothing)  
DB_HOST=localhost  
DB_PORT=5432  
