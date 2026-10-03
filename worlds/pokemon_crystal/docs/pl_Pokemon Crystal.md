# Pokémon Crystal

## Gdzie jest strona opcji?

Możesz zapoznać się ze wszystkimi opcjami i wygenerować plik YAML [tutaj](../player-options).

## Jak losowość wpływa na tę grę?

W podstawowej wersji gry wprowadzono pewne zmiany związane z losowością:

- Dyrektor zawsze przebywa w podziemnym magazynie, nawet gdy wieża radiowa nie jest zajęta.
- Drzwi na kartę w domu towarowym Goldenrod na poziomie B1F otwierają się za pomocą karty znajdującej się w plecaku.
- Kontrole oparte na czasie, takie jak rodzeństwo z dnia tygodnia i facet na dachu rezydencji Celadon, są zawsze
  dostępne.
    - Ukryte przedmioty pod Freidą i Wesleyem zostały przeniesione o jedną płytkę, aby pozostały dostępne.
- Statek między Olivine a Vermilion jest zawsze obecny w grach innych niż Johto, nawet przed wejściem do Hall of Fame,
  i można nim pływać za pomocą S.S. Ticket bez ograniczeń co do dnia tygodnia.
- Półka na Route 45 została przesunięta, aby wszystkie przedmioty i trenerzy byli dostępni w 2 przejściach
- W przypadku opcji, które to umożliwiają, odznaki Kanto odpowiadają następującym HM:
    - HM01 Cut - Cascade Badge
    - HM02 Fly - Thunder Badge
    - HM03 Surf - Soul Badge
    - HM04 Strength - Rainbow Badge
    - HM05 Flash - Boulder Badge
    - HM06 Whirlpool - Volcano Badge
    - HM07 Waterfall - Earth Badge
- TM02 i TM08 będą zawsze odpowiednio Headbutt i Rock Smash i zawsze będą wielokrotnego użytku.
- Ewolucje wymiany zostały zmienione, aby były możliwe w trybie solo:
    - Zwykłe ewolucje wymiany następują po użyciu na Pokémonie kluczowego przedmiotu Link Cable.
    - Ewolucje wymiany z trzymanym przedmiotem następują po użyciu Link Cable na Pokémonie, który trzyma swój
      przedmiot ewolucyjny.
- Eevee ewoluuje w Espeona i Umbreona odpowiednio za pomocą kamienia słońca i kamienia księżyca.
- Ewolucje szczęścia są logicznie powiązane z dostępem do podziemi Goldenrod lub Pallet Town. Młodszy brat o krótkiej
  fryzurze i Daisy maksymalizują poziom szczęścia pokemona i są zawsze dostępni.
- Unown pojawia się na wolności dopiero po rozwiązaniu jednej układanki w Ruinach Alph (Ruins of Alph). Wcześniej
  każde spotkanie, w którym pojawiłby się Unown, zamiast tego odtworzy tylko jego okrzyk
- Po zdobyciu Kryształowego Dzwonu (Clear Bell) można wejść na 1F Cynowej Wieży (Tin Tower).
- Schody prowadzące na 2F i wyższe poziomy Cynowej Wieży pojawiają się, gdy spełniony zostanie wspomniany warunek
  i gracz posiada Tęczowe Pióro (Rainbow Wing). Oba są przedmiotami w multiworld.
- Eusine przekaże graczowi wiadomość Eon Mail, jeśli porozmawia z nim na 1F Cynowej Wieży po zobaczeniu Suicune
  w świecie gry we wszystkich możliwych lokalizacjach, które można odwiedzać w dowolnej kolejności
- Wydarzenie Celebi można aktywować, przekazując Kurtowi przedmiot wieloświatowy GS Ball po ukończeniu Slowpoke Well i
  pokonaniu rywala w Azalea.
- Wydarzenie, które zazwyczaj zapewnia GS Ball w Goldenrod Pokécenter 1F, aktywuje się po zdobyciu tytułu mistrza.
- Mężczyzna w Vermilion City, który daje nagrodę za posiadanie wszystkich odznak, sprawdza tylko 8 odznak Kanto
- Dostęp do komnaty z przedmiotem Ho-Oh w Ruinach Alph można uzyskać, posiadając Tęczowe Pióro
- Do 2F wszystkich centrów Pokémon dodano sklep, którego asortyment można dostosować za pomocą opcji `build_a_mart`.
  Sklep zawsze będzie sprzedawał Poké Balls i Escape Ropes
- Na 2F wszystkich centrów Pokémon dodano postać NPC, która pozwala walczyć z losowym dzikim Pokémonem.
  Walka ta zapewnia pieniądze i doświadczenie, ale nie zapewnia wpisów do Pokédexu i nie można złapać pokemona.
- Jeśli jest to losowe, profesor Elm poinformuje cię o twoim celu, gdy porozmawiasz z nim w jego laboratorium lub
  zadzwonisz do niego.
- Zakładka "Obszar" na stronie Pokédexu danego Pokémona została ulepszona, aby umożliwić przełączanie się między
  spotkaniami o poranku, w ciągu dnia i w nocy. Na mapie wyświetlane są wyłącznie spotkania na lądzie i na wodzie.
  Spotkania związane z wędkarstwem, atakiem Taran, atakiem Kamienny Grom oraz Zawody w Łapaniu Pokémonów Robaków można
  wyświetlić w zakładce "Więcej".

## Jakie przedmioty i lokalizacje są losowane?

