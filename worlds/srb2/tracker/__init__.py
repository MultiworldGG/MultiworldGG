


def range_incl(a: int, b: int) -> range:
    return range(a, b+1)


mapping_single: dict[int, int] = {
    125:0,
    1:1,
    2:2,
    3:3,
    4:4,
    5:5,
    6:6,
    7:7,
    8:8,
    9:9,
    10:10,
    11:11,
    12:12,
    13:13,
    14:14,
    0:0,

}

mapping_range: dict[range, int] = {
    range_incl(356, 0): 0

}


def should_change(map_id: int) -> bool:
    if map_id in mapping_single:
        return True
    for rang in mapping_range:
        if map_id in rang:
            return True
    return False


def map_page_index(data: int) -> int:

    if data in mapping_single:
        return mapping_single[data]
    for rang in mapping_range:
        if data in rang:
            return mapping_range[rang]
    return 0
