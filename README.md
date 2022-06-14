# TRON GETEWAY
It is used to work with the TRON node!

> `./demon` | TRON DEMON - It is used to search for transactions by blocks.

> `./balancer` | TRON BALANCER - It is used to transfer crypts from the user's wallet to the main wallet.

## Setup:
>```shell
> # SSH
> git clone git@github.com:xristxgod/TRON-GETEWAY.git
> # HTTPS
> git clone https://github.com/xristxgod/TRON-GETEWAY.git
>```

## Settings in .env file:
> `NETWORK` - Test network or main network. USE: `TESTNET`/`MAINNET` 
> 
> `NODE_URL` - The url from the TRON node. Use your own node. Don't use TRON GRID. Example: `http://tron.mainnet.network.io:8080`
> 
> `API_URL` - The url to which the bot will be accessed to receive: `list of addresses`, `private key at the address`, and `notify about the transfer of funds to the main wallet`. Example: `https://test-api.com`
> 
> `RABBITMQ_URL` - The url for RabbitMQ. The path must be specified the same as in docker-compose. Example: `amqp://username:password@rabbitmq:5672/` 
> 
> `QUEUE_BALANCER` - The queue for rabbitmq in which the demon will send messages to the balancer. Example: `balancer_message` 
> 
> `REDIS_URL` - The url for Redis. The path must be specified the same as in docker-compose. Example: `redis://user:password123@redis:6379/0` 
> 
> `ADMIN_ADDRESS` - The address of the admin wallet to which the money will be sent. Example: `TJH8ss65nzJmeVHYHgCakD1TrBrjYzoLmt` 
> 
> `ADMIN_PRIVATE_KEY` - The private key from the admin wallet. It is used to sign transactions for sending TRX to pay the commission. Example: `Cf2413...a8b1512` 
> 
> `TOKEN_COST_USDT` - The minimum amount from which the transaction will be sent to the admin wallet. Example: `1.2`

## How to run:
> ```shell
> # Run
> docker-compose -f tron-geteway-docker-compose.yml up --build
> # Stop
> docker-compose -f tron-geteway-docker-compose.yml stop
> ```

## Example of transactions in TRON SCAN:
![image](https://user-images.githubusercontent.com/84931791/173503232-97d90d7f-e2b2-4d4f-bb55-3785993d3bff.png)
