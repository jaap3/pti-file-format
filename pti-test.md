# Test files

These .pti files created by a Polyend Tracker device using
firmware version 1.5.0b2.

## ./test/

1. defaults
2. Volume: +24.0 dB
3. Volume: -inf dB
4. Volume: -24.0 DB
5. Panning: -50
6. Panning: +50
7. Tune: -24
8. Tune: +24
9. Finetune: -100
10. Finetune: +100
11. Filter type: Low-pass
12. Filter type: High-pass
13. Filter type: Band-pass
14. Overdrive: 100
15. Bit depth: 4
16. Tune: -12
17. Low-pass / Cutoff: 0 / Resonance: 0
18. High-pass / Cutoff: 0 / Resonance: 100
19. Band-pass / Cutoff: 100 / Resonance: 100
20. Reverb send: 0.0 dB
21. Delay send: 0.0 dB
22. Reverb send: -39.6 dB
23. Delay send: -39.6 dB
24. Forward loop
25. Backward loop
26. Pingpong loop
27. Slice
28. Beat slice
29. Wavetable
30. Granular
31. Volume automation off
32. Volume automation LFO
33. Panning automation Envelope
34. Panning automation LFO
35. Cutoff automation Envelope
36. Cutoff automation LFO
37. Wavetable position Envelop
38. Wavetable position LFO
39. Granular position Envelop
40. Granular position LFO
41. Finetune Envelop
42. Finetune LFO

## ./filter-test/

1. defaults
2. LP Cutoff 100 Resonance 0
3. LP Cutoff 50 Resonance 0
4. LP Cutoff 0 Resonance 0
5. LP Cutoff 100 Resonance 100
6. LP Cutoff 100 Resonance 50
7. LP Cutoff 50 Resonance 50
8. LP Cutoff 0 Resonance 100
9. LP Cutoff 0 Resonance 50
10. HP Cutoff 100 Resonance 0
11. HP Cutoff 50 Resonance 0
12. HP Cutoff 0 Resonance 0
13. HP Cutoff 100 Resonance 100
14. HP Cutoff 100 Resonance 50
15. HP Cutoff 50 Resonance 50
16. HP Cutoff 0 Resonance 100
17. HP Cutoff 0 Resonance 50

## ./envelope-test

1. defaults
2. Volume - Envelope - Attack 10.0s
3. Volume - Envelope - Attack 5.0s
4. Volume - Envelope - Decay 10.0s
5. Volume - Envelope - Decay 5.0s
6. Volume - Envelope - Sustain 50
7. Volume - Envelope - Sustain 0
8. Volume - Envelope - Release 10s
9. Volume - Envelope - Release 0s
10. Volume - Envelope - Amount 50
11. Volume - Envelope - Amount 0

## ./lfo-test/

1. defaults (Triangle, 24 steps, 50)
2. Volume LFO - Rev Saw
3. Volume LFO - Saw
4. Volume LFO - Square
5. Volume LFO - Random
6. Volume LFO - 16 steps
7. Volume LFO - 6 steps
8. Volume LFO - 3/2 steps
9. Volume LFO - 1/64 steps
10. Volume LFO - Amount 100
11. Volume LFO - Amount 0
12. Panning LFO - Rev Saw
13. Panning LFO - Random
14. Panning LFO - 1/48 step
15. Panning LFO - 128 steps (default?)
16. Panning LFO - 24 steps
17. Panning LFO - Amount 80
18. Panning LFO - Amount 66
19. Panning LFO - Amount 25
20. Panning LFO - Amount 10
21. Panning LFO - Amount 100
22. Cutoff LFO - Square - 96 steps - Amount 38
23. Wavetable LFO - Random - 2 steps - Amount 8
24. Granular LFO - Saw - 32 steps - Amount 90
25. Finetune LFO - Square - 3 steps - Amount 100

## ./playback-test/

1. defaults - start 0
2. 1-Shot - start 0.02s
3. 1-Shot - start 0.025s
4. 1-Shot - start 0.125s (50%)
5. 1-Shot - end 0.2
6. 1-Shot - end 0.125s (50%)
7. 1-Shot - zoom 1.41
8. Forward loop - start 0.025s - loop start 0.05
9. Forward loop - end 0.2 - loop end 0.18
10. Backward loop - start 0.033 - loop start 0.111 - end 0.234 - loop end 0.197
11. Pingpong loop - start 0.025 - loop start 0.033 - end 0.250 - loop end 0.190
12. Slice - 1-2 - Adjust 0.025 - Slice 2-2 - Adjust 0.08
13. Start - 2 (0s)
14. Start - 4 (0s)
15. Start - 8 (0s)
16. Start - 16 (0s)
17. Start - 29 (0.001s)
18. Start/End minor adjustments
19. Start/End minor adjustments (visible)
20. Start/End + Looppoint adjustments
21. Extremely short loop
22. Max loop start
23. Min loop end
24. 48 slices
25. Beat slice 1 adjust
26. Beat slice 3
27. Beat slice 4
28. Wavetable window 32 (6)
29. Wavetable window 512 (2)
30. Wavetable window 1024 (1) - position 1
31. Wavetable window 32 (6) - position 343
32. Wavetable window 1024 (1) - position 9
33. Granular loop Backward (1)
34. Granular loop PingPong (2)
35. Granular shape triangle (1)
36. Granular shape gauss (2)
37. Granular length 1.0ms (min)
38. Granular length 250ms (max)
39. Granular position 250ms (max) length 20ms

## ./sample-test/

1. 10ms Granular position 1ms - length 5ms
2. 250ms Granular position 125ms - length 20ms
3. 1000ms Granular position 500ms - length 100ms
4. 5000ms Granular position 0ms - length 1000ms
5. 10000ms Granular position 10000ms - length 1000ms