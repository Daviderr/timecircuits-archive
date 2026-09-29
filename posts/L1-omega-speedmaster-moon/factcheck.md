# Fact-check: Omega Speedmaster: from racetrack to the Moon
Verdict: PASS WITH FIXES

| # | Where (slide/caption) | Claim | Verdict | Evidence (URL + short note) |
|---|---|---|---|---|
| 1 | S1 | Started as a racing chronograph, "never meant to leave Earth" | ✅ VERIFIED | https://en.wikipedia.org/wiki/Omega_Speedmaster: "introduced in 1957 as a sport and racing chronograph" |
| 2 | S1 | "the only watch NASA trusted with the Moon" | ✅ VERIFIED (with a caveat) | Only NASA-issued, flight-qualified watch for Apollo. But on Apollo 15 Dave Scott wore a personal Bulova on the lunar surface (EVA-3) after his Speedmaster's crystal came off (same Wikipedia page). "Trusted" makes it defensible; see optional note |
| 3 | S2 | Launched in 1957 | ✅ VERIFIED | Wikipedia (above); Omega |
| 4 | S2 | Tachymeter scale on the bezel, to measure speed | ✅ VERIFIED | Wikipedia: brushed steel tachymeter bezel, where the "Speedmaster" name comes from |
| 5 | S3 | 1962: Schirra wore his own Speedmaster in orbit aboard Sigma 7 | ✅ VERIFIED | Wikipedia: personal CK 2998 on Mercury-Atlas 8, 3 Oct 1962 |
| 6 | S3 | NASA had no official watch yet in 1962 | ✅ VERIFIED | Qualification came in 1965 (Wikipedia; Omega chronicle below) |
| 7 | S4 | 1964: NASA asks several brands for chronographs | ✅ VERIFIED | Ragan sent a request for quotation to about 10 makers; 4 replied (Rolex, Longines-Wittnauer, Hamilton, Omega). https://www.fratellowatches.com/celebrating-60-years-of-the-omega-speedmaster-becoming-nasa-flight-qualified/ ; Omega: "one of four watch brands invited" https://www.omegawatches.com/chronicle/1965-nasa-tests-and-qualifies-the-speedmaster |
| 8 | S4 | Tests: extreme heat and cold, vacuum, violent shocks, deafening noise | ✅ VERIFIED | Wikipedia: temperatures, humidity, vacuum, oxygen, shock, vibration, acoustic noise |
| 9 | S4 / S5 / caption | The others fail, only the Speedmaster survives | ✅ VERIFIED | Omega chronicle and Wikipedia. (Hamilton was dropped because it sent a pocket watch rather than failing a test; "one by one, they fail" is a slight dramatisation but acceptable) |
| 10 | S5 | March 1965: flight-qualified for manned space missions | ✅ VERIFIED | Omega chronicle: 1 March 1965; NASM post "flight-qualified for all manned space missions" https://x.com/airandspace/status/2028251654315802867 |
| 11 | S5 | Legend: Omega didn't know; the records suggest otherwise | ✅ VERIFIED (correctly framed as a legend) | Wikipedia: order forms sent by NASA's procurement office to Omega's US agents in 1964 "suggest that this anecdote may be exaggerated"; Omega itself says it was "invited" |
| 12 | S6 | Aldrin walked on the Moon wearing his Speedmaster | ✅ VERIFIED | Wikipedia; collectSPACE (below) |
| 13 | S6 | Armstrong left his in the LM as a backup because the electronic timer had failed | ✅ VERIFIED | Wikipedia: left in the LM "because the LM's electronic timer had malfunctioned" |
| 14 | S7 | Aldrin's watch was sent to the Smithsonian, never arrived, never found | ✅ VERIFIED | https://www.collectspace.com/news/news-101303a-buzz-aldrin-apollo-11-omega-speedmaster-missing-lawsuit.html ; the shipment arrived without the watch, and it is still missing |
| 15 | S7 | "The first watch on the Moon" | ⚠️ IMPRECISE | Armstrong's Speedmaster reached the Moon in the same LM, at the same moment. Aldrin's is the first watch *worn on the lunar surface* |
| 16 | S7 | "The most famous watch in history" | ⚠️ OPINION | Hyperbole stated as fact. Tolerable in storytelling tone; see optional |
| 17 | S8 | Apollo 13: crew timed a critical 14-second burn with a Speedmaster | ✅ VERIFIED | Wikipedia (Swigert's Speedmaster); https://www.omegawatches.com/chronicle/1970-the-silver-snoopy-award |
| 18 | S8 | Astronauts gave Omega the Silver Snoopy Award (1970) | ✅ VERIFIED | Omega chronicle 1970: presented by Tom Stafford, with a certificate signed by the Apollo 13 crew |
| 19 | CTA | Still in production, called the Moonwatch | ✅ VERIFIED | Current "Speedmaster Moonwatch Professional"; Wikipedia |
| 20 | Caption | "Five years later" (1964 to 1969) | ✅ VERIFIED | Arithmetic is correct |
| 21 | Caption | "Sources: Omega; NASA; Smithsonian National Air and Space Museum" | ❓ UNSUPPORTED | post.json `sources` lists only Wikipedia. None of the three cited bodies is actually referenced there |

## Required fixes
- Slide 7: "The first watch on the Moon is *missing*" → "The first watch worn on the Moon is *missing*"
- `sources` / caption: the caption credits Omega, NASA and the NASM, but `sources` holds only Wikipedia. Add the real URLs to `sources`: https://www.omegawatches.com/chronicle/1965-nasa-tests-and-qualifies-the-speedmaster , https://www.omegawatches.com/chronicle/1970-the-silver-snoopy-award , https://www.collectspace.com/news/news-101303a-buzz-aldrin-apollo-11-omega-speedmaster-missing-lawsuit.html. Otherwise, change the caption line to "Sources: Omega; Wikipedia; collectSPACE."

## Optional improvements
- Slide 7: "The most famous watch in history is lost." → "Perhaps the most famous watch in history is lost."
- Slide 1: "the only watch NASA trusted with the Moon" is defensible (the only NASA-issued watch), but a pedant may point to Dave Scott's Bulova on Apollo 15. Option: "the watch NASA chose for the Moon." This could also make a future post.
- Slide 7: "It never arrived" → "It never made it" is more precise, because the shipment arrived without the watch.

Summary: 17 of 21 claims verified, including every date, number and the corrected "Omega didn't know" legend. No factual errors.
Two small fixes needed: the "first watch on the Moon" wording and sources that don't match the caption's "Sources" line.
