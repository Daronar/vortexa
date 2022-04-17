# Vortexa Programming Assignment - Land Storage

## Context:
We are interested in understanding how sea-borne flows of energy products impact on-land storage reserves.

For this exercise, please assume that the only way by which on-land storage changes is when a vessel loads a product from that port, or when a vessel discharges a product to that port.  

For example, during a cargo movement a vessel loads 100,000 Tons of crude oil from Houston, and discharges it in Rotterdam.  In this case, Houston’s Crude Oil reserves would decrease by 100,000 Tons, and Rotterdam’s would increase by 100,000 Tons.

## Data:
In the `data/` directory you will find 2 files:
* `storage_asof_20200101.parquet` - storage reserves of Crude Oil and Diesel for a set of ports as of 01/01/2020.  This includes the absolute quantity stored, as well as a percentage value, relative to the maximum capacity which the ports can hold for a given product.
* `cargo_movements.parquet` - A series of cargo movements from 01/01/2020 until the end of 14/01/2020.  Each cargo movement represents a vessel loading a product from an origin port (loading_port) and discharging it at a destination port (`discharge_port`).

## Task:
Please write a program which will return a csv file (`storage_asof_20200114.csv`) with the the absolute and relative storage quantities updated to reflect storage levels as of **14/01/2020 00:00:00**.

We are only interested in the storage levels of **Crude Oil and Diesel, at the ports for which we have an opening storage balance.**

Storage levels decrease at the loading port, as soon as the cargo movement starts (`start_timestamp`).  At the discharge port, storage levels only increase once the vessel arrives in port (`end_timestamp`).

## Solution:

### Structure:
Here will be described the structure of project:
 - `src/event_generator/` - this directory contains the abstract class and the realization for event generator from dataframe. I suppose the metrics of ports storages' can be got not only from static files, but also from database or realtime API. So it is enough to write new event generator for such case.
 - `src/event_handlers/` - the main core directory. It contains the class to get events from generator and update the ports' storages' states. Also the special multiprocessing wrapper is available to get events from queue and handle its in parallel with generating process. Such parallelization is not the best practice for real production, but acceptable for the prototyping.
 - `src/event_publisher/` - the multiprocessing wrapper for event generators to generate events in parallel with event handler process.
 - `src/events/` - contains types of event and some enums.
 - `src/resources/` - this directory contains the classes for tracking states of ports and its' storages. Also contains the class for port serialization to dataframe.
 - `src/config.py` - this file contains the class for reading ENV variables from the system. More about app settings in section *Configuration*.
 - `tests/` - contains the ut and it tests for application.
 - `app.py` - main file of application. It contains two realization: as single process and as two processes. The choosing between them is managed by ENV variables.

There are some default variables in the project, f.e. multiprocessing queue size or retry count. Of course, this variables can be not optimal for real production.

### Configuration:
There are some settings to set up the application.
 - **LOG_LEVEL** - set the logging level, default *'DEBUG'*.
 - **MAX_DATETIME** - set the datetime until which the app should be run. By default, *'14/01/2020 00:00:00'*.
 - **PATH_TO_PORTS_FILE** - set the path to init ports' states data file in .parquet format.
 - **PATH_TO_EVENT_FILE** - set the path to file with the information of vessels' operation in .parquet format.
 - **USE_MULTIPROCESSING** - set the setting to use or not to use the multiprocessing in data handling.
 - **PATH_TO_RESULT_FILE** - path to result file, by default, *'./storage_asof_20200114.csv'*.

You can set this ENV variables for running in Docker container using -e options.


### Build, run, test:
For building, running and testing you should have installed Docker, make utility and pytest.

For building run `make build`. It will create Docker image `mp_test_assignment_image`.

For running application run `make run`. The result file in CSV format will be created in the directory `result_from_docker` in your file system.

For testing run `make test`. The tests run in your local system with pytest.

