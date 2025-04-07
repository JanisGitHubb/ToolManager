# Akcepttestu veicējiem:
Programmu Tool Manager iespējams testēt divos dažādos veidos:
 1) lejupielādējot attiecīgo programmas kodu un ar to saistītās bibliotēkas no GitHub repozitorija
 2) palaižot programmu no kādas pārlūkprogrammas, dodoties uz konkrētu saiti. Par saiti vaicāt 

  - Pēc koda lejupielādēšanas no GitHub repozitorija, ir nepieciešams izvēlētajā koda rediģēšanas vidē (VsCode, PyCharm, utt.) lejupielādēt pip un Flask bibliotēkas (versija attiecīgi vismaz  25.0.1 un 3.0.3). Ja nepieciešams veikt arī vienībtestu palaišanu, tad papildus nepieciešams lejupielādēt pytest 8.3.4 un pytest-cov 5.0.0. Lejupielāde parasti norisinās attiecīgā datora terminālī.
  - Lietotājsaskarsmes testēšanu iespējams veikt arī caur attiecīgo programmas toolManager mājaslapu, ja serveris ir palaists tiešaisstē (kontaktēties ar darba autoriem).

  3) Pēc visu attiecīgo bibliotēku lejupielādēšanas (ja tiek izmantots 1. testēšanas variants), attiecīgajā programmas kodā nepieciešams navigēt uz mapi "Python", iekš kuras atrodas fails "app.py". Atverot šo failu un izstrādes vides labajā apakšējā stūrī nospiežot pogu "Go Live", iespējams lokāli palaist programmu Tool Manager Google Chrome pārlūkprogrammā. Papildus tam, ja nepieciešams navigēt uz vēl citiem failiem, visa programmas loģika atrodama šajā pašā mapē "Python", savukārt visa vizuālā programmas (HTML) interpretācija atrodas mapē "templates". Ja nepieciešama piekļuve veiktajiem vienībtestiem, tos iespējams atrast mapē "tests". 