Domyślnie losowane są przedmioty z kul przedmiotów i przedmioty przekazywane przez NPC.
Odznaki mogą być standardowe, przetasowane lub losowe. Pokégear i jego moduły kart mogą być standardowe lub losowe.
Jeśli włączony jest tryb Johto Only, przedmioty w Kanto nie będą losowane, a Kanto będzie niedostępne.
S.S. Ticket przekazywany przez Elma po pokonaniu Elitarnej Czwórki zostanie wtedy zastąpiony Srebrnym Skrzydłem
(Silver Wing).

Istnieją opcje umożliwiające dodanie większej liczby przedmiotów do puli:

- Losowe ukryte przedmioty: dodaje ukryte przedmioty do puli
- Losowe drzewa jagodowe: dodaje przedmioty z drzew jagodowych do puli
- Szaleństwo trenerów: dodaje do puli nagrodę za pokonanie trenerów
- Dexsanity: wpis Pokémona w Dexie może zawierać czek. Jest to powiązane z konkretnym Pokémonem
- Dexcountsanity: pewna liczba wpisów w Dexie zawiera czeki. Nie jest to powiązane z konkretnym Pokémonem, ale z
  całkowitą liczbą
- Shopsanity: dodaje przedmioty ze sklepu do puli
- Grasssanity: ścięcie każdej płytki trawy jest lokacją
- Zawody w Łapaniu Pokémonów Robaków: tasuje nagrody za zawody w łapaniu Pokémonów Robaków, od udziału po zwycięstwo
- Losowe prośby o Pokémony: dodaje do puli nagrody od dziadka Billa oraz nagrodę za Magikarpa z Jeziora Wściekłości
  (Lake of Rage)
- Losowe rozmowy telefoniczne: dodaje do puli przedmioty z rozmów telefonicznych od trenerów
- Momsanity: Dodaje do puli przedmioty zakupione za oszczędności mamy
- Battle Tower Sanity: Dodaje nagrodę za pokonanie 10 poziomów Wieży Walki oraz, opcjonalnie, każdego trenera

## Jakie inne zmiany wprowadzono do gry?

Wprowadzono wiele dodatkowych zmian poprawiających komfort gry:

- Do menu opcji w grze dodano nową opcję szybkości tekstu, Instant.
- Przyciski A i/lub B mogą służyć jako przyciski turbo, umożliwiające przyspieszenie dialogów.
- Opcja Battle Scene jest bardziej szczegółowa, a najszybszy wybór, Speedy, eliminuje prawie wszystkie animacje.
- Możesz przytrzymać przycisk B, aby biec i przyspieszyć na rowerze oraz podczas surfowania. Dostępna jest również
  opcja Auto-run, a jeśli jest włączona, przycisk B uniemożliwia bieganie.
- Dodano wiele innych opcji, które znacznie przyspieszają rozgrywkę, w tym: Rods mogą zawsze działać, niezłapane
  pokemony mogą pojawiać się częściej, trenerzy mogą być ślepi itp.
- Usunięto opóźnienia w menu
- Rower można używać w pomieszczeniach
- Z Escape Rope można korzystać w większej liczbie wnętrz, na przykład w Gymach
- Jeśli skończy się repelent, a masz więcej w plecaku, pojawi się monit o użycie kolejnego.
- Tempo wzrostu pokemonów zostało znormalizowane (średnio-szybkie dla pokemonów niebędących legendarnymi, wolne dla
  pokemonów legendarnych).
- Usunięto system resetowania zegara za pomocą hasła. Zegar można zresetować, naciskając przyciski Down + Select + B na
  ekranie tytułowym.
- Dodano opcję w grze, dzięki której nie trzeba uczyć się ruchów terenowych. Aby zachować dostępność ruchów Fly, Flash i
  innych ruchów terenowych, po naciśnięciu przycisku Select w menu Start dostępne jest dodatkowe menu.
- Możesz odnowić wszystkie statyczne wydarzenia, rozmawiając z osobą odpowiedzialną za kapsułę czasu na 2F
  dowolnego PokéCenter
- Możesz teleportować się z powrotem do miasta startowego, wybierając opcję „Go Home” w menu Start

## Jak wygląda przedmiot z innego świata w Pokémon Crystal?

Przedmioty z innych światów będą drukować nazwę przedmiotu i nazwę gracza, który go otrzymał, po zebraniu. Ze względu na
ograniczenia tekstu w grze nazwy te są skracane do 16 znaków, a znaki specjalne, których nie ma w
czcionce, są zastępowane znakami zapytania.

Dzięki opcji `colored_item_balls` kule z przedmiotami w świecie gry będą miały również inny kolor w zależności od
kategorii przedmiotu.

## Co się dzieje, gdy gracz otrzymuje przedmiot?

Opcja w grze "AP Item Notify" pozwala odtworzyć dźwięk i/lub wyświetlić okienko z powiadomieniem po otrzymaniu
przedmiotu.
Odtwarzane są różne dźwięki, aby odróżnić przedmioty związane z postępami w grze od pułapek. Przedmioty można zdobywać
zarówno w świecie otwartej gry, jak i podczas walki.

## Czy mogę grać w trybie offline?

Tak, gra nie wymaga połączenia z klientem w przypadku nasion solo. Połączenie jest wymagane tylko do wysyłania i
odbierania przedmiotów. Nie dotyczy to sytuacji, gdy włączona jest opcja `remote_items`.

## Czy mogę grać w trybie kooperacyjnym?
Tak, zdecydowana większość wydarzeń fabularnych i złapanych pokemonów zostanie zsynchronizowana na wszystkich
klientach, gdy opcja `remote_items` jest włączona.
Gracze mogą skorzystać z ustawienia "Tracker Slot" w grze, aby zapobiec zakłóceniom podczas automatycznego śledzenia
map.
