"""Update 1.03 balance changes, grouped by planet and named gameplay effect.

Maintenance guide:
* offsets are SNR2-relative; US, EU and JP are explicitly labelled.
* original contains exact retail words used for signature validation.
* replacement contains the normal patched values; boss is an optional override.
* damage groups list levels 1, 2, 3, 4 with a 0x10-byte row stride.
* f32(...) exposes gameplay numbers; instruction patches remain hexadecimal.
* omitted EU/JP word lists inherit US. Explicit EU values retain 50 Hz scaling.

Some float words intentionally remain hex: rounding them to a short decimal
would change the existing patch. Do not recompute the stored EU compensation.
See docs/balance_patch.md and balance_patch_sources.json for provenance.
"""

from .balance_types import PatchGroup, RegionalOffsets, RegionalWords, f32


POKITARU = (
    PatchGroup(
        name="Lacerator damage",
        offsets=RegionalOffsets(us=0x218FEC, eu=0x21A40C, jp=0x21968C),
        original=RegionalWords(
            us=(0x3F800000, 0x40400000, 0x40A00000, 0x40800000),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(2.0), f32(3.0), f32(6.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Lacerator fire interval",
        offsets=RegionalOffsets(us=0x21CB08, eu=0x21DF28, jp=0x21D1A8),
        original=RegionalWords(
            us=(0x3F800000,),
        ),
        replacement=RegionalWords(
            us=(f32(0.4),),
        ),
    ),
    PatchGroup(
        name="Acid Bomb impact damage",
        offsets=RegionalOffsets(us=0x218D6C, eu=0x21A18C, jp=0x21940C),
        original=RegionalWords(
            us=(0x40200000, 0x40A00000, 0x41200000, 0x41400000),
        ),
        replacement=RegionalWords(
            us=(f32(4.0), f32(6.0), f32(8.0), f32(10.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Acid Bomb trail damage",
        offsets=RegionalOffsets(us=0x218DEC, eu=0x21A20C, jp=0x21948C),
        original=RegionalWords(
            us=(0x3D4CCCCE, 0x3DCCCCCE, 0x3E4CCCCE, 0x3ECCCCCE),
            eu=(0x3D75C28F, 0x3DF5C28F, 0x3E75C28F, 0x3EF5C28F),
        ),
        replacement=RegionalWords(
            us=(f32(0.25), f32(0.5), f32(0.8), f32(1.0)),
            eu=(f32(0.3), f32(0.6), 0x3F75C290, f32(1.2)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun damage",
        offsets=RegionalOffsets(us=0x2190EC, eu=0x21A50C, jp=0x21978C),
        original=RegionalWords(
            us=(0x40800000, 0x41000000, 0x41400000, 0x41800000),
        ),
        replacement=RegionalWords(
            us=(f32(13.0), f32(17.0), f32(22.0), f32(28.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun fire interval instructions",
        offsets=RegionalOffsets(us=0x14F110, eu=0x150428, jp=0x14F5C8),
        original=RegionalWords(
            us=(0x3C013FC0, 0x342100FC, 0x44810000),
            eu=(0x3C013FC0, 0x342100FA, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013F95, 0x34215555, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Shock Rocket fire rate instruction",
        offsets=RegionalOffsets(us=0x1AB88C, eu=0x1ACD3C, jp=0x1ABE2C),
        original=RegionalWords(
            us=(0x3C014270,),
        ),
        replacement=RegionalWords(
            us=(0x3C0141F0,),
        ),
    ),
    PatchGroup(
        name="Helipack vertical movement instructions",
        offsets=RegionalOffsets(us=0x042EB8, eu=0x042FF8, jp=0x042FC0),
        original=RegionalWords(
            us=(0x3C01BCA3, 0x3421D70A, 0x44810000),
            eu=(0x3C01BCC4, 0x34219BA5, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C01BD93, 0x342174BC, 0x44810000),
            eu=(0x3C01BDB0, 0x3421F27C, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Helipack forward movement instructions",
        offsets=RegionalOffsets(us=0x0480C4, eu=0x04820C, jp=0x0481CC),
        original=RegionalWords(
            us=(0x3C013CF5, 0x3421C290, 0x44810000),
            eu=(0x3C013D13, 0x342174BC, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013E25, 0x3421E354, 0x44810000),
            eu=(0x3C013E47, 0x342110CB, 0x44810000),
        ),
    ),
)


RYLLUS = (
    PatchGroup(
        name="Lacerator damage",
        offsets=RegionalOffsets(us=0x22DF6C, eu=0x22F40C, jp=0x22E68C),
        original=RegionalWords(
            us=(0x3F800000, 0x40400000, 0x40A00000, 0x40800000),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.25), f32(2.0), f32(4.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Lacerator fire interval",
        offsets=RegionalOffsets(us=0x231DD8, eu=0x233278, jp=0x2324F8),
        original=RegionalWords(
            us=(0x3F800000,),
        ),
        replacement=RegionalWords(
            us=(f32(0.4),),
        ),
    ),
    PatchGroup(
        name="Acid Bomb impact damage",
        offsets=RegionalOffsets(us=0x22DCEC, eu=0x22F18C, jp=0x22E40C),
        original=RegionalWords(
            us=(0x40200000, 0x40A00000, 0x41200000, 0x41400000),
        ),
        replacement=RegionalWords(
            us=(f32(3.0), f32(4.5), f32(6.0), f32(7.5)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Acid Bomb trail damage",
        offsets=RegionalOffsets(us=0x22DD6C, eu=0x22F20C, jp=0x22E48C),
        original=RegionalWords(
            us=(0x3D4CCCCE, 0x3DCCCCCE, 0x3E4CCCCE, 0x3ECCCCCE),
            eu=(0x3D75C28F, 0x3DF5C28F, 0x3E75C28F, 0x3EF5C28F),
        ),
        replacement=RegionalWords(
            us=(f32(0.09375), f32(0.1875), f32(0.3), f32(0.375)),
            eu=(f32(0.1125), f32(0.225), f32(0.36), f32(0.45)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun damage",
        offsets=RegionalOffsets(us=0x22E06C, eu=0x22F50C, jp=0x22E78C),
        original=RegionalWords(
            us=(0x40800000, 0x41000000, 0x41400000, 0x41800000),
        ),
        replacement=RegionalWords(
            us=(f32(13.0), f32(17.0), f32(22.0), f32(28.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun fire interval instructions",
        offsets=RegionalOffsets(us=0x155988, eu=0x156CB0, jp=0x155E68),
        original=RegionalWords(
            us=(0x3C013FC0, 0x342100FC, 0x44810000),
            eu=(0x3C013FC0, 0x342100FA, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013F95, 0x34215555, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Scorcher damage",
        offsets=RegionalOffsets(us=0x22E0EC, eu=0x22F58C, jp=0x22E80C),
        original=RegionalWords(
            us=(0x3F088889, 0x3F4CCCCE, 0x3F888889, 0x40088889),
            eu=(0x3F23D70A, 0x3F75C28F, 0x3FA3D70A, 0x4023D70A),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.5), f32(2.0), f32(3.0)),
            eu=(f32(1.2), f32(1.8), f32(2.4), f32(3.6)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Shock Rocket fire rate instruction",
        offsets=RegionalOffsets(us=0x1C9874, eu=0x1CAD64, jp=0x1C9EB4),
        original=RegionalWords(
            us=(0x3C014270,),
        ),
        replacement=RegionalWords(
            us=(0x3C0141F0,),
        ),
    ),
    PatchGroup(
        name="Helipack vertical movement instructions",
        offsets=RegionalOffsets(us=0x047E40, eu=0x047F80, jp=0x047F48),
        original=RegionalWords(
            us=(0x3C01BCA3, 0x3421D70A, 0x44810000),
            eu=(0x3C01BCC4, 0x34219BA5, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C01BD93, 0x342174BC, 0x44810000),
            eu=(0x3C01BDB0, 0x3421F27C, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Helipack forward movement instructions",
        offsets=RegionalOffsets(us=0x04D04C, eu=0x04D194, jp=0x04D154),
        original=RegionalWords(
            us=(0x3C013CF5, 0x3421C290, 0x44810000),
            eu=(0x3C013D13, 0x342174BC, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013E25, 0x3421E354, 0x44810000),
            eu=(0x3C013E47, 0x342110CB, 0x44810000),
        ),
    ),
)


KALIDON = (
    PatchGroup(
        name="Lacerator damage",
        offsets=RegionalOffsets(us=0x231EEC, eu=0x23340C, jp=0x23240C),
        original=RegionalWords(
            us=(0x3F800000, 0x40400000, 0x40A00000, 0x40800000),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.25), f32(3.0), f32(5.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Lacerator fire interval",
        offsets=RegionalOffsets(us=0x235EA8, eu=0x2373C8, jp=0x2363C8),
        original=RegionalWords(
            us=(0x3F800000,),
        ),
        replacement=RegionalWords(
            us=(f32(0.4),),
        ),
    ),
    PatchGroup(
        name="Acid Bomb impact damage",
        offsets=RegionalOffsets(us=0x231C6C, eu=0x23318C, jp=0x23218C),
        original=RegionalWords(
            us=(0x40200000, 0x40A00000, 0x41200000, 0x41400000),
        ),
        replacement=RegionalWords(
            us=(f32(3.0), f32(4.5), f32(6.0), f32(7.5)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Acid Bomb trail damage",
        offsets=RegionalOffsets(us=0x231CEC, eu=0x23320C, jp=0x23220C),
        original=RegionalWords(
            us=(0x3D4CCCCE, 0x3DCCCCCE, 0x3E4CCCCE, 0x3ECCCCCE),
            eu=(0x3D75C28F, 0x3DF5C28F, 0x3E75C28F, 0x3EF5C28F),
        ),
        replacement=RegionalWords(
            us=(f32(0.09375), f32(0.1875), f32(0.3), f32(0.375)),
            eu=(f32(0.1125), f32(0.225), f32(0.36), f32(0.45)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun damage",
        offsets=RegionalOffsets(us=0x231FEC, eu=0x23350C, jp=0x23250C),
        original=RegionalWords(
            us=(0x40800000, 0x41000000, 0x41400000, 0x41800000),
        ),
        replacement=RegionalWords(
            us=(f32(13.0), f32(17.0), f32(22.0), f32(28.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun fire interval instructions",
        offsets=RegionalOffsets(us=0x14E5A0, eu=0x14F8C8, jp=0x14EA60),
        original=RegionalWords(
            us=(0x3C013FC0, 0x342100FC, 0x44810000),
            eu=(0x3C013FC0, 0x342100FA, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013F95, 0x34215555, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Scorcher damage",
        offsets=RegionalOffsets(us=0x23206C, eu=0x23358C, jp=0x23258C),
        original=RegionalWords(
            us=(0x3F088889, 0x3F4CCCCE, 0x3F888889, 0x40088889),
            eu=(0x3F23D70A, 0x3F75C28F, 0x3FA3D70A, 0x4023D70A),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.5), f32(2.0), f32(3.0)),
            eu=(f32(1.2), f32(1.8), f32(2.4), f32(3.6)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Shock Rocket fire rate instruction",
        offsets=RegionalOffsets(us=0x1BD13C, eu=0x1BE69C, jp=0x1BD57C),
        original=RegionalWords(
            us=(0x3C014270,),
        ),
        replacement=RegionalWords(
            us=(0x3C0141F0,),
        ),
    ),
    PatchGroup(
        name="Helipack vertical movement instructions",
        offsets=RegionalOffsets(us=0x041178, eu=0x0412B8, jp=0x041280),
        original=RegionalWords(
            us=(0x3C01BCA3, 0x3421D70A, 0x44810000),
            eu=(0x3C01BCC4, 0x34219BA5, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C01BD93, 0x342174BC, 0x44810000),
            eu=(0x3C01BDB0, 0x3421F27C, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Helipack forward movement instructions",
        offsets=RegionalOffsets(us=0x046384, eu=0x0464CC, jp=0x04648C),
        original=RegionalWords(
            us=(0x3C013CF5, 0x3421C290, 0x44810000),
            eu=(0x3C013D13, 0x342174BC, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013E25, 0x3421E354, 0x44810000),
            eu=(0x3C013E47, 0x342110CB, 0x44810000),
        ),
    ),
)


DREAMTIME = (
    PatchGroup(
        name="Lacerator damage",
        offsets=RegionalOffsets(us=0x207EEC, eu=0x20938C, jp=0x20858C),
        original=RegionalWords(
            us=(0x3F800000, 0x40400000, 0x40A00000, 0x40800000),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.25), f32(3.0), f32(5.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Lacerator fire interval",
        offsets=RegionalOffsets(us=0x20B958, eu=0x20CDF8, jp=0x20BFF8),
        original=RegionalWords(
            us=(0x3F800000,),
        ),
        replacement=RegionalWords(
            us=(f32(0.4),),
        ),
    ),
    PatchGroup(
        name="Acid Bomb impact damage",
        offsets=RegionalOffsets(us=0x207C6C, eu=0x20910C, jp=0x20830C),
        original=RegionalWords(
            us=(0x40200000, 0x40A00000, 0x41200000, 0x41400000),
        ),
        replacement=RegionalWords(
            us=(f32(3.0), f32(4.5), f32(6.0), f32(7.5)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Acid Bomb trail damage",
        offsets=RegionalOffsets(us=0x207CEC, eu=0x20918C, jp=0x20838C),
        original=RegionalWords(
            us=(0x3D4CCCCE, 0x3DCCCCCE, 0x3E4CCCCE, 0x3ECCCCCE),
            eu=(0x3D75C28F, 0x3DF5C28F, 0x3E75C28F, 0x3EF5C28F),
        ),
        replacement=RegionalWords(
            us=(f32(0.09375), f32(0.1875), f32(0.3), f32(0.375)),
            eu=(f32(0.1125), f32(0.225), f32(0.36), f32(0.45)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun damage",
        offsets=RegionalOffsets(us=0x207FEC, eu=0x20948C, jp=0x20868C),
        original=RegionalWords(
            us=(0x40800000, 0x41000000, 0x41400000, 0x41800000),
        ),
        replacement=RegionalWords(
            us=(f32(13.0), f32(17.0), f32(22.0), f32(28.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun fire interval instructions",
        offsets=RegionalOffsets(us=0x14AB00, eu=0x14BE18, jp=0x14AFE8),
        original=RegionalWords(
            us=(0x3C013FC0, 0x342100FC, 0x44810000),
            eu=(0x3C013FC0, 0x342100FA, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013F95, 0x34215555, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Scorcher damage",
        offsets=RegionalOffsets(us=0x20806C, eu=0x20950C, jp=0x20870C),
        original=RegionalWords(
            us=(0x3F088889, 0x3F4CCCCE, 0x3F888889, 0x40088889),
            eu=(0x3F23D70A, 0x3F75C28F, 0x3FA3D70A, 0x4023D70A),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.5), f32(2.0), f32(3.0)),
            eu=(f32(1.2), f32(1.8), f32(2.4), f32(3.6)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Shock Rocket fire rate instruction",
        offsets=RegionalOffsets(us=0x1A5E8C, eu=0x1A732C, jp=0x1A63BC),
        original=RegionalWords(
            us=(0x3C014270,),
        ),
        replacement=RegionalWords(
            us=(0x3C0141F0,),
        ),
    ),
    PatchGroup(
        name="Helipack vertical movement instructions",
        offsets=RegionalOffsets(us=0x040AB8, eu=0x040BF8, jp=0x040BC0),
        original=RegionalWords(
            us=(0x3C01BCA3, 0x3421D70A, 0x44810000),
            eu=(0x3C01BCC4, 0x34219BA5, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C01BD93, 0x342174BC, 0x44810000),
            eu=(0x3C01BDB0, 0x3421F27C, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Helipack forward movement instructions",
        offsets=RegionalOffsets(us=0x045CC4, eu=0x045E0C, jp=0x045DCC),
        original=RegionalWords(
            us=(0x3C013CF5, 0x3421C290, 0x44810000),
            eu=(0x3C013D13, 0x342174BC, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013E25, 0x3421E354, 0x44810000),
            eu=(0x3C013E47, 0x342110CB, 0x44810000),
        ),
    ),
)


OUTPOST_OMEGA = (
    PatchGroup(
        name="Lacerator damage",
        offsets=RegionalOffsets(us=0x207E6C, eu=0x20938C, jp=0x20838C),
        original=RegionalWords(
            us=(0x3F800000, 0x40400000, 0x40A00000, 0x40800000),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.25), f32(3.0), f32(5.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Lacerator fire interval",
        offsets=RegionalOffsets(us=0x20B8F8, eu=0x20CE18, jp=0x20BE18),
        original=RegionalWords(
            us=(0x3F800000,),
        ),
        replacement=RegionalWords(
            us=(f32(0.4),),
        ),
    ),
    PatchGroup(
        name="Acid Bomb impact damage",
        offsets=RegionalOffsets(us=0x207BEC, eu=0x20910C, jp=0x20810C),
        original=RegionalWords(
            us=(0x40200000, 0x40A00000, 0x41200000, 0x41400000),
        ),
        replacement=RegionalWords(
            us=(f32(3.0), f32(4.5), f32(6.0), f32(7.5)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Acid Bomb trail damage",
        offsets=RegionalOffsets(us=0x207C6C, eu=0x20918C, jp=0x20818C),
        original=RegionalWords(
            us=(0x3D4CCCCE, 0x3DCCCCCE, 0x3E4CCCCE, 0x3ECCCCCE),
            eu=(0x3D75C28F, 0x3DF5C28F, 0x3E75C28F, 0x3EF5C28F),
        ),
        replacement=RegionalWords(
            us=(f32(0.09375), f32(0.1875), f32(0.3), f32(0.375)),
            eu=(f32(0.1125), f32(0.225), f32(0.36), f32(0.45)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun damage",
        offsets=RegionalOffsets(us=0x207F6C, eu=0x20948C, jp=0x20848C),
        original=RegionalWords(
            us=(0x40800000, 0x41000000, 0x41400000, 0x41800000),
        ),
        replacement=RegionalWords(
            us=(f32(13.0), f32(17.0), f32(22.0), f32(28.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun fire interval instructions",
        offsets=RegionalOffsets(us=0x145808, eu=0x146B20, jp=0x145C88),
        original=RegionalWords(
            us=(0x3C013FC0, 0x342100FC, 0x44810000),
            eu=(0x3C013FC0, 0x342100FA, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013F95, 0x34215555, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Scorcher damage",
        offsets=RegionalOffsets(us=0x207FEC, eu=0x20950C, jp=0x20850C),
        original=RegionalWords(
            us=(0x3F088889, 0x3F4CCCCE, 0x3F888889, 0x40088889),
            eu=(0x3F23D70A, 0x3F75C28F, 0x3FA3D70A, 0x4023D70A),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.5), f32(2.0), f32(3.0)),
            eu=(f32(1.2), f32(1.8), f32(2.4), f32(3.6)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Shock Rocket fire rate instruction",
        offsets=RegionalOffsets(us=0x19FD24, eu=0x1A122C, jp=0x1A009C),
        original=RegionalWords(
            us=(0x3C014270,),
        ),
        replacement=RegionalWords(
            us=(0x3C0141F0,),
        ),
    ),
    PatchGroup(
        name="Bee Mine Glove damage",
        offsets=RegionalOffsets(us=0x2084AC, eu=0x2099CC, jp=0x2089CC),
        original=RegionalWords(
            us=(0x4119999A, 0x4199999A, 0x41E66666, 0x4219999A),
        ),
        replacement=RegionalWords(
            us=(f32(30.0), f32(40.0), f32(50.0), f32(60.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Additional Outpost damage word (unlabelled in source)",
        offsets=RegionalOffsets(us=0x2082DC, eu=0x2097FC, jp=0x2087FC),
        original=RegionalWords(
            us=(0x41555556,),
            eu=(0x41800000,),
        ),
        replacement=RegionalWords(
            us=(f32(102.0),),
            eu=(f32(122.4),),
        ),
    ),
    PatchGroup(
        name="Helipack vertical movement instructions",
        offsets=RegionalOffsets(us=0x03F5E0, eu=0x03F720, jp=0x03F6E8),
        original=RegionalWords(
            us=(0x3C01BCA3, 0x3421D70A, 0x44810000),
            eu=(0x3C01BCC4, 0x34219BA5, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C01BD93, 0x342174BC, 0x44810000),
            eu=(0x3C01BDB0, 0x3421F27C, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Helipack forward movement instructions",
        offsets=RegionalOffsets(us=0x0447EC, eu=0x044934, jp=0x0448F4),
        original=RegionalWords(
            us=(0x3C013CF5, 0x3421C290, 0x44810000),
            eu=(0x3C013D13, 0x342174BC, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013E25, 0x3421E354, 0x44810000),
            eu=(0x3C013E47, 0x342110CB, 0x44810000),
        ),
    ),
)


CHALLAX = (
    PatchGroup(
        name="Lacerator damage",
        offsets=RegionalOffsets(us=0x22DCEC, eu=0x22F20C, jp=0x22E40C),
        original=RegionalWords(
            us=(0x3F800000, 0x40400000, 0x40A00000, 0x40800000),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.25), f32(3.0), f32(5.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Lacerator fire interval",
        offsets=RegionalOffsets(us=0x2319A8, eu=0x232EC8, jp=0x2320C8),
        original=RegionalWords(
            us=(0x3F800000,),
        ),
        replacement=RegionalWords(
            us=(f32(0.4),),
        ),
    ),
    PatchGroup(
        name="Acid Bomb impact damage",
        offsets=RegionalOffsets(us=0x22DA6C, eu=0x22EF8C, jp=0x22E18C),
        original=RegionalWords(
            us=(0x40200000, 0x40A00000, 0x41200000, 0x41400000),
        ),
        replacement=RegionalWords(
            us=(f32(3.0), f32(4.5), f32(6.0), f32(7.5)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Acid Bomb trail damage",
        offsets=RegionalOffsets(us=0x22DAEC, eu=0x22F00C, jp=0x22E20C),
        original=RegionalWords(
            us=(0x3D4CCCCE, 0x3DCCCCCE, 0x3E4CCCCE, 0x3ECCCCCE),
            eu=(0x3D75C28F, 0x3DF5C28F, 0x3E75C28F, 0x3EF5C28F),
        ),
        replacement=RegionalWords(
            us=(f32(0.09375), f32(0.1875), f32(0.3), f32(0.375)),
            eu=(f32(0.1125), f32(0.225), f32(0.36), f32(0.45)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun damage",
        offsets=RegionalOffsets(us=0x22DDEC, eu=0x22F30C, jp=0x22E50C),
        original=RegionalWords(
            us=(0x40800000, 0x41000000, 0x41400000, 0x41800000),
        ),
        replacement=RegionalWords(
            us=(f32(13.0), f32(17.0), f32(22.0), f32(28.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun fire interval instructions",
        offsets=RegionalOffsets(us=0x152438, eu=0x153750, jp=0x152908),
        original=RegionalWords(
            us=(0x3C013FC0, 0x342100FC, 0x44810000),
            eu=(0x3C013FC0, 0x342100FA, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013F95, 0x34215555, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Scorcher damage",
        offsets=RegionalOffsets(us=0x22DE6C, eu=0x22F38C, jp=0x22E58C),
        original=RegionalWords(
            us=(0x3F088889, 0x3F4CCCCE, 0x3F888889, 0x40088889),
            eu=(0x3F23D70A, 0x3F75C28F, 0x3FA3D70A, 0x4023D70A),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.5), f32(2.0), f32(3.0)),
            eu=(f32(1.2), f32(1.8), f32(2.4), f32(3.6)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Shock Rocket fire rate instruction",
        offsets=RegionalOffsets(us=0x1BE854, eu=0x1BFD4C, jp=0x1BEDFC),
        original=RegionalWords(
            us=(0x3C014270,),
        ),
        replacement=RegionalWords(
            us=(0x3C0141F0,),
        ),
    ),
    PatchGroup(
        name="Bee Mine Glove damage",
        offsets=RegionalOffsets(us=0x22E32C, eu=0x22F84C, jp=0x22EA4C),
        original=RegionalWords(
            us=(0x4119999A, 0x4199999A, 0x41E66666, 0x4219999A),
        ),
        replacement=RegionalWords(
            us=(f32(30.0), f32(40.0), f32(50.0), f32(60.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Sniper Mine damage",
        offsets=RegionalOffsets(us=0x22E43C, eu=0x22F95C, jp=0x22EB5C),
        original=RegionalWords(
            us=(0x41A80000, 0x42000000, 0x422C0000, 0x42580000),
        ),
        replacement=RegionalWords(
            us=(f32(70.0), f32(75.0), f32(80.0), f32(90.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Helipack vertical movement instructions",
        offsets=RegionalOffsets(us=0x043488, eu=0x0435C8, jp=0x043590),
        original=RegionalWords(
            us=(0x3C01BCA3, 0x3421D70A, 0x44810000),
            eu=(0x3C01BCC4, 0x34219BA5, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C01BD93, 0x342174BC, 0x44810000),
            eu=(0x3C01BDB0, 0x3421F27C, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Helipack forward movement instructions",
        offsets=RegionalOffsets(us=0x048694, eu=0x0487DC, jp=0x04879C),
        original=RegionalWords(
            us=(0x3C013CF5, 0x3421C290, 0x44810000),
            eu=(0x3C013D13, 0x342174BC, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013E25, 0x3421E354, 0x44810000),
            eu=(0x3C013E47, 0x342110CB, 0x44810000),
        ),
    ),
)


DAYNI_MOON = (
    PatchGroup(
        name="Lacerator damage",
        offsets=RegionalOffsets(us=0x262C6C, eu=0x26418C, jp=0x26338C),
        original=RegionalWords(
            us=(0x3F800000, 0x40400000, 0x40A00000, 0x40800000),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.25), f32(3.0), f32(5.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Lacerator fire interval",
        offsets=RegionalOffsets(us=0x266BF8, eu=0x268118, jp=0x267318),
        original=RegionalWords(
            us=(0x3F800000,),
        ),
        replacement=RegionalWords(
            us=(f32(0.4),),
        ),
    ),
    PatchGroup(
        name="Acid Bomb impact damage",
        offsets=RegionalOffsets(us=0x2629EC, eu=0x263F0C, jp=0x26310C),
        original=RegionalWords(
            us=(0x40200000, 0x40A00000, 0x41200000, 0x41400000),
        ),
        replacement=RegionalWords(
            us=(f32(3.0), f32(4.5), f32(6.0), f32(7.5)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Acid Bomb trail damage",
        offsets=RegionalOffsets(us=0x262A6C, eu=0x263F8C, jp=0x26318C),
        original=RegionalWords(
            us=(0x3D4CCCCE, 0x3DCCCCCE, 0x3E4CCCCE, 0x3ECCCCCE),
            eu=(0x3D75C28F, 0x3DF5C28F, 0x3E75C28F, 0x3EF5C28F),
        ),
        replacement=RegionalWords(
            us=(f32(0.09375), f32(0.1875), f32(0.3), f32(0.375)),
            eu=(f32(0.1125), f32(0.225), f32(0.36), f32(0.45)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun damage",
        offsets=RegionalOffsets(us=0x262D6C, eu=0x26428C, jp=0x26348C),
        original=RegionalWords(
            us=(0x40800000, 0x41000000, 0x41400000, 0x41800000),
        ),
        replacement=RegionalWords(
            us=(f32(13.0), f32(17.0), f32(22.0), f32(28.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun fire interval instructions",
        offsets=RegionalOffsets(us=0x161590, eu=0x1628B0, jp=0x161A78),
        original=RegionalWords(
            us=(0x3C013FC0, 0x342100FC, 0x44810000),
            eu=(0x3C013FC0, 0x342100FA, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013F95, 0x34215555, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Scorcher damage",
        offsets=RegionalOffsets(us=0x262DEC, eu=0x26430C, jp=0x26350C),
        original=RegionalWords(
            us=(0x3F088889, 0x3F4CCCCE, 0x3F888889, 0x40088889),
            eu=(0x3F23D70A, 0x3F75C28F, 0x3FA3D70A, 0x4023D70A),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.5), f32(2.0), f32(3.0)),
            eu=(f32(1.2), f32(1.8), f32(2.4), f32(3.6)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Shock Rocket damage",
        offsets=RegionalOffsets(us=0x262FAC, eu=0x2644CC, jp=0x2636CC),
        original=RegionalWords(
            us=(0x42400000, 0x42000000, 0x42340000, 0x42700000),
        ),
        replacement=RegionalWords(
            us=(f32(50.0), f32(55.0), f32(60.0), f32(70.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Shock Rocket fire rate instruction",
        offsets=RegionalOffsets(us=0x1DE6DC, eu=0x1DFBE4, jp=0x1DECD4),
        original=RegionalWords(
            us=(0x3C014270,),
        ),
        replacement=RegionalWords(
            us=(0x3C0141F0,),
        ),
    ),
    PatchGroup(
        name="Bee Mine Glove damage",
        offsets=RegionalOffsets(us=0x2632AC, eu=0x2647CC, jp=0x2639CC),
        original=RegionalWords(
            us=(0x4119999A, 0x4199999A, 0x41E66666, 0x4219999A),
        ),
        replacement=RegionalWords(
            us=(f32(30.0), f32(40.0), f32(50.0), f32(60.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Sniper Mine damage",
        offsets=RegionalOffsets(us=0x2633BC, eu=0x2648DC, jp=0x263ADC),
        original=RegionalWords(
            us=(0x41A80000, 0x42000000, 0x422C0000, 0x42580000),
        ),
        replacement=RegionalWords(
            us=(f32(70.0), f32(75.0), f32(80.0), f32(90.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Helipack vertical movement instructions",
        offsets=RegionalOffsets(us=0x047FC0, eu=0x048100, jp=0x0480C8),
        original=RegionalWords(
            us=(0x3C01BCA3, 0x3421D70A, 0x44810000),
            eu=(0x3C01BCC4, 0x34219BA5, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C01BD93, 0x342174BC, 0x44810000),
            eu=(0x3C01BDB0, 0x3421F27C, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Helipack forward movement instructions",
        offsets=RegionalOffsets(us=0x04D1CC, eu=0x04D314, jp=0x04D2D4),
        original=RegionalWords(
            us=(0x3C013CF5, 0x3421C290, 0x44810000),
            eu=(0x3C013D13, 0x342174BC, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013E25, 0x3421E354, 0x44810000),
            eu=(0x3C013E47, 0x342110CB, 0x44810000),
        ),
    ),
)


INSIDE_CLANK = (
    PatchGroup(
        name="Lacerator damage",
        offsets=RegionalOffsets(us=0x202BEC, eu=0x20410C, jp=0x20368C),
        original=RegionalWords(
            us=(0x3F800000, 0x40400000, 0x40A00000, 0x40800000),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.25), f32(3.0), f32(5.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Lacerator fire interval",
        offsets=RegionalOffsets(us=0x206698, eu=0x207BB8, jp=0x207138),
        original=RegionalWords(
            us=(0x3F800000,),
        ),
        replacement=RegionalWords(
            us=(f32(0.4),),
        ),
    ),
    PatchGroup(
        name="Acid Bomb impact damage",
        offsets=RegionalOffsets(us=0x20296C, eu=0x203E8C, jp=0x20340C),
        original=RegionalWords(
            us=(0x40200000, 0x40A00000, 0x41200000, 0x41400000),
        ),
        replacement=RegionalWords(
            us=(f32(3.0), f32(4.5), f32(6.0), f32(7.5)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Acid Bomb trail damage",
        offsets=RegionalOffsets(us=0x2029EC, eu=0x203F0C, jp=0x20348C),
        original=RegionalWords(
            us=(0x3D4CCCCE, 0x3DCCCCCE, 0x3E4CCCCE, 0x3ECCCCCE),
            eu=(0x3D75C28F, 0x3DF5C28F, 0x3E75C28F, 0x3EF5C28F),
        ),
        replacement=RegionalWords(
            us=(f32(0.09375), f32(0.1875), f32(0.3), f32(0.375)),
            eu=(f32(0.1125), f32(0.225), f32(0.36), f32(0.45)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun damage",
        offsets=RegionalOffsets(us=0x202CEC, eu=0x20420C, jp=0x20378C),
        original=RegionalWords(
            us=(0x40800000, 0x41000000, 0x41400000, 0x41800000),
        ),
        replacement=RegionalWords(
            us=(f32(13.0), f32(17.0), f32(22.0), f32(28.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Concussion Gun fire interval instructions",
        offsets=RegionalOffsets(us=0x1480F0, eu=0x149408, jp=0x148580),
        original=RegionalWords(
            us=(0x3C013FC0, 0x342100FC, 0x44810000),
            eu=(0x3C013FC0, 0x342100FA, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013F95, 0x34215555, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Scorcher damage",
        offsets=RegionalOffsets(us=0x202D6C, eu=0x20428C, jp=0x20380C),
        original=RegionalWords(
            us=(0x3F088889, 0x3F4CCCCE, 0x3F888889, 0x40088889),
            eu=(0x3F23D70A, 0x3F75C28F, 0x3FA3D70A, 0x4023D70A),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.5), f32(2.0), f32(3.0)),
            eu=(f32(1.2), f32(1.8), f32(2.4), f32(3.6)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Shock Rocket damage",
        offsets=RegionalOffsets(us=0x202F2C, eu=0x20444C, jp=0x2039CC),
        original=RegionalWords(
            us=(0x42400000, 0x42000000, 0x42340000, 0x42700000),
        ),
        replacement=RegionalWords(
            us=(f32(50.0), f32(55.0), f32(60.0), f32(70.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Shock Rocket fire rate instruction",
        offsets=RegionalOffsets(us=0x19C064, eu=0x19D50C, jp=0x19C994),
        original=RegionalWords(
            us=(0x3C014270,),
        ),
        replacement=RegionalWords(
            us=(0x3C0141F0,),
        ),
    ),
    PatchGroup(
        name="Bee Mine Glove damage",
        offsets=RegionalOffsets(us=0x20322C, eu=0x20474C, jp=0x203CCC),
        original=RegionalWords(
            us=(0x4119999A, 0x4199999A, 0x41E66666, 0x4219999A),
        ),
        replacement=RegionalWords(
            us=(f32(30.0), f32(40.0), f32(50.0), f32(60.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Sniper Mine damage",
        offsets=RegionalOffsets(us=0x20333C, eu=0x20485C, jp=0x203DDC),
        original=RegionalWords(
            us=(0x41A80000, 0x42000000, 0x422C0000, 0x42580000),
        ),
        replacement=RegionalWords(
            us=(f32(70.0), f32(75.0), f32(80.0), f32(90.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Helipack vertical movement instructions",
        offsets=RegionalOffsets(us=0x03F398, eu=0x03F4D8, jp=0x03F4A0),
        original=RegionalWords(
            us=(0x3C01BCA3, 0x3421D70A, 0x44810000),
            eu=(0x3C01BCC4, 0x34219BA5, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C01BD93, 0x342174BC, 0x44810000),
            eu=(0x3C01BDB0, 0x3421F27C, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Helipack forward movement instructions",
        offsets=RegionalOffsets(us=0x0445A4, eu=0x0446EC, jp=0x0446AC),
        original=RegionalWords(
            us=(0x3C013CF5, 0x3421C290, 0x44810000),
            eu=(0x3C013D13, 0x342174BC, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013E25, 0x3421E354, 0x44810000),
            eu=(0x3C013E47, 0x342110CB, 0x44810000),
        ),
    ),
)


QUODRONA = (
    PatchGroup(
        name="Lacerator damage",
        offsets=RegionalOffsets(us=0x221F7C, eu=0x22349C, jp=0x22269C),
        original=RegionalWords(
            us=(0x3F800000, 0x40400000, 0x40A00000, 0x40800000),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.25), f32(3.0), f32(5.0)),
        ),
        stride=0x10,
        boss=RegionalWords(
            us=(f32(1.0), f32(1.0), f32(2.0), f32(4.0)),
        ),
    ),
    PatchGroup(
        name="Lacerator fire interval",
        offsets=RegionalOffsets(us=0x225A78, eu=0x226F98, jp=0x226198),
        original=RegionalWords(
            us=(0x3F800000,),
        ),
        replacement=RegionalWords(
            us=(f32(0.4),),
        ),
    ),
    PatchGroup(
        name="Acid Bomb impact damage",
        offsets=RegionalOffsets(us=0x221CFC, eu=0x22321C, jp=0x22241C),
        original=RegionalWords(
            us=(0x40200000, 0x40A00000, 0x41200000, 0x41400000),
        ),
        replacement=RegionalWords(
            us=(f32(3.0), f32(4.5), f32(6.0), f32(7.5)),
        ),
        stride=0x10,
        boss=RegionalWords(
            us=(f32(2.0), f32(3.0), f32(4.0), f32(5.0)),
        ),
    ),
    PatchGroup(
        name="Acid Bomb trail damage",
        offsets=RegionalOffsets(us=0x221D7C, eu=0x22329C, jp=0x22249C),
        original=RegionalWords(
            us=(0x3D4CCCCE, 0x3DCCCCCE, 0x3E4CCCCE, 0x3ECCCCCE),
            eu=(0x3D75C28F, 0x3DF5C28F, 0x3E75C28F, 0x3EF5C28F),
        ),
        replacement=RegionalWords(
            us=(f32(0.09375), f32(0.1875), f32(0.3), f32(0.375)),
            eu=(f32(0.1125), f32(0.225), f32(0.36), f32(0.45)),
        ),
        stride=0x10,
        boss=RegionalWords(
            us=(f32(0.125), f32(0.25), f32(0.4), f32(0.5)),
            eu=(f32(0.15), f32(0.3), 0x3EF5C290, f32(0.6)),
        ),
    ),
    PatchGroup(
        name="Concussion Gun damage",
        offsets=RegionalOffsets(us=0x22207C, eu=0x22359C, jp=0x22279C),
        original=RegionalWords(
            us=(0x40800000, 0x41000000, 0x41400000, 0x41800000),
        ),
        replacement=RegionalWords(
            us=(f32(13.0), f32(17.0), f32(22.0), f32(28.0)),
        ),
        stride=0x10,
        boss=RegionalWords(
            us=(f32(10.0), f32(15.0), f32(20.0), f32(25.0)),
        ),
    ),
    PatchGroup(
        name="Concussion Gun fire interval instructions",
        offsets=RegionalOffsets(us=0x14DC18, eu=0x14EF38, jp=0x14E0E0),
        original=RegionalWords(
            us=(0x3C013FC0, 0x342100FC, 0x44810000),
            eu=(0x3C013FC0, 0x342100FA, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013F95, 0x34215555, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Scorcher damage",
        offsets=RegionalOffsets(us=0x2220FC, eu=0x22361C, jp=0x22281C),
        original=RegionalWords(
            us=(0x3F088889, 0x3F4CCCCE, 0x3F888889, 0x40088889),
            eu=(0x3F23D70A, 0x3F75C28F, 0x3FA3D70A, 0x4023D70A),
        ),
        replacement=RegionalWords(
            us=(f32(1.0), f32(1.5), f32(2.0), f32(3.0)),
            eu=(f32(1.2), f32(1.8), f32(2.4), f32(3.6)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Shock Rocket damage",
        offsets=RegionalOffsets(us=0x2222BC, eu=0x2237DC, jp=0x2229DC),
        original=RegionalWords(
            us=(0x42400000, 0x42000000, 0x42340000, 0x42700000),
        ),
        replacement=RegionalWords(
            us=(f32(15.2), f32(17.2), f32(19.2), f32(21.2)),
        ),
        stride=0x10,
        boss=RegionalWords(
            us=(f32(35.0), f32(35.0), f32(35.0), f32(35.0)),
        ),
    ),
    PatchGroup(
        name="Shock Rocket fire rate instruction",
        offsets=RegionalOffsets(us=0x1B8C34, eu=0x1BA0FC, jp=0x1B91C4),
        original=RegionalWords(
            us=(0x3C014270,),
        ),
        replacement=RegionalWords(
            us=(0x3C0141F0,),
        ),
    ),
    PatchGroup(
        name="Bee Mine Glove damage",
        offsets=RegionalOffsets(us=0x2225BC, eu=0x223ADC, jp=0x222CDC),
        original=RegionalWords(
            us=(0x4119999A, 0x4199999A, 0x41E66666, 0x4219999A),
        ),
        replacement=RegionalWords(
            us=(f32(30.0), f32(40.0), f32(50.0), f32(60.0)),
        ),
        stride=0x10,
        boss=RegionalWords(
            us=(f32(15.0), f32(20.0), f32(25.0), f32(30.0)),
        ),
    ),
    PatchGroup(
        name="Sniper Mine damage",
        offsets=RegionalOffsets(us=0x2226CC, eu=0x223BEC, jp=0x222DEC),
        original=RegionalWords(
            us=(0x41A80000, 0x42000000, 0x422C0000, 0x42580000),
        ),
        replacement=RegionalWords(
            us=(f32(70.0), f32(75.0), f32(80.0), f32(90.0)),
        ),
        stride=0x10,
    ),
    PatchGroup(
        name="Laser Tracer damage",
        offsets=RegionalOffsets(us=0x2223BC, eu=0x2238DC, jp=0x222ADC),
        original=RegionalWords(
            us=(0x40A00001, 0x40E55556, 0x4122AAAB, 0x41555556),
            eu=(0x40C00000, 0x41099999, 0x41433333, 0x41800000),
        ),
        replacement=RegionalWords(
            us=(f32(59.5), f32(68.0), f32(76.5), f32(102.0)),
            eu=(f32(71.4), f32(81.6), f32(91.8), f32(122.4)),
        ),
        stride=0x10,
        boss=RegionalWords(
            us=(f32(3.0), f32(5.0), f32(6.0), f32(8.0)),
            eu=(f32(3.6), f32(6.0), f32(7.2), f32(9.6)),
        ),
    ),
    PatchGroup(
        name="Helipack vertical movement instructions",
        offsets=RegionalOffsets(us=0x0415C0, eu=0x041700, jp=0x0416C8),
        original=RegionalWords(
            us=(0x3C01BCA3, 0x3421D70A, 0x44810000),
            eu=(0x3C01BCC4, 0x34219BA5, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C01BD93, 0x342174BC, 0x44810000),
            eu=(0x3C01BDB0, 0x3421F27C, 0x44810000),
        ),
    ),
    PatchGroup(
        name="Helipack forward movement instructions",
        offsets=RegionalOffsets(us=0x0467CC, eu=0x046914, jp=0x0468D4),
        original=RegionalWords(
            us=(0x3C013CF5, 0x3421C290, 0x44810000),
            eu=(0x3C013D13, 0x342174BC, 0x44810000),
        ),
        replacement=RegionalWords(
            us=(0x3C013E25, 0x3421E354, 0x44810000),
            eu=(0x3C013E47, 0x342110CB, 0x44810000),
        ),
    ),
)


GIANT_CLANK_FLIGHT = (
    PatchGroup(
        name="Giant Clank laser damage",
        offsets=RegionalOffsets(us=0x170C2C, eu=0x17234C, jp=0x171B4C),
        original=RegionalWords(
            us=(0x3F800000,),
        ),
        replacement=RegionalWords(
            us=(f32(4.0),),
        ),
    ),
)


# Native boss-health quartet: its second float is the conditional trigger.
BOSS_HEALTH = RegionalOffsets(us=0x2051C4, eu=0x2066C4, jp=0x2058C4)


PATCHES_BY_PLANET = {
    1: POKITARU,
    2: RYLLUS,
    3: KALIDON,
    5: DREAMTIME,
    6: OUTPOST_OMEGA,
    7: CHALLAX,
    8: DAYNI_MOON,
    9: INSIDE_CLANK,
    10: QUODRONA,
    15: GIANT_CLANK_FLIGHT,
}
