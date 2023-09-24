from argparse import ArgumentParser, ArgumentTypeError
from collections import defaultdict
from itertools import islice
from math import ceil
from multiprocessing import Manager, Process
import os
import warnings

from geopy import distance
import pandas as pd


def validate_file(filename):
    filepath = os.path.abspath(filename)
    if not os.path.exists(filepath):
        raise ArgumentTypeError(f'{filename} does not exist')
    return filepath


def get_stops_df(filename, usecols):
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        stops_df = pd.read_excel(
            filename,
            usecols=usecols,
            skiprows=[1]
        )

    return stops_df


def get_street_with_most_stops(stop_addresses):
    street_stops_count = defaultdict(int)
    for address in stop_addresses:
        if not isinstance(address, str):
            continue
        street = address.split(',')[0]
        street_stops_count[street] += 1

    return max(street_stops_count, key=street_stops_count.get)


def get_bus_stop_locs(bus_stops_df):
    districts = bus_stops_df['District'].unique()

    stop_locs = []

    for district in districts:
        district_df = bus_stops_df[bus_stops_df.District == district]
        stop_locs_aggregated = district_df.groupby('StationName').agg(
            {'Longitude_WGS84': 'mean', 'Latitude_WGS84': 'mean'}
        ).reset_index()
        stop_locs.extend(
            list(zip(
                stop_locs_aggregated.Longitude_WGS84,
                stop_locs_aggregated.Latitude_WGS84
            ))
        )

    return stop_locs


def get_subway_stations(subway_stations_df):
    station_locs_aggregated = subway_stations_df.groupby('NameOfStation').agg(
        {'Longitude_WGS84': 'mean', 'Latitude_WGS84': 'mean'}
    ).reset_index()
    stations = {
        name: (lon, lat)
        for name, lon, lat
        in zip(
            station_locs_aggregated.NameOfStation,
            station_locs_aggregated.Longitude_WGS84,
            station_locs_aggregated.Latitude_WGS84
            )
    }

    return stations


def count_stops_near_the_stations_chunk(
    stations_with_loc,
    stop_locs,
    stops_near_the_stations_chunks,
    proc_index
):
    stops_near_the_stations = defaultdict(int)

    for station in stations_with_loc:
        for loc in stop_locs:
            if distance.distance(stations_with_loc[station], loc).km < 0.5:
                stops_near_the_stations[station] += 1

    stops_near_the_stations_chunks[proc_index] = stops_near_the_stations


def split_dict(dictionary, chunk_size):
    chunks = []
    chunks_count = ceil(len(dictionary) / chunk_size)

    for i in range(chunks_count):
        chunks.append({
            key: dictionary[key]
            for key
            in islice(dictionary, i * chunk_size, (i + 1) * chunk_size)}
        )

    return chunks


def count_stops_near_the_stations(stations_with_loc, stop_locs, proc_count=10):
    stops_near_the_stations = {}

    chunk_size = ceil(len(stations_with_loc) / proc_count)
    stations_with_loc_chunks = split_dict(stations_with_loc, chunk_size)

    with Manager() as manager:
        processes = [None] * proc_count
        stops_near_the_stations_chunks = manager.list()
        stops_near_the_stations_chunks.extend([None] * proc_count)

        for i in range(proc_count):
            processes[i] = Process(
                target=count_stops_near_the_stations_chunk,
                args=(
                    stations_with_loc_chunks[i],
                    stop_locs,
                    stops_near_the_stations_chunks,
                    i
                )
            )
            processes[i].start()

        for i in range(proc_count):
            processes[i].join()

        for i in range(proc_count):
            stops_near_the_stations.update(stops_near_the_stations_chunks[i])

    return stops_near_the_stations


def get_stations_sorted_by_stop_count(stops_near_the_stations, count):
    return dict([
        (station, stop_count) for station, stop_count
        in sorted(
            stops_near_the_stations.items(), key=lambda x: x[1], reverse=True
        )
    ][:count])


def main():
    parser = ArgumentParser(description='Simple stops stat calculator')
    parser.add_argument(
        '-b', '--bus_stops_file',
        required=True,
        type=validate_file,
        help='Bus stops *.xlsx file'
    )
    parser.add_argument(
        '-s', '--subway_stations_file',
        required=True,
        type=validate_file,
        help='Subway stations *.xlsx file'
    )
    args = parser.parse_args()

    bus_stops_df = get_stops_df(
        args.bus_stops_file,
        'C,D,F,H,N'
    )
    subway_stations_df = get_stops_df(
        args.subway_stations_file,
        'F,G,I,Q'
    )

    bus_stop_addresses = bus_stops_df['PlaceDescription'].unique()
    bus_stop_locs = get_bus_stop_locs(bus_stops_df)

    stations_with_escalators_under_repair = (
        subway_stations_df.dropna()['NameOfStation'].unique()
    )

    subway_stations_with_loc = get_subway_stations(subway_stations_df)
    stops_near_the_stations = count_stops_near_the_stations(
        subway_stations_with_loc,
        bus_stop_locs
    )
    ten_stations_with_most_stops = get_stations_sorted_by_stop_count(
        stops_near_the_stations,
        10
    )

    print(f'Bus stop count: {len(bus_stop_addresses)}')
    print()
    print(
        f'Street with most bus stops: '
        f'{get_street_with_most_stops(bus_stop_addresses)}'
    )
    print()
    print(
        f'Subway stations with escalators under repair: '
        f'{", ".join(stations_with_escalators_under_repair)}'
    )
    print()
    print(
        '10 stations with most stops nearby:',
        *[
            f'\t{station}: {stop_count}'
            for station, stop_count
            in ten_stations_with_most_stops.items()
        ],
        sep='\n'
    )


if __name__ == '__main__':
    main()
