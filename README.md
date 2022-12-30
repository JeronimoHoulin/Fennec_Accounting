# Fennec_Accounting
This repo is holding all logic that runs once the futures contract reach maturity, and user's positions have to be closed to gather interest.
Because markets can close a little lower and / or higher than expected, these accounting scripts make sure that users have their capital available, 
and interests as close as the once he expected to recive, as well as sending them their requested withdrawal money.
The main.py calculates the final position for each user. 
The distributino script send's fund's back to users Web3 wallets.
