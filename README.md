# Huobi Market Data

Coding challenge by SingAlliance
</br></br>



## Current Perpetual Future Contracts
The data fields present would be in found under kline data which is found in  `/market/history/kline` REST API interface, and the data fields are as follows:

| id | open | close | high | low | vol | amount |
| -- | -- | -- | -- | -- | -- | -- |
| 1621267200 | 43342.5 | 45004.68 | 45781.52 | 42106.0 | 1.5694329022947967E9 | 35623.935414808795 |
</br>

## Periods
Periods are supported as follows: 
`1min`, `5min`, `15min`, `30min`, `60min`, `4hour`, `1day`, `1mon`, `1week`, `1year`
</br></br>

## Data collected
Houbi provides a maximum of 2000 data fields per get request. For each hour, we send a get request of size 2000 from 2022-11-01 at time 00:00:00+00:00 to 2022-12-01 at time 23:00:00+00:00. The size, tokens and dates could be altered in the first 20 lines of code to your liking under `size` , `symbols`, `start_date` and `end_date`.

## Mean - Variance Optimization
Only the `close` prices are collected from the data. The code uses the `scipy` library to run the optimization. A dictionary of the weights will be printed onto the terminal. An efficient fronter is also plotted using `matplotlib` library and will be shown. An image is also saved as `efficient_frontier.png`. 

## HTTP codes
Appropriate http error messages are handled in the file.


## How to Run Code

1. Git clone this repository
2. install the libraries under 'requirements.txt'
3. Run file on shell `(works on any OS)` **(either python or python3 according to your version)**
    ```
        python challenge.py
    ```

4. Image of efficient file is saved in the folder
