function main()
    local FRAME = 0
    local changed_map = 0x0
    while true do
        FRAME = FRAME + 1
        if (FRAME % 120 == 1) then
            CURRENT_MAP = mainmemory.read_u16_be(0x12B402)
            if changed_map ~= CURRENT_MAP
            then
                client.saveram()
                changed_map = CURRENT_MAP
            end
        end
        emu.frameadvance()
    end
end
main()