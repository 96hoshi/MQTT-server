# MCPS Project: Plant Monitoring :seedling:

*Mobile and Cyber-Phisical Systems Project by Fiorini, Lo Cascio*

## MQTT-Server

Server as main system logic for sensors relevations.  
It also contains the Telegram Bot to inteface the user with several commands.  
The bot is available at the following link:  https://t.me/plant_monitorbot.

### Bot Commands

**/help**: Shows a list of all possible commands  
**/start**: Starts the monitoring of your plant  
**/status**: Gives you the status of your plant  
**/avgtemp**: Returns the average temperature of the last hour  
**/avghum**: Returns the average humidity of the last hour  
**/lasttemp**: Shows the last recorded temperature  
**/lasthum**: Shows the last recorded humidity  
**/lastwater**: Shows the last time you watered your plant  

## Links to the project repositories

- [_MQTT Server_](https://github.com/96hoshi/MQTT-server) - Server part as main system logic and the Telegram Bot to inteface the user.
- [_MQTT Client_](https://github.com/dufnill/MQTT-client) - Client part related to sensors relevations and comunications with the MQTT Broker.
