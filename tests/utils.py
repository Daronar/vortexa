from datetime import datetime, timedelta

import pandas as pd


NUMBER_OF_EVENTS = 5
PORTS_NAMES = ['port0', 'port1', 'port2']
PRODUCT_TYPES = ['crude oil', 'fuel oil', 'diesel']

UNTRACKABLE_PORTS_NAMES = ['port3', 'port4']

BASE_PRODUCT_CRUDE_AMOUNT = 10000
BASE_PRODUCT_DIESEL_AMOUNT = 15000


def generate_events() -> pd.DataFrame:
    df = pd.DataFrame(
        columns=[
            'loading_port', 'start_timestamp', 'discharge_port',
            'end_timestamp', 'product', 'quantity'
        ]
    )
    start_datetime = datetime.now() - timedelta(days=10)
    current_datetime = start_datetime
    ports_pairs = [
        (PORTS_NAMES[0], PORTS_NAMES[1]),
        (PORTS_NAMES[1], PORTS_NAMES[2]),
        (PORTS_NAMES[2], PORTS_NAMES[0]),
    ]
    quantities = [100, 200, 500]

    for event_id in range(NUMBER_OF_EVENTS):
        row = {
            'loading_port': ports_pairs[event_id % 3][0],
            'start_timestamp': current_datetime,
            'discharge_port': ports_pairs[event_id % 3][1],
            'end_timestamp': current_datetime + timedelta(days=3),
            'product':  PRODUCT_TYPES[event_id % 3],
            'quantity': quantities[event_id % 3]
        }
        df = df.append(row, ignore_index=True)
        current_datetime += timedelta(days=2)

    # add untrackable events
    df = df.append(
        {
            'loading_port': PORTS_NAMES[0],
            'start_timestamp': start_datetime + timedelta(days=2),
            'discharge_port': UNTRACKABLE_PORTS_NAMES[0],
            'end_timestamp': start_datetime + timedelta(days=4),
            'product': PRODUCT_TYPES[0],
            'quantity': 300
        },
        ignore_index=True
    )
    df = df.append(
        {
            'loading_port': UNTRACKABLE_PORTS_NAMES[1],
            'start_timestamp': start_datetime + timedelta(days=2),
            'discharge_port': PORTS_NAMES[1],
            'end_timestamp': start_datetime + timedelta(days=4),
            'product': PRODUCT_TYPES[2],
            'quantity': 100
        },
        ignore_index=True
    )

    return df


def generate_ports() -> pd.DataFrame:
    port_df = pd.DataFrame(columns=['port', 'crude_absolute', 'crude_relative', 'diesel_absolute', 'diesel_relative'])
    for idx, port_name in enumerate(PORTS_NAMES):
        port_df = port_df.append(
            {
                'port': port_name,
                'crude_absolute': BASE_PRODUCT_CRUDE_AMOUNT * (1 + idx),
                'crude_relative': 0.1,
                'diesel_absolute': BASE_PRODUCT_DIESEL_AMOUNT * (1 + idx),
                'diesel_relative': 0.2,
            },
            ignore_index=True
        )
    return port_df


