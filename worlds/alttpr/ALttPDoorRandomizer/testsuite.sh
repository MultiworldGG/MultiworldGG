#!/bin/bash

count=${1:-2}
dr=${2:-basic}
tense=${3:-3} #intensity

printf "Testing %s DR with %s Tests (intensity=%d)\n" $dr $count $tense

rom="../../orig/z3.sfc"
vov=0
vsv=0
viv=0
vor=0
vsr=0
vir=0
vok=0
vsk=0
vik=0
vos=0
vss=0
vis=0
vof=0
vsf=0
vif=0
voc=0
vsc=0
vic=0
voi=0
vsi=0
vii=0
#flags - v - vanilla DR
# osi - mode
# vrk  ER - sfci

for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --shuffle vanilla --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vov++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --mode standard --shuffle vanilla --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vsv++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --mode inverted --shuffle vanilla --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((viv++))
	fi
done

for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --shuffle vanilla --retro --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vor++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --mode standard --shuffle vanilla --retro --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vsr++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --mode inverted --shuffle vanilla --retro --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vir++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --shuffle vanilla --keysanity --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vok++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --mode standard --shuffle vanilla --keysanity --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vsk++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --mode inverted --shuffle vanilla --keysanity --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vik++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --shuffle simple --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vos++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --mode standard --shuffle simple --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vss++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --mode inverted --shuffle simple --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vis++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --shuffle full --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vof++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --mode standard --shuffle full --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vsf++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --mode inverted --shuffle full --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vif++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --shuffle crossed --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((voc++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --mode standard --shuffle crossed --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vsc++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --mode inverted --shuffle crossed --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vic++))
	fi
done

for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --shuffle insanity --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((voi++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --mode standard --shuffle insanity --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vsi++))
	fi
done
for (( i=1; i<=$count; i++ ))
do
	python3 DungeonRandomizer.py --door_shuffle $dr --intensity $tense --mode inverted --shuffle insanity --suppress_rom --suppress_spoiler --rom $rom
	if [[ $? -eq 1 ]]
	then
		((vii++))
	fi
done

printf "DR Stats\n"
printf "Vanilla Open Rate: %.2f%%\n" "$((($count-$vov)*100/$count))"
printf "Vanilla Std  Rate: %.2f%%\n" "$((($count-$vsv)*100/$count))"
printf "Vanilla Inv  Rate: %.2f%%\n" "$((($count-$viv)*100/$count))"

printf "Retro   Open Rate: %.2f%%\n" "$((($count-$vor)*100/$count))"
printf "Retro   Std  Rate: %.2f%%\n" "$((($count-$vsr)*100/$count))"
printf "Retro   Inv  Rate: %.2f%%\n" "$((($count-$vir)*100/$count))"

printf "Keysant Open Rate: %.2f%%\n" "$((($count-$vok)*100/$count))"
printf "Keysant Std  Rate: %.2f%%\n" "$((($count-$vsk)*100/$count))"
printf "Keysant Inv  Rate: %.2f%%\n" "$((($count-$vik)*100/$count))"

printf "Simple  Open Rate: %.2f%%\n" "$((($count-$vos)*100/$count))"
printf "Simple  Std  Rate: %.2f%%\n" "$((($count-$vss)*100/$count))"
printf "Simple  Inv  Rate: %.2f%%\n" "$((($count-$vis)*100/$count))"

printf "Full    Open Rate: %.2f%%\n" "$((($count-$vof)*100/$count))"
printf "Full    Std  Rate: %.2f%%\n" "$((($count-$vsf)*100/$count))"
printf "Full    Inv  Rate: %.2f%%\n" "$((($count-$vif)*100/$count))"

printf "Crossed Open Rate: %.2f%%\n" "$((($count-$voc)*100/$count))"
printf "Crossed Std  Rate: %.2f%%\n" "$((($count-$vsc)*100/$count))"
printf "Crossed Inv  Rate: %.2f%%\n" "$((($count-$vic)*100/$count))"

printf "Insanit Open Rate: %.2f%%\n" "$((($count-$voi)*100/$count))"
printf "Insanit Std  Rate: %.2f%%\n" "$((($count-$vsi)*100/$count))"
printf "Insanit Inv  Rate: %.2f%%\n" "$((($count-$vii)*100/$count))"
printf "%.2f%%\t%.2f%%\t%.2f%%\n" "$((($count-$vov)*100/$count))" "$((($count-$vsv)*100/$count))" "$((($count-$viv)*100/$count))"
printf "%.2f%%\t%.2f%%\t%.2f%%\n" "$((($count-$vor)*100/$count))" "$((($count-$vsr)*100/$count))" "$((($count-$vir)*100/$count))"
printf "%.2f%%\t%.2f%%\t%.2f%%\n" "$((($count-$vok)*100/$count))" "$((($count-$vsk)*100/$count))" "$((($count-$vik)*100/$count))"
printf "%.2f%%\t%.2f%%\t%.2f%%\n" "$((($count-$vos)*100/$count))" "$((($count-$vss)*100/$count))" "$((($count-$vis)*100/$count))"
printf "%.2f%%\t%.2f%%\t%.2f%%\n" "$((($count-$vof)*100/$count))" "$((($count-$vsf)*100/$count))" "$((($count-$vif)*100/$count))"
printf "%.2f%%\t%.2f%%\t%.2f%%\n" "$((($count-$voc)*100/$count))" "$((($count-$vsc)*100/$count))" "$((($count-$vic)*100/$count))"
printf "%.2f%%\t%.2f%%\t%.2f%%\n" "$((($count-$voi)*100/$count))" "$((($count-$vsi)*100/$count))" "$((($count-$vii)*100/$count))"