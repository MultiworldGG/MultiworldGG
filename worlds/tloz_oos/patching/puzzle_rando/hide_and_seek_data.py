class Direction:
    Up = 0x00
    Right = 0x08
    Down = 0x10
    Left = 0x18


class MoveDirection:
    Wait = 0x00
    Up = 0xec
    Right = 0xed
    Down = 0xee
    Left = 0xef


class LookDirection:
    DownUpRightLeft = 0x69fe
    UpDownRightLeft = 0x6a0b
    RightLeftUpDown = 0x6a13
    LeftRightUpDown = 0x6a20


hide_and_seek_data = [
    [  # First screen
        {
            # Vanilla 1-1-1
            "start": 0x14,
            "start_angle": Direction.Left,
            "moves": [
                (MoveDirection.Left, 0x30),
                LookDirection.RightLeftUpDown,
                (MoveDirection.Down, 0x60),
                LookDirection.UpDownRightLeft,
                (MoveDirection.Down, 0x20),
            ]
        },
        {
            # Vanilla 1-1-2
            "start": 0x41,
            "start_angle": Direction.Up,
            "moves": [
                (MoveDirection.Up, 0x30),
                LookDirection.DownUpRightLeft,
                (MoveDirection.Right, 0x30),
                (MoveDirection.Down, 0x10),
                (MoveDirection.Right, 0x10),
                LookDirection.LeftRightUpDown,
                (MoveDirection.Down, 0x50),
                LookDirection.UpDownRightLeft,
                (MoveDirection.Down, 0x20)
            ]
        },
        {
            # Vanilla 1-2-1
            "start": 0x21,
            "start_angle": Direction.Down,
            "moves": [
                (MoveDirection.Down, 0x40),
                LookDirection.UpDownRightLeft,
                (MoveDirection.Right, 0x30),
                LookDirection.LeftRightUpDown,
                (MoveDirection.Down, 0x18),
                LookDirection.UpDownRightLeft,
                (MoveDirection.Down, 0x20),
            ]
        },
        {
            # Vanilla 1-2-2
            "start": 0x42,
            "start_angle": Direction.Up,
            "moves": [
                (MoveDirection.Up, 0x20),
                LookDirection.DownUpRightLeft,
                (MoveDirection.Right, 0x30),
                (MoveDirection.Down, 0x10),
                (MoveDirection.Right, 0x30),
                LookDirection.LeftRightUpDown,
                (MoveDirection.Left, 0x30),
                (MoveDirection.Down, 0x20),
                (MoveDirection.Left, 0x30),
                LookDirection.RightLeftUpDown,
                (MoveDirection.Down, 0x40),
            ]
        },
        {
            # Guard the house
            "start": 0x48,
            "start_angle": Direction.Down,
            "moves": [
                (MoveDirection.Wait, 120),
                Direction.Left,
                (MoveDirection.Wait, 120),
                Direction.Up,
                (MoveDirection.Wait, 120),
                (MoveDirection.Left, 0x30),
                (MoveDirection.Down, 0x50),
            ]
        },
        {
            # Spin
            "start": 0x55,
            "start_angle": Direction.Left,
            "moves": [
                (MoveDirection.Left, 0x30),
                Direction.Down,
                (MoveDirection.Wait, 60),
                Direction.Left,
                (MoveDirection.Wait, 60),
                (MoveDirection.Up, 0x30),
                Direction.Left,
                (MoveDirection.Wait, 60),
                Direction.Up,
                (MoveDirection.Wait, 60),
                (MoveDirection.Right, 0x30),
                Direction.Up,
                (MoveDirection.Wait, 60),
                Direction.Right,
                (MoveDirection.Wait, 60),
                (MoveDirection.Down, 0x70),
            ]
        }
    ],
    [  # Second screen
        {
            # Vanilla 2-1-1
            "start": 0x27,
            "start_angle": Direction.Down,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Down, 0x30),
                LookDirection.UpDownRightLeft,
                (MoveDirection.Wait, 180),
                (MoveDirection.Left, 0x30),
                (MoveDirection.Up, 0x30),
                LookDirection.UpDownRightLeft,
                (MoveDirection.Right, 0x30),
                (MoveDirection.Down, 0x30),
                (MoveDirection.Wait, 120),
                (MoveDirection.Left, 0x10),
                (MoveDirection.Down, 0x20),
                LookDirection.UpDownRightLeft,
                (MoveDirection.Down, 0x20),
            ]
        },
        {
            # Vanilla 2-1-2
            "start": 0x72,
            "start_angle": Direction.Left,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Left, 0x10),
                (MoveDirection.Up, 0x30),
                (MoveDirection.Wait, 150),
                (MoveDirection.Right, 0x20),
                LookDirection.LeftRightUpDown,
                (MoveDirection.Up, 0x30),
                (MoveDirection.Left, 0x20),
                LookDirection.RightLeftUpDown,
                (MoveDirection.Wait, 120),
                (MoveDirection.Right, 0x30),
                (MoveDirection.Down, 0x60),
                LookDirection.UpDownRightLeft,
                (MoveDirection.Down, 0x20)
            ]
        },
        {
            # Vanilla 2-2-1
            "start": 0x28,
            "start_angle": Direction.Left,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Left, 0x10),
                (MoveDirection.Down, 0x20),
                LookDirection.UpDownRightLeft,
                (MoveDirection.Down, 0x10),
                (MoveDirection.Left, 0x30),
                (MoveDirection.Down, 0x20),
                LookDirection.UpDownRightLeft,
                (MoveDirection.Left, 0x30),
                (MoveDirection.Up, 0x30),
                (MoveDirection.Right, 0x20),
                (MoveDirection.Up, 0x30),
                LookDirection.DownUpRightLeft,
                (MoveDirection.Right, 0x10),
                (MoveDirection.Down, 0x80),
            ]
        },
        {
            # Vanilla 2-2-2
            "start": 0x73,
            "start_angle": Direction.Right,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Right, 0x30),
                (MoveDirection.Up, 0x20),
                LookDirection.DownUpRightLeft,
                (MoveDirection.Left, 0x20),
                (MoveDirection.Up, 0x30),
                LookDirection.DownUpRightLeft,
                (MoveDirection.Wait, 90),
                (MoveDirection.Right, 0x30),
                (MoveDirection.Down, 0x30),
                (MoveDirection.Left, 0x10),
                (MoveDirection.Down, 0x40),
            ]
        },
        {
            # Check the corners
            "start": 0x55,
            "start_angle": Direction.Up,
            "moves": [
                LookDirection.UpDownRightLeft,
                (MoveDirection.Left, 0x10),
                (MoveDirection.Up, 0x50),
                LookDirection.UpDownRightLeft,
                (MoveDirection.Wait, 60),
                (MoveDirection.Down, 0x20),
                (MoveDirection.Right, 0x40),
                LookDirection.LeftRightUpDown,
                (MoveDirection.Left, 0x10),
                (MoveDirection.Down, 0x30),
                (MoveDirection.Left, 0x30),
                (MoveDirection.Down, 0x20),
                LookDirection.LeftRightUpDown,
                (MoveDirection.Down, 0x20),
            ]
        },
        {
            # Fakeout guy
            "start": 0x44,
            "start_angle": Direction.Left,
            "moves": [
                LookDirection.LeftRightUpDown,
                (MoveDirection.Up, 0x60),
                (MoveDirection.Wait, 30),
                (MoveDirection.Down, 0x20),
                LookDirection.DownUpRightLeft,
                (MoveDirection.Down, 0x90),
                (MoveDirection.Wait, 30),
                (MoveDirection.Up, 0x20),
                LookDirection.UpDownRightLeft,
                (MoveDirection.Down, 0x20),
            ]
        }
    ],
    [  # Third screen
        {
            # Vanilla 3-1-1
            "start": 0x37,
            "start_angle": Direction.Left,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Left, 0x60),
                LookDirection.RightLeftUpDown,
                (MoveDirection.Up, 0x20),
                LookDirection.DownUpRightLeft,
                (MoveDirection.Up, 0x10),
                (MoveDirection.Right, 0x40),
                (MoveDirection.Down, 0x30),
                LookDirection.UpDownRightLeft,
                (MoveDirection.Left, 0x40),
                (MoveDirection.Down, 0x10),
                (MoveDirection.Left, 0x30),
            ]
        },
        {
            # Vanilla 3-1-2
            "start": 0x34,
            "start_angle": Direction.Left,
            "moves": [
                (MoveDirection.Wait, 122),
                Direction.Down,
                (MoveDirection.Wait, 62),
                Direction.Right,
                (MoveDirection.Wait, 62),
                Direction.Up,
                (MoveDirection.Wait, 62),
                (MoveDirection.Left, 0x30),
                (MoveDirection.Down, 0x10),
                (MoveDirection.Left, 0x30),
            ]
        },
        {
            # Vanilla 3-2-1
            "start": 0x38,
            "start_angle": Direction.Left,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Left, 0x50),
                Direction.Right,
                (MoveDirection.Wait, 60),
                Direction.Left,
                (MoveDirection.Wait, 180),
                (MoveDirection.Left, 0x10),
                (MoveDirection.Up, 0x10),
                (MoveDirection.Left, 0x20),
                LookDirection.RightLeftUpDown,
                (MoveDirection.Left, 0x20),
            ]
        },
        {
            # Vanilla 3-2-2
            "start": 0x32,
            "start_angle": Direction.Left,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Left, 0x10),
                LookDirection.RightLeftUpDown,
                (MoveDirection.Up, 0x20),
                (MoveDirection.Left, 0x10),
                LookDirection.RightLeftUpDown,
                (MoveDirection.Right, 0x20),
                (MoveDirection.Up, 0x10),
                (MoveDirection.Right, 0x30),
                (MoveDirection.Down, 0x30),
                (MoveDirection.Left, 0x30),
                (MoveDirection.Up, 0x10),
                (MoveDirection.Left, 0x20),
                LookDirection.RightLeftUpDown,
                (MoveDirection.Left, 0x20),
            ]
        },
        {
            # Just watching the waves
            "start": 0x52,
            "start_angle": Direction.Down,
            "moves": [
                (MoveDirection.Wait, 600),
                (MoveDirection.Left, 0x40),
            ]
        },
        {
            # Go counterclockwise
            "start": 0x41,
            "start_angle": Direction.Left,
            "moves": [
                LookDirection.LeftRightUpDown,
                (MoveDirection.Up, 0x10),
                (MoveDirection.Right, 0x40),
                LookDirection.RightLeftUpDown,
                (MoveDirection.Up, 0x30),
                (MoveDirection.Left, 0x30),
                (MoveDirection.Down, 0x10),
                (MoveDirection.Left, 0x20),
                LookDirection.LeftRightUpDown,
                (MoveDirection.Left, 0x20)
            ]
        }
    ],
    [  # Fourth screen
        {
            # Vanilla 4-1-1
            "start": 0x33,
            "start_angle": Direction.Left,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Left, 0x20),
                LookDirection.RightLeftUpDown,
                (MoveDirection.Up, 0x20),
                (MoveDirection.Right, 0x60),
                (MoveDirection.Up, 0x10),
                LookDirection.DownUpRightLeft,
                (MoveDirection.Up, 0x20),
            ]
        },
        {
            # Vanilla 4-1-2
            "start": 0x11,
            "start_angle": Direction.Down,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Down, 0x30),
                LookDirection.UpDownRightLeft,
                (MoveDirection.Right, 0x50),
                LookDirection.LeftRightUpDown,
                (MoveDirection.Up, 0x10),
                (MoveDirection.Right, 0x20),
                LookDirection.LeftRightUpDown,
                (MoveDirection.Up, 0x50),
            ]
        },
        {
            # Vanilla 4-2-1
            "start": 0x34,
            "start_angle": Direction.Up,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Up, 0x20),
                LookDirection.DownUpRightLeft,
                (MoveDirection.Wait, 180),
                (MoveDirection.Right, 0x40),
                LookDirection.LeftRightUpDown,
                (MoveDirection.Wait, 60),
                (MoveDirection.Down, 0x20),
                (MoveDirection.Left, 0x20),
                (MoveDirection.Down, 0x10),
                LookDirection.UpDownRightLeft,
                (MoveDirection.Left, 0x50),
                LookDirection.RightLeftUpDown,
                (MoveDirection.Up, 0x60),
            ]
        },
        {
            # Vanilla 4-2-2
            "start": 0x01,
            "start_angle": Direction.Down,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Down, 0x30),
                (MoveDirection.Right, 0x20),
                (MoveDirection.Up, 0x20),
                (MoveDirection.Left, 0x20),
                (MoveDirection.Up, 0x20),
            ]
        },
        {
            # Love the sea
            "start": 0x57,
            "start_angle": Direction.Down,
            "moves": [
                (MoveDirection.Wait, 300),
                (MoveDirection.Right, 0x40),
                (MoveDirection.Wait, 180),
                (MoveDirection.Left, 0x80),
                Direction.Down,
                (MoveDirection.Wait, 120),
                LookDirection.LeftRightUpDown,
                (MoveDirection.Up, 0x70)
            ]
        },
        {
            # Back and forths
            "start": 0x15,
            "start_angle": Direction.Up,
            "moves": [
                LookDirection.UpDownRightLeft,
                (MoveDirection.Left, 0x10),
                (MoveDirection.Down, 0x30),
                (MoveDirection.Right, 0x20),
                (MoveDirection.Up, 0x10),
                (MoveDirection.Right, 0x10),
                (MoveDirection.Up, 0x20),
                (MoveDirection.Left, 0x30),
                (MoveDirection.Down, 0x20),
                (MoveDirection.Up, 0x20),
                Direction.Right,
                (MoveDirection.Wait, 30),
                (MoveDirection.Left, 0x30),
                (MoveDirection.Down, 0x20),
                (MoveDirection.Up, 0x50)
            ]
        }
    ]
]