def generate_full_result_ports():
    # -10d port_0 - 100 crude oil
    # - 8d port_1 - 200 fuel oil
    # - 8d port_0 - 300 crude oil
    # - 7d port_1 + 100 crude oil
    # - 6d port_2 - 500 diesel
    # - 6d port_1 + 300 diesel
    # - 5d port_2 + 200 fuel oil
    # - 4d port_0 - 100 crude oil
    # - 3d port_0 + 500  diesel
    # - 2d port_1 - 200 fuel oil
    # - 1d port_1 + 100 crude oil
    # + 1d port_2 + 200 fuel oil
    # ======
    # port0 -500 crude +500 diesel
    # port1 -400 fuel +200 crude +100 diesel
    # port2 +400 fuel -500 diesel
    port_df = pd.DataFrame(columns=['port', 'crude_absolute', 'crude_relative', 'diesel_absolute', 'diesel_relative'])
    port_df = port_df.append(
        {
            'port': PORTS_NAMES[0],
            'crude_absolute': BASE_PRODUCT_CRUDE_AMOUNT - 500,
            'crude_relative': (BASE_PRODUCT_CRUDE_AMOUNT - 500) / int(BASE_PRODUCT_CRUDE_AMOUNT / 0.1),
            'diesel_absolute': BASE_PRODUCT_DIESEL_AMOUNT + 500,
            'diesel_relative': (BASE_PRODUCT_DIESEL_AMOUNT + 500) / int(BASE_PRODUCT_DIESEL_AMOUNT / 0.2),
        },
        ignore_index=True
    )
    port_df = port_df.append(
        {
            'port': PORTS_NAMES[1],
            'crude_absolute': 2 * BASE_PRODUCT_CRUDE_AMOUNT + 200,
            'crude_relative': (2 * BASE_PRODUCT_CRUDE_AMOUNT + 200) / int(2 * BASE_PRODUCT_CRUDE_AMOUNT / 0.1),
            'diesel_absolute': 2 * BASE_PRODUCT_DIESEL_AMOUNT + 100,
            'diesel_relative': (2 * BASE_PRODUCT_DIESEL_AMOUNT + 100) / int(2 * BASE_PRODUCT_DIESEL_AMOUNT / 0.2),
        },
        ignore_index=True
    )
    port_df = port_df.append(
        {
            'port': PORTS_NAMES[2],
            'crude_absolute': 3 * BASE_PRODUCT_CRUDE_AMOUNT,
            'crude_relative': 0.1,
            'diesel_absolute': 3 * BASE_PRODUCT_DIESEL_AMOUNT - 500,
            'diesel_relative': (3 * BASE_PRODUCT_DIESEL_AMOUNT - 500) / int(3 * BASE_PRODUCT_DIESEL_AMOUNT / 0.2),
        },
        ignore_index=True
    )
    return port_df


def generate_partial_result_ports():
    # -10d port_0 - 100 crude oil
    # - 8d port_1 - 200 fuel oil
    # - 8d port_0 - 300 crude oil
    # - 7d port_1 + 100 crude oil
    # - 6d port_2 - 500 diesel
    # - 6d port_1 + 300 diesel
    # =====partitial=====
    # port0 -400 crude
    # port1 -200 fuel +100 crude +100 diesel
    # port2 -500 diesel

    port_df = pd.DataFrame(columns=['port', 'crude_absolute', 'crude_relative', 'diesel_absolute', 'diesel_relative'])
    port_df = port_df.append(
        {
            'port': PORTS_NAMES[0],
            'crude_absolute': BASE_PRODUCT_CRUDE_AMOUNT - 400,
            'crude_relative': (BASE_PRODUCT_CRUDE_AMOUNT - 400) / int(BASE_PRODUCT_CRUDE_AMOUNT / 0.1),
            'diesel_absolute': BASE_PRODUCT_DIESEL_AMOUNT,
            'diesel_relative': BASE_PRODUCT_DIESEL_AMOUNT / int(BASE_PRODUCT_DIESEL_AMOUNT / 0.2),
        },
        ignore_index=True
    )
    port_df = port_df.append(
        {
            'port': PORTS_NAMES[1],
            'crude_absolute': 2 * BASE_PRODUCT_CRUDE_AMOUNT + 100,
            'crude_relative': (2 * BASE_PRODUCT_CRUDE_AMOUNT + 100) / int(2 * BASE_PRODUCT_CRUDE_AMOUNT / 0.1),
            'diesel_absolute': 2 * BASE_PRODUCT_DIESEL_AMOUNT + 100,
            'diesel_relative': (2 * BASE_PRODUCT_DIESEL_AMOUNT + 100) / int(2 * BASE_PRODUCT_DIESEL_AMOUNT / 0.2),
        },
        ignore_index=True
    )
    port_df = port_df.append(
        {
            'port': PORTS_NAMES[2],
            'crude_absolute': 3 * BASE_PRODUCT_CRUDE_AMOUNT,
            'crude_relative': 0.1,
            'diesel_absolute': 3 * BASE_PRODUCT_DIESEL_AMOUNT - 500,
            'diesel_relative': (3 * BASE_PRODUCT_DIESEL_AMOUNT - 500) / int(3 * BASE_PRODUCT_DIESEL_AMOUNT / 0.2),
        },
        ignore_index=True
    )
    return port_df

