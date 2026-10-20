from random import Random

from Options import OptionError
from . import Spawn
from .warp_platforms import WarpPlatforms


def test_vanilla_get_connected_warp() -> None:
    wp = WarpPlatforms()
    wp.apply_vanilla_warp_platform_mapping()

    assert wp.get_connected_warp("SS") == "ST"
    assert wp.get_connected_warp("ET") == "ETT"
    assert wp.get_connected_warp("BHNG") == "WHS"
    assert wp.get_connected_warp("BHF") == "BHT"


def test_vanilla_connection_exists() -> None:
    wp = WarpPlatforms()
    wp.apply_vanilla_warp_platform_mapping()

    # trivial, warpless, invalid connections
    assert wp.shipless_connection_exists("Sun Station", "Sun Station")
    assert wp.shipless_connection_exists("Hourglass Twins", "Hourglass Twins")
    assert wp.shipless_connection_exists("Sun Station", "Dark Bramble") == False
    assert wp.shipless_connection_exists("Sun Station", "invalid region name") == False

    # direct connections
    assert wp.shipless_connection_exists("Sun Station", "Hourglass Twins")
    assert wp.shipless_connection_exists("Hourglass Twins", "Sun Station")
    assert wp.shipless_connection_exists("Hourglass Twins", "Ash Twin Interior")
    assert wp.shipless_connection_exists("Hourglass Twins", "Timber Hearth")
    assert wp.shipless_connection_exists("Hourglass Twins", "Hanging City Ceiling")
    assert wp.shipless_connection_exists("Hourglass Twins", "Giant's Deep")

    # simple indirect connections: warp to Ash Twin, then use a different Ash Twin tower
    assert wp.shipless_connection_exists("Sun Station", "Ash Twin Interior")
    assert wp.shipless_connection_exists("Sun Station", "Timber Hearth")
    assert wp.shipless_connection_exists("Sun Station", "Hanging City Ceiling")
    assert wp.shipless_connection_exists("Sun Station", "Giant's Deep")

    # connections involving HCC -> BH and HCC -> WHS falls
    assert wp.shipless_connection_exists("Hanging City Ceiling", "Brittle Hollow")
    assert wp.shipless_connection_exists("Hanging City Ceiling", "White Hole Station")
    assert wp.shipless_connection_exists("Sun Station", "Brittle Hollow")
    assert wp.shipless_connection_exists("Sun Station", "White Hole Station")
    assert wp.shipless_connection_exists("Brittle Hollow", "White Hole Station")
    assert wp.shipless_connection_exists("Brittle Hollow", "Hanging City Ceiling") == False
    assert wp.shipless_connection_exists("Brittle Hollow", "Sun Station") == False


def test_fixed_seed_get_connected_warp() -> None:
    wp = WarpPlatforms()
    r = Random()
    r.seed(1)
    wp.randomize_unmapped_warps(r, Spawn(Spawn.option_vanilla))

    assert wp.get_connected_warp("SS") == "ET"
    assert wp.get_connected_warp("ATP") == "GDT"
    assert wp.get_connected_warp("BHF") == "ETT"
    assert wp.get_connected_warp("BHT") == "ATT"
    assert wp.get_connected_warp("TH") == "GD"
    assert wp.get_connected_warp("WHS") == "THT"
    assert wp.get_connected_warp("ST") == "BHNG"


def test_fixed_seed_connection_exists() -> None:
    wp = WarpPlatforms()
    r = Random()
    # this seed has WHS warp to an Ash Twin tower, which is what we want to test
    # it also has Sun Station warp to Hourglass Twins, so we can leave many control asserts unchanged
    r.seed(1)
    wp.randomize_unmapped_warps(r, Spawn(Spawn.option_vanilla))

    # trivial, warpless, invalid connections
    assert wp.shipless_connection_exists("Sun Station", "Sun Station")
    assert wp.shipless_connection_exists("Hourglass Twins", "Hourglass Twins")
    assert wp.shipless_connection_exists("Sun Station", "Dark Bramble") == False
    assert wp.shipless_connection_exists("Sun Station", "invalid region name") == False

    # direct connections
    assert wp.shipless_connection_exists("Sun Station", "Hourglass Twins")
    assert wp.shipless_connection_exists("Hourglass Twins", "Sun Station")
    assert wp.shipless_connection_exists("Hourglass Twins", "Ash Twin Interior")
    assert wp.shipless_connection_exists("Hourglass Twins", "Hanging City Ceiling")
    # because THT <-> WHS in this seed
    assert wp.shipless_connection_exists("Hourglass Twins", "White Hole Station")
    # TH <-> GD are the only "isolated" warps in this seed
    assert wp.shipless_connection_exists("Timber Hearth", "Giant's Deep")
    assert wp.shipless_connection_exists("Giant's Deep", "Timber Hearth")

    # simple indirect connections: warp to Ash Twin, then use a different Ash Twin tower
    assert wp.shipless_connection_exists("Sun Station", "Ash Twin Interior")
    assert wp.shipless_connection_exists("Sun Station", "Hanging City Ceiling")
    # because THT <-> WHS in this seed
    assert wp.shipless_connection_exists("Sun Station", "White Hole Station")

    # connections involving HCC -> BH and HCC -> WHS falls
    assert wp.shipless_connection_exists("Hanging City Ceiling", "Brittle Hollow")
    assert wp.shipless_connection_exists("Hanging City Ceiling", "White Hole Station")
    assert wp.shipless_connection_exists("Sun Station", "Brittle Hollow")
    assert wp.shipless_connection_exists("Sun Station", "White Hole Station")
    assert wp.shipless_connection_exists("Brittle Hollow", "White Hole Station")
    # these are now True because THT <-> WHS in this seed
    assert wp.shipless_connection_exists("Brittle Hollow", "Hanging City Ceiling")
    assert wp.shipless_connection_exists("Brittle Hollow", "Sun Station")


def test_warp_plando() -> None:
    wp = WarpPlatforms()
    wp.apply_warp_plando({"ATP": "ATT", "TH": "GD", "BHNG": "WHS"})
    wp.randomize_unmapped_warps(Random(), Spawn(Spawn.option_vanilla))
    # Test plando working.
    assert wp.get_connected_warp("ATP") == "ATT"
    # Test that non-plando platforms got mapped.
    assert wp.get_connected_warp("ETT") is not None
    # Test that every platform is mapped once.
    all_warps = [w for t in wp.mappings for w in t]
    assert len(all_warps) == len(set(all_warps))


def test_warp_plando_invalid_input() -> None:
    wp = WarpPlatforms()
    try:
        wp.apply_warp_plando({"ATP": "ATP"})
    except OptionError:
        pass
    else:
        raise Exception("Duplicate warp did not cause error.")


def test_ac_warps() -> None:
    wp = WarpPlatforms()
    r = Random()
    wp.apply_ac_modifications(r)
    wp.randomize_unmapped_warps(r, Spawn(Spawn.option_vanilla))
    assert wp.shipless_connection_exists("Hourglass Twins", "Timber Hearth")